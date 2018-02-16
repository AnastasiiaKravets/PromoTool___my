import random
from datetime import date, timedelta

import utilities
from BaseTest import BaseTest
from Pages.home_page.HomePage import HomePage
from Pages.promo_detail_page import PromoDetailLabels
from Pages.promo_detail_page.BasicInformationForm import BasicInformation
from Pages.promo_detail_page.ComparedPromoWidget import ComparedPromoWidget
from Pages.promo_detail_page.DepartmentsViewWidget import DepartmentViewWidget
from Pages.promo_detail_page.FinancialInformationWidget import FinancialInformation
from Pages.promo_detail_page.PagesViewWidget import PagesViewWidget
from Pages.promo_detail_page.PromoDetailPage import PromoDetailPage
from Pages.promo_type_page.NewPromoTypePage import NewPromoTypePage
from Pages.promo_type_page.PromoTypePage import PromoTypePage
from utilities import utils
from utilities.DataBase import DataBase
from utilities.PromoRequest import PromoRequest
from utilities.Table import Table


class PromoTemplateTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        cls.promo_id = utils.add_full_promo_type()
        cls.data_base = DataBase(utilities.DataBase.get_connection_parameters())
        cls.valid_from_date = (date.today() - timedelta(days=10)).strftime('%Y-%m-%d')
        cls.valid_to_date = (date.today() + timedelta(days=20)).strftime('%Y-%m-%d')
        # cls.promo_id = 101

    @classmethod
    def tearDownClass(cls):
        utils.delete_promo_type(cls.promo_id)

    def setUp(self):
        super().setUp()
        self.driver.get(self.base_url + '404')
        request = PromoRequest(self.driver)
        request.authorization_by_request(login=self.autotest_user['login'],
                                         password=self.autotest_user['password'], language='cs')
        request.create_update_promo_type(promo_type_id=self.promo_id,
                                         name='default string' + str(random.randint(0, 500)),
                                         key_code='default string' + str(random.randint(0, 500)),
                                         valid_from=self.valid_from_date, valid_to=self.valid_to_date)
        self.driver.get(self.base_url + 'promo-type/{0}'.format(self.promo_id))
        self.type_page = NewPromoTypePage(self.driver)

    def test_0_validity_message(self):
        """Try to create template with expired, not set or has not started validity"""
        valid_from = ['NULL',
                      (date.today() - timedelta(days=10)).strftime('%Y-%m-%d'),
                      (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')]
        valid_to = ['NULL',
                    (date.today() - timedelta(days=3)).strftime('%Y-%m-%d'),
                    (date.today() + timedelta(days=20)).strftime('%Y-%m-%d')]

        subtest_name = ['Validity of Promo Type not set',
                        'Promo type validity expired',
                        "Promo type hasn't started yet"]
        message = ['Špatná doba platnosti nebo platnost vypršela!',
                   'Špatná doba platnosti nebo platnost vypršela!',
                   'Akce ještě nezačala']
        assertion_error = ['Wrong message for Validity of Promo Type not set',
                           'Wrong message for expired validity from/to date',
                           "Wrong message 'Promo type hasn't started yet'"]

        for i in range(len(valid_from)):
            if i == 0:
                self.data_base.execute("UPDATE [PromoToolGlobus].[PromoTool].[PromoActionType] "
                                       "SET ValidFrom = NULL, ValidTo = NULL, templateId = NULL "
                                       "WHERE Id={}".format(self.promo_id))
            else:
                self.data_base.execute("UPDATE [PromoToolGlobus].[PromoTool].[PromoActionType] "
                                       "SET ValidFrom = '{}', ValidTo = '{}' "
                                       "WHERE Id={}".format(valid_from[i], valid_to[i], self.promo_id))
            self.driver.refresh()
            self.type_page.wait_spiner_loading() \
                .click_create_template_button()
            with self.subTest(subtest_name[i]):
                self.assertEqual(message[i], self.type_page.get_dialog_message(),
                                 assertion_error[i])
            self.type_page.click_ok_to_pop_up_dialog()

    def test_1_create_new_template(self):
        """Create new template with valid data"""
        self.data_base.execute("UPDATE [PromoToolGlobus].[PromoTool].[PromoActionType] "
                               "SET ValidFrom = '{}', ValidTo = '{}', templateId = NULL "
                               "WHERE Id={}".format(self.valid_from_date, self.valid_to_date, self.promo_id))
        self.driver.refresh()
        self.type_page.wait_spiner_loading() \
            .click_create_template_button()
        self.type_page.wait_for_url_contain('promo-detail/', "New template wasn't created")
        template_id = self.data_base.select_in_list("SELECT templateId "
                                                    "FROM [PromoToolGlobus].[PromoTool].[PromoActionType] "
                                                    "WHERE Id = {}".format(self.promo_id))[0][0]
        if template_id is None:
            raise Exception("New template wasn't created")
        self.assertEqual(self.base_url + 'promo-detail/' + str(template_id), self.driver.current_url,
                         'After creating new promo template was opened template with another url than in data base')
        self.driver.get(self.base_url + 'promo-type')
        promo_type_page = PromoTypePage(self.driver)
        promo_type_row = Table(self.driver, promo_type_page.get_table_content()).wait_table_to_load().get_row_by_id(
            self.promo_id)
        self.assertTrue(promo_type_page.is_template_button_present(promo_type_row),
                        'There is no Template button in promo type row for recently created template')

    def test_2_default_template_view(self):
        """Verify presence and state of all element on Promo detail and Additional information tabs"""
        basic_info_labels = PromoDetailLabels.basic_info_labels

        origin_financial_info_labels = PromoDetailLabels.financial_info_labels

        template_id = utils.get_existed_template(self.driver, self.promo_id)
        self.driver.get(
            '{}promo-detail/{}'.format(self.base_url, template_id))

        promo_detail_page = PromoDetailPage(self.driver)
        promo_detail_page.wait_spiner_loading()
        with self.subTest('Header'):
            self.assertTrue(promo_detail_page.is_element_present(promo_detail_page.back_button),
                            '"Back" button is invisible')
            self.assertTrue(promo_detail_page.is_element_present(promo_detail_page.save_button),
                            '"Save" button is invisible')
            self.assertTrue(promo_detail_page.is_element_present(promo_detail_page.cancel_template_button),
                            '"Cancel" button is invisible')
            self.assertTrue(promo_detail_page.is_element_present(promo_detail_page.create_promo_button),
                            '"Create promo" button is invisible')
            self.assertFalse(promo_detail_page.is_button_disabled(promo_detail_page.back_button, 'Back'),
                             '"Back" button should be active')
            self.assertTrue(promo_detail_page.is_button_disabled(promo_detail_page.save_button, 'Save'),
                            '"Save" button should be disabled')
            self.assertFalse(
                promo_detail_page.is_button_disabled(promo_detail_page.cancel_template_button, 'Cancel template'),
                '"Cancel template" button should be active')
            self.assertFalse(
                promo_detail_page.is_button_disabled(promo_detail_page.create_promo_button, 'Create promo'),
                '"Create promo" button should be active')

            self.assertEqual(promo_detail_page.get_title_from_toolbar(), 'Detail akce', '"Promo detail" title is wrong')
        with self.subTest('Tabs'):
            self.assertEqual('Detail akce', promo_detail_page.get_promo_detail_tab().text,
                             '"Promo deatil" text on tab is wrong')
            self.assertEqual('Dodatečné informace', promo_detail_page.get_additional_info_tab().text,
                             '"Additional info" text on tab is wrong')
        basic_info = BasicInformation(self.driver)

        with self.subTest('Basic information'):
            data_list = utils.get_promo_type_info_from_database(driver=self.driver, promo_id=self.promo_id,
                                                                template_id=template_id)

            self.assertEqual('Základní informace', basic_info.get_title_text(), 'Wrong title for "Basic information"')
            labels_list = basic_info.get_all_labels_text()
            for i in range(len(labels_list)):
                self.assertEqual(basic_info_labels[i], labels_list[i], 'Wrong translation for Basic info labels')

            self.assertTrue(basic_info.is_input_disabled(basic_info.code_input), '"Code" input should be disabled')
            self.assertTrue(basic_info.is_input_disabled(basic_info.external_code_input),
                            '"External code" input should be disabled')
            self.assertEqual('', basic_info.get_input_text(basic_info.external_code_input),
                             'By default External code in template should be empty')
            self.assertFalse(basic_info.is_input_disabled(basic_info.name_input), '"Name" input is disabled')
            self.assertTrue(basic_info.is_field_required(basic_info.name_input), '"Name" input should be required')
            self.assertEqual(data_list['key for promotion name'], basic_info.get_input_text(basic_info.name_input),
                             '"Name" in template does not coincide with Promo type data')
            self.assertTrue(basic_info.is_input_disabled(basic_info.promo_type_input),
                            '"Type" input should be disabled')
            self.assertEqual(data_list['name'], basic_info.get_input_text(basic_info.promo_type_input),
                             '"Type" in template does not coincide with Promo type data')
            self.assertFalse(basic_info.is_dropdown_disabled(basic_info.promo_kind_input),
                             '"Promo kind" dropdown is disabled')
            self.assertIn(basic_info.get_dropdown_value_text(basic_info.promo_kind_input), data_list['promo kind'],
                          '"promo kind" in template does not coincide with Promo type data')
            self.assertFalse(basic_info.is_input_disabled(basic_info.validity_from_input),
                             '"Validity from" input is disabled')
            self.assertFalse(basic_info.is_input_disabled(basic_info.validity_to_input),
                             '"Validity to" input is disabled')
            self.assertFalse(basic_info.is_input_disabled(basic_info.description_input),
                             '"Description" input is disabled')
            self.assertEqual('', basic_info.get_input_text(basic_info.description_input),
                             'By default Description in template should be empty')
            self.assertTrue(basic_info.is_input_disabled(basic_info.status_input), '"Status" input should be disabled')
            self.assertIn('Template', basic_info.get_input_text(basic_info.status_input),
                          'Wrong status for Template')
            self.assertTrue(basic_info.is_input_disabled(basic_info.deadline_input),
                            '"Deadline" input should be disabled')
            self.assertTrue(basic_info.is_checkbox_disabled(basic_info.confirm_checkbox),
                            '"Confirm" checkbox should be disabled')
            self.assertFalse(basic_info.is_note_existed(), 'There are some notes on creating new promo detail')
            self.assertFalse(basic_info.is_tag_existed(), 'There are some tags on creating new promo detail')

        with self.subTest('Financial information'):
            financial_info = FinancialInformation(self.driver)
            self.assertEqual('Rozpočet', financial_info.get_title_text(),
                             'Wrong title for "Financial Information" widget')
            self.assertTrue(financial_info.is_element_present(financial_info.main_headers_table),
                            'There are no table headers in "Financial information" widget')
            self.assertTrue(financial_info.is_element_present(financial_info.main_content_table),
                            'There are no table content in "Financial information" widget')

            real_financial_info_labels = financial_info.get_all_tables_labels()
            for i in range(len(origin_financial_info_labels)):
                self.assertEqual(origin_financial_info_labels[i], real_financial_info_labels[i],
                                 'Wrong translation for labels in Financial information table')

        with self.subTest('Pages view'):
            pages_view = PagesViewWidget(self.driver)
            self.assertEqual('Přehled stránek', pages_view.get_title_text(), 'Wrong title for "Pages view" widget')
            self.assertTrue(pages_view.is_element_present(pages_view.new_page_button), '"New page" button is absent')
            self.assertTrue(pages_view.is_element_present(pages_view.delete_button), '"Delete" button is absent')

            self.assertFalse(pages_view.is_button_disabled(pages_view.new_page_button, 'New page'),
                             '"New page" button should be active')
            self.assertTrue(pages_view.is_button_disabled(pages_view.delete_button, 'Delete'),
                            '"Delete" button should be disabled')
            self.assertTrue(pages_view.is_element_present(pages_view.main_headers_table),
                            'There are no table headers in "Pages view" widget')
            self.assertTrue(pages_view.is_element_present(pages_view.main_content_table),
                            'There are no table content in "Pages view" widget')

        with self.subTest('Departments view'):
            departments_view = DepartmentViewWidget(self.driver)
            self.assertEqual('Přehled oddělení', departments_view.get_title_text(),
                             'Wrong title for "Departments view" widget')
            self.assertTrue(departments_view.is_element_present(departments_view.main_headers_table),
                            'There are no table headers in "Departments view" widget')
            self.assertTrue(departments_view.is_element_present(departments_view.main_content_table),
                            'There are no table content in "Departments view" widget')

        with self.subTest('Compared promo'):
            compared_promo = ComparedPromoWidget(self.driver)
            self.assertEqual('Porovnávaná akce', compared_promo.get_title_text(),
                             'Wrong title for "Compared promo" widget')
            self.assertTrue(compared_promo.is_element_present(compared_promo.add_compared_action_button),
                            '"Add compared action" button is absent')
            self.assertTrue(compared_promo.is_element_present(compared_promo.delete_button),
                            '"Delete" button is absent')
            self.assertFalse(
                compared_promo.is_button_disabled(compared_promo.add_compared_action_button, 'Add compared promo'),
                '"Add compared promo" button should be active')
            self.assertTrue(compared_promo.is_button_disabled(compared_promo.delete_button, 'Delete'),
                            '"Delete" button should be disabled')
            self.assertTrue(compared_promo.is_element_present(compared_promo.main_headers_table),
                            'There are no table headers in "Compared promo" widget')
            self.assertTrue(compared_promo.is_element_present(compared_promo.main_content_table),
                            'There are no table content in "Compared promo" widget')

        promo_detail_page.click_additional_info()
        additional_info = NewPromoTypePage(self.driver)
        with self.subTest('Additional info'):
            self.assertTrue(additional_info.is_dropdown_disabled(additional_info.validity_input),
                            '"Validity" dropdown should be disabled')
            self.assertTrue(additional_info.is_input_disabled(additional_info.number_validy_input),
                            '"Validity number" input should be disabled')
            self.assertTrue(additional_info.is_dropdown_disabled(additional_info.start_date_validy_input),
                            '"Start date (day of week)" dropdown should be disabled')
            self.assertTrue(additional_info.is_dropdown_disabled(additional_info.date_validy_input),
                            '"Date" dropdown should be disabled')
            self.assertTrue(additional_info.is_dropdown_disabled(additional_info.range_input),
                            '"Range" dropdown should be disabled')
            self.assertTrue(additional_info.is_input_disabled(additional_info.number_range_input),
                            '"Range Number" input should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.setting_targets),
                            '"Setting targets (KPI)" checkbox should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.split_KPI_per_pages),
                            '"Split KPI per pages" checkbox should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.parametrs_split_input),
                            '"Parameters" multiselect should be disabled')
            self.assertTrue(additional_info.is_assortment_from_additional_info_disabled(),
                            '"Assortment" multiselect should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.one_supplier),
                            '"One supplier" checkbox should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.only_goods),
                            '"Only goods in stock" checkbox should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.order_planning),
                            '"Order planning" checkbox should be disabled')
            self.assertTrue(additional_info.is_dropdown_disabled(additional_info.how_to_order_input),
                            '"How to order" dropdown should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.region_input),
                            '"Region" multiselect should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.supermarket_input),
                            '"Supermarket" multiselect should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.mutation),
                            '"Mutation" checkbox should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.distribution_channel_input),
                            '"Distribution channel" multiselect should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.advertising_channel_input),
                            '"Advertising channel" multiselect should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.print_advertising_input),
                            '"Print advertising" multiselect should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.format_input),
                            '"Format" multiselect should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.distribution_input),
                            '"Distribution" multiselect should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.electronic_version),
                            '"Electronic version" checkbox should be disabled')
            self.assertTrue(additional_info.is_input_disabled(additional_info.external_agency_input),
                            '"External agency" input should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.web_globus),
                            '"Web Globus.cz" checkbox should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.web_shop),
                            '"Web shop" checkbox should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.direct_mail),
                            '"Direct mail" checkbox should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.shelf_labels),
                            '"Shelf labels" checkbox should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.type_of_labels_input),
                            '"Type of labeles" multiselect should be disabled')
            self.assertTrue(additional_info.is_multiselect_disabled(additional_info.pos_support_input),
                            '"POS support" multiselect should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.defined_direct_costs),
                            '"Defined direct costs" checkbox should be disabled')
            self.assertTrue(additional_info.is_checkbox_disabled(additional_info.suppliers_contributions),
                            '"Suppliers contributions" checkbox should be disabled')

    def test_4_transfer_values_from_type_to_template(self):
        """Verify that the values in the promo type match the value in the template, change the value and check if they have moved to an existing template"""
        template_id = utils.get_existed_template(self.driver, self.promo_id)

        for i in range(2):
            data_list = utils.get_promo_type_info_from_database(driver=self.driver, promo_id=self.promo_id,
                                                                template_id=template_id)
            self.driver.get('{}promo-detail/{}'.format(self.base_url, template_id))

            promo_detail_page = PromoDetailPage(self.driver)
            promo_detail_page.wait_spiner_loading()

            promo_detail_page.click_additional_info()
            with self.subTest('Additional info'):
                utils.compare_additional_info_with_type_data(data_list, self.driver,
                                                             'in template does not coincide with Promo type data')

            if i == 0:
                PromoRequest(self.driver).create_update_promo_type(promo_type_id=self.promo_id, name='Something new',
                                                                   template_id=template_id)

    def test_cancel_template(self):
        """Click "Cancel" button two times. First one choose 'No' option, and second one choose 'Yes'. Verify deleting template"""
        old_template_id = utils.get_existed_template(self.driver, self.promo_id)
        self.driver.get('{}promo-detail/{}'.format(self.base_url, old_template_id))
        promo_detail_page = PromoDetailPage(self.driver)
        message = promo_detail_page \
            .click_cancel_template_button() \
            .get_dialog_message()
        with self.subTest():
            self.assertEqual('Opravdu chcete zrušit šablonu?', message,
                             'Wrong message for "Do you really want to cancel the template?"')
        promo_detail_page.click_no_to_pop_up_dialog()
        self.assertEqual('{}promo-detail/{}'.format(self.base_url, old_template_id), self.driver.current_url,
                         'After cancel deleting template, was opened another page {}'.format(self.driver.current_url))
        promo_detail_page.click_cancel_template_button() \
            .click_yes_to_pop_up_dialog() \
            .wait_for_url_contain('promo-type',
                                  'After canceling template was opened {}'.format(self.driver.current_url))
        new_template_id = self.data_base.select_in_list("SELECT templateId "
                                                        "FROM [PromoToolGlobus].[PromoTool].[PromoActionType] "
                                                        "WHERE Id = {}".format(self.promo_id))[0][0]
        if new_template_id is not None:
            self.fail('After canceling a template, template still exist')

    def test_replace_template(self):
        """Replace existed template, verify message, verify new template"""
        old_template_id = utils.get_existed_template(self.driver, self.promo_id)
        self.type_page.click_create_template_button()
        with self.subTest():
            self.assertEqual('Tento typ má šablonu. Chtěli byste ji nahradit?',
                             self.type_page.get_dialog_message('Message text in the dialog pop up is missing after '
                                                               'clicking Create template button'),
                             'Wrong message text for "This type got a template. Would you like to replace it?"')
        self.type_page.click_no_to_pop_up_dialog()
        self.assertEqual('{}promo-type/{}'.format(self.base_url, self.promo_id), self.driver.current_url,
                         'After choose "No" option for replacing template, was opened another page {}'
                         .format(self.driver.current_url))
        self.type_page.click_create_template_button(). \
            click_yes_to_pop_up_dialog(). \
            wait_for_url_contain('promo-detail', 'Promo detail page was not opened after replacing existed template')
        new_template_id = self.data_base.select_in_list("SELECT templateId "
                                                        "FROM [PromoToolGlobus].[PromoTool].[PromoActionType] "
                                                        "WHERE Id = {}".format(self.promo_id))[0][0]
        if old_template_id == new_template_id:
            self.fail('Replaced template has the same id')

    def test_3_pre_set_up_value_for_template(self):
        # TODO datapicker
        """Select range, enter number, create template, verify Pages Views block content"""
        template_id = utils.get_template_id(self.promo_id)
        range_list = ['Article(s)',
                      'Page(s)',
                      'Vaucher(s)'
                      ]
        i = 0
        for range in range_list:
            if template_id is not None:
                PromoRequest(self.driver).remove_template(self.promo_id, template_id)
                self.driver.get(self.base_url + 'promo-type/{0}'.format(self.promo_id))
            range_number = random.randint(1, 10)

            self.type_page.choose_range(range) \
                .wait_spiner_loading() \
                .enter_value(self.type_page.number_range_input, range_number,
                             "Can't enter value in Range number input")
            if i == 0:  # For first time also verify assortment
                self.type_page.choose_assortment_by_index([1, 2])
            self.type_page.click_save_button() \
                .click_create_template_button()
            pages_view_widget = PagesViewWidget(self.driver)
            template_id = utils.get_template_id(self.promo_id)
            if template_id is None:
                raise Exception('New promo template was not created')
            pages_view_table = Table(self.driver, pages_view_widget.get_table_content())
            position_input = pages_view_table.get_row(0)[pages_view_table.get_column_index(pages_view_widget.assortment_header)]
            with self.subTest('Article(s)'):
                if range in 'Article(s)':
                    self.assertEqual(1, pages_view_table.count_rows(),
                                     'For "Article" (Range) on promo detail should be only one page')
                    self.assertEqual(str(range_number), pages_view_table.get_value_from_input(position_input),
                                     'Position number does not math range number is promo type')
            if i == 0:
                with self.subTest("Assortment"):
                    pages_view_widget.choose_assortment(0)
                    self.assertListEqual(pages_view_widget.get_assortment_value(pages_view_table.get_row(0)),
                                         PromoRequest(self.driver).get_assortment(template_id),
                                         "Available assortment in promo template don't corespond with "
                                         "assortment in promo type")
            with self.subTest('Vaucher(s)'):
                if range in 'Vaucher(s)':
                    self.assertEqual(1, pages_view_table.count_rows(),
                                     'For "Vaucher" (Range) on promo detail should be only one page')
                    self.assertEqual(str(range_number), pages_view_table.get_value_from_input(position_input))
            with self.subTest('Page(s)'):
                if range in 'Page(s)':
                    self.assertEqual(range_number, pages_view_table.count_rows(),
                                     'Wrong number of pages in "Pages view" in promo detail page')
            i += 1

    def test_leave_template_without_saving(self):
        template_id = utils.get_existed_template(self.driver, self.promo_id)
        self.driver.get('{}promo-detail/{}'.format(self.base_url, template_id))
        template_page = PromoDetailPage(self.driver)
        template_page.wait_spiner_loading()
        basic_info = BasicInformation(self.driver)
        basic_info.enter_value(basic_info.name_input, 'New Name',
                               'Can not enter value in Name field in Basic information block') \
            .enter_value(basic_info.description_input, 'Some new description',
                         'Can not enter value in Description field in Basic information block')

        left_menu = HomePage(self.driver)
        left_menu.click_promo_type_menuitem()

        self.assertEqual('Všechna neuložená data budou ztracena. Chcete pokračovat?',
                         template_page.get_dialog_message(),
                         'Wrong text for "All unsaved data will be lost. Continue?"')
        template_page.click_no_to_pop_up_dialog()
        self.assertEqual('{}promo-detail/{}'.format(self.base_url, template_id), self.driver.current_url,
                         'After click No option to pop up Unsaved data was opened another page')
        left_menu.click_promo_type_menuitem()
        self.assertEqual('Všechna neuložená data budou ztracena. Chcete pokračovat?',
                         template_page.get_dialog_message(),
                         'Wrong text for "All unsaved data will be lost. Continue?"')
        template_page.click_yes_to_pop_up_dialog()
        template_page.wait_for_url_contain('promo-type',
                                           'After click Yes option to pop up Unsaved data was not opened another page')