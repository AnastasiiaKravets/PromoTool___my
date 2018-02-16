import time

from datetime import date, timedelta

from selenium import webdriver

import utilities
from Pages.home_page.HomePage import HomePage
from Pages.promo_detail_page import PromoDetailLabels
from Pages.promo_detail_page.BasicInformationForm import BasicInformation
from Pages.promo_detail_page.ComparedGroupOfPromoWidget import ComparedGroupOfPromoWidget
from Pages.promo_detail_page.ComparedPromoWidget import ComparedPromoWidget
from Pages.promo_detail_page.DepartmentsViewWidget import DepartmentViewWidget
from Pages.promo_detail_page.FinancialGroupsOfPromotionsWidget import GroupsOfPromotions
from Pages.promo_detail_page.FinancialInformationWidget import FinancialInformation
from Pages.promo_detail_page.PromoDetailPage import PromoDetailPage
from Pages.promo_detail_page.WorkflowWidget import WorkflowWidget
from Pages.promo_type_page.NewPromoTypePage import NewPromoTypePage
from utilities import utils
from utilities.DataBase import DataBase
from Pages.promo_detail_page.PagesViewWidget import PagesViewWidget
from utilities.PromoRequest import PromoRequest

from BaseTest import BaseTest
from utilities.Table import Table


class PromoActionDetailTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        cls.data_base = DataBase(utilities.DataBase.get_connection_parameters())
        # cls.promo_type_id = utils.add_full_promo_type()
        # print('Promo type id ' + str(cls.promo_type_id))
        # if cls.browser == 'Chrome':
        #     driver = webdriver.Chrome(executable_path='c:\Program Files (x86)\SeleniumDriver\chromedriver.exe')
        # if cls.browser == "IE":
        #     driver = webdriver.Ie('c:\Program Files (x86)\SeleniumDriver\IEDriverServer_32.exe')
        #
        # driver.get(cls.base_url + '404')
        # cls.request = PromoRequest(driver)
        # cls.request.authorization_by_request(login=cls.autotest_user['login'],
        #                                  password=cls.autotest_user['password'], language='cs')
        # cls.action_id = cls.request.create_promo_action(cls.promo_type_id)
        # print('Action id ' + str(cls.action_id))
        # driver.close()

        cls.action_id = 537438
        cls.promo_type_id = 1272

    @classmethod
    def tearDownClass(cls):
        # utils.delete_promo_action(cls.action_id)
        # utils.delete_promo_type(cls.promo_type_id)
        pass

    def setUp(self):
        super().setUp()
        self.driver.get(self.base_url + '404')
        self.request = PromoRequest(self.driver)
        self.request.authorization_by_request(login=self.autotest_user['login'],
                                              password=self.autotest_user['password'], language='cs')
        self.driver.get('{}promo-detail/{}'.format(self.base_url, self.action_id))
        self.action_detail_page = PromoDetailPage(self.driver)

    def test_validity_message(self):
        """Try to create action with expired, not set or has not started validity"""
        self.driver.get('{}promo-type/{}'.format(self.base_url, self.promo_type_id))

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

        for i in range(3):
            if i == 0:
                self.data_base.execute("UPDATE [PromoToolGlobus].[PromoTool].[PromoActionType] "
                                       "SET ValidFrom = NULL, ValidTo = NULL, templateId = NULL "
                                       "WHERE Id={}".format(self.promo_type_id))
            else:
                self.data_base.execute("UPDATE [PromoToolGlobus].[PromoTool].[PromoActionType] "
                                       "SET ValidFrom = '{}', ValidTo = '{}' "
                                       "WHERE Id={}".format(valid_from[i], valid_to[i], self.promo_type_id))
            self.driver.refresh()
            type_page = NewPromoTypePage(self.driver)
            type_page.wait_spiner_loading() \
                .click_new_promo_button()
            with self.subTest(subtest_name[i]):
                self.assertEqual(message[i], type_page.get_dialog_message(),
                                 assertion_error[i])
            type_page.click_ok_to_pop_up_dialog()

    def test_unsaved_data_pop_up(self):
        self.action_detail_page.wait_spiner_loading()

        basic_info = BasicInformation(self.driver)
        basic_info.enter_value(basic_info.name_input, 'New Name',
                               'Can not enter value in Name field in Basic information block') \
            .enter_value(basic_info.description_input, 'Some new description',
                         'Can not enter value in Description field in Basic information block')

        left_menu = HomePage(self.driver)
        left_menu.click_promo_type_menuitem()

        self.assertEqual('Všechna neuložená data budou ztracena. Chcete pokračovat?',
                         self.action_detail_page.get_dialog_message(),
                         'Wrong text for "All unsaved data will be lost. Continue?"')
        self.action_detail_page.click_no_to_pop_up_dialog()
        self.assertEqual('{}promo-detail/{}'.format(self.base_url, self.action_id), self.driver.current_url,
                         'After click No option to pop up Unsaved data was opened another page')
        left_menu.click_promo_type_menuitem()
        self.assertEqual('Všechna neuložená data budou ztracena. Chcete pokračovat?',
                         self.action_detail_page.get_dialog_message(),
                         'Wrong text for "All unsaved data will be lost. Continue?"')
        self.action_detail_page.click_yes_to_pop_up_dialog()
        self.action_detail_page.wait_for_url_contain('promo-type',
                                                     'After click Yes option to pop up Unsaved data was not opened another page')

    def test_create_promo_action_from_promo_type(self):
        """Go to promo type page. Click New promo. Verify action was created, transfer data to additional info tab"""
        self.driver.get('{}promo-type/{}'.format(self.base_url, self.promo_type_id))
        type_page = NewPromoTypePage(self.driver)
        action_detail_page = type_page.click_new_promo_button()
        type_page.wait_for_url_contain('{}promo-detail/'.format(self.base_url),
                                       'Promo detail page was not loaded after creating new promo page')
        action_id = self.driver.current_url.split('promo-detail/')[1]
        print('-----------------{}-------------------'.format(action_id))

        action_detail_page.wait_spiner_loading()
        data_list = utils.get_promo_type_info_from_database(driver=self.driver, promo_id=self.promo_type_id,
                                                            template_id=action_id)

        with self.subTest('Basic info block'):
            basic_info_block = BasicInformation(self.driver)
            self.assertIn('Nová', basic_info_block.get_input_text(basic_info_block.status_input),
                          'Status for action should be "New"')
            self.assertEqual(data_list['name'], basic_info_block.get_input_text(basic_info_block.promo_type_input),
                             '"Type" in action does not coincide with Promo type data')
            self.assertIn(basic_info_block.get_dropdown_value_text(basic_info_block.promo_kind_input),
                          data_list['promo kind'],
                          '"Promo kind" in action does not coincide with Promo type data')
            self.assertEqual(data_list['key for promotion name'],
                             basic_info_block.get_input_text(basic_info_block.name_input),
                             '"Name" in action does not coincide with Promo type data')

        with self.subTest('Additional info'):
            action_detail_page.click_additional_info()
            utils.compare_additional_info_with_type_data(data_list, self.driver,
                                                         'in action does not coincide with Promo type data')
        try:
            self.request.delete_promo_action(action_id)
        except:
            print('Action with id {} was not deleted'.format(action_id))

    def test_create_promo_action_from_template(self):
        promo_id = 1
        action_id = None
        template_id = utils.get_existed_template(self.driver, promo_id)

        self.open_url('promo-detail/{}'.format(template_id))
        template_page = PromoDetailPage(self.driver)

        template_basic_info = BasicInformation(self.driver)
        template_basic_info_value = {
            'name': template_basic_info.get_input_text(template_basic_info.name_input,
                                                       'Name input is absent in template'),
            'type': template_basic_info.get_input_text(template_basic_info.promo_type_input,
                                                       'Promo type input is absent in template'),
            'description': template_basic_info.get_input_text(template_basic_info.description_input,
                                                              'Description input is absent in template'),
            'external code': template_basic_info.get_input_text(template_basic_info.external_code_input,
                                                                'External code input is absent in template'),
            'promo kind': template_basic_info.get_dropdown_value_text(template_basic_info.promo_kind_input,
                                                                      'Promo kind dropdown is absent in template')
        }
        template_financial_info = FinancialInformation(self.driver)
        template_financial_info_value = {
            'turnover': template_financial_info.get_plan_value(template_financial_info.turnover_row),
            'title page': template_financial_info.get_plan_value(template_financial_info.title_page_row),
            'margin': template_financial_info.get_plan_value(template_financial_info.margin_row),
            'gross profit': template_financial_info.get_plan_value(template_financial_info.gross_profit_row),
            'suppliers contribution': template_financial_info.get_plan_value(
                template_financial_info.suppliers_contribution_row),
            'total gross profit': template_financial_info.get_plan_value(
                template_financial_info.total_gross_profit_row),
        }

        try:
            action_detail = template_page.wait_spiner_loading()\
                .create_promo()
            action_id = self.driver.current_url.split('promo-detail/')[1]
            print('-----------------{}-------------------'.format(action_id))
            action_basic_info = BasicInformation(self.driver)
            action_basic_info_value = {
                'name': action_basic_info.get_input_text(action_basic_info.name_input,
                                                           'Name input is absent in template'),
                'type': action_basic_info.get_input_text(action_basic_info.promo_type_input,
                                                           'Promo type input is absent in template'),
                'description': action_basic_info.get_input_text(action_basic_info.description_input,
                                                                  'Description input is absent in template'),
                'external code': action_basic_info.get_input_text(action_basic_info.external_code_input,
                                                                    'External code input is absent in template'),
                'promo kind': action_basic_info.get_dropdown_value_text(action_basic_info.promo_kind_input,
                                                                          'Promo kind dropdown is absent in template')
            }
            action_financial_info = FinancialInformation(self.driver)
            action_financial_info_value = {
                'turnover': action_financial_info.get_plan_value(action_financial_info.turnover_row),
                'title page': action_financial_info.get_plan_value(action_financial_info.title_page_row),
                'margin': action_financial_info.get_plan_value(action_financial_info.margin_row),
                'gross profit': action_financial_info.get_plan_value(action_financial_info.gross_profit_row),
                'suppliers contribution': action_financial_info.get_plan_value(
                    action_financial_info.suppliers_contribution_row),
                'total gross profit': action_financial_info.get_plan_value(
                    action_financial_info.total_gross_profit_row),
            }


        except Exception as error:
            raise Exception(error)
        finally:
            if action_id is not None:
                try:
                    self.request.delete_promo_action(action_id)
                except:
                    print('Action with id {} was not deleted'.format(action_id))

    def test_0_default_view_of_promo_action(self):
        """Verify presence of all elements on Promo detail page"""
        self.action_detail_page.wait_spiner_loading()
        with self.subTest('Header'):
            self.assertFalse(self.action_detail_page.is_button_disabled(self.action_detail_page.back_button, 'Back'),
                             '"Back" button should be active')
            self.assertTrue(self.action_detail_page.is_button_disabled(self.action_detail_page.save_button),
                            '"Save" button should be disabled')
            self.assertTrue(self.action_detail_page.is_button_disabled(self.action_detail_page.cancel_promo_button),
                            '"Cancel" button should be disabled')
            self.assertFalse(self.action_detail_page.is_button_disabled(self.action_detail_page.copy_button),
                             '"Copy" button should be active')
            self.assertFalse(self.action_detail_page.is_button_disabled
                             (self.action_detail_page.generate_reservation_button),
                             '"Generate reservation" button should be active')
            self.assertFalse(self.action_detail_page.is_button_disabled(self.action_detail_page.reservations_button),
                             '"Reservation" button should be active')
            self.assertEqual(self.action_detail_page.get_title_from_toolbar(), 'Detail akce',
                             '"Promo detail" title is wrong')
        with self.subTest('Tabs'):
            self.assertEqual('Detail akce', self.action_detail_page.get_promo_detail_tab().text,
                             '"Promo deatil" text on tab is wrong')
            self.assertEqual('Dodatečné informace', self.action_detail_page.get_additional_info_tab().text,
                             '"Additional info" text on tab is wrong')

        with self.subTest('Basic information'):
            basic_info = BasicInformation(self.driver)
            self.assertEqual('Základní informace', basic_info.get_title_text(), 'Wrong title for "Basic information"')
            labels_list = basic_info.get_all_labels_text()

            for i in range(len(labels_list) - 1):
                self.assertEqual(PromoDetailLabels.basic_info_labels[i], labels_list[i],
                                 'Wrong translation for Basic info labels')
            self.assertTrue(basic_info.is_input_disabled(basic_info.code_input), '"Code" input should be disabled')
            self.assertFalse(basic_info.is_input_disabled(basic_info.external_code_input),
                             '"External code" input should be active')
            self.assertEqual('', basic_info.get_input_text(basic_info.external_code_input),
                             'External code in template should be empty')
            self.assertFalse(basic_info.is_input_disabled(basic_info.name_input), '"Name" input is disabled')
            self.assertTrue(basic_info.is_field_required(basic_info.name_input), '"Name" input should be required')
            self.assertTrue(basic_info.is_input_disabled(basic_info.promo_type_input),
                            '"Type" input should be disabled')
            self.assertFalse(basic_info.is_dropdown_disabled(basic_info.promo_kind_input),
                             '"Promo kind" dropdown is disabled')
            self.assertFalse(basic_info.is_input_disabled(basic_info.validity_from_input),
                             '"Validity from" input is disabled')
            self.assertEqual('', basic_info.get_input_text(basic_info.validity_from_input),
                             'By default "Validity from" should be empty')
            self.assertFalse(basic_info.is_input_disabled(basic_info.validity_to_input),
                             '"Validity to" input is disabled')
            self.assertEqual('', basic_info.get_input_text(basic_info.validity_to_input),
                             'By default "Validity to" input should be empty')
            self.assertFalse(basic_info.is_input_disabled(basic_info.description_input),
                             '"Description" input is disabled')
            self.assertEqual('', basic_info.get_input_text(basic_info.description_input),
                             'By default Description should be empty')
            self.assertTrue(basic_info.is_input_disabled(basic_info.status_input), '"Status" input should be disabled')
            self.assertTrue(basic_info.is_input_disabled(basic_info.deadline_input),
                            '"Deadline" input should be disabled')
            self.assertEqual('', basic_info.get_input_text(basic_info.deadline_input),
                             'By default Deadline input should be empty')
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
            financial_info_labels = financial_info.get_all_tables_labels()
            for i in range(len(PromoDetailLabels.financial_info_labels)):
                self.assertEqual(PromoDetailLabels.financial_info_labels[i], financial_info_labels[i],
                                 'Wrong translation for labels in Financial information table')
            self.assertEqual('0', financial_info.get_plan_value(financial_info.turnover_row),
                             'Turnover should be 0 by default')
            self.assertEqual('0', financial_info.get_plan_value(financial_info.title_page_row),
                             'Title page only should be 0 by default')
            self.assertEqual('', financial_info.get_plan_value(financial_info.margin_row),
                             'Margin should be 0 by default')
            self.assertEqual('0', financial_info.get_plan_value(financial_info.gross_profit_row),
                             'Gross profit should be 0 by default')
            self.assertEqual('0', financial_info.get_plan_value(financial_info.suppliers_contribution_row),
                             'Suppliers contribution should be 0 by default')
            self.assertEqual('0', financial_info.get_plan_value(financial_info.total_gross_profit_row),
                             'Total gross profit should be 0 by default')
            self.assertTrue(financial_info.is_plan_input_disabled(financial_info.total_gross_profit_row))

        with self.subTest('Financial information - Groups of promotions'):
            financial_groups = GroupsOfPromotions(self.driver)
            self.assertEqual('Rozpočet - skupina akcí', financial_groups.get_title_text(),
                             'Wrong title for "Financial Information - Groups of promotions" widget')
            self.assertTrue(financial_groups.is_element_present(financial_groups.main_headers_table),
                            'There are no table headers in "Financial information" widget')
            self.assertTrue(financial_groups.is_element_present(financial_groups.main_content_table),
                            'There are no table content in "Financial information" widget')
            financial_info_labels = financial_groups.get_all_tables_labels()
            for i in range(len(PromoDetailLabels.financial_info_labels)):
                self.assertEqual(PromoDetailLabels.financial_info_labels[i], financial_info_labels[i],
                                 'Wrong translation for labels in "Financial Information - Groups of promotions" table')
            self.assertTrue(financial_groups.are_plan_inputs_disabled())

        with self.subTest('Workflow'):
            workflow = WorkflowWidget(self.driver)
            self.assertEqual('Workflow', workflow.get_title_text(),
                             'Wrong title for "Workflow" widget')
            self.assertTrue(workflow.is_element_present(workflow.main_headers_table),
                            'There are no table headers in "Workflow" widget')

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
            self.assertTrue(pages_view.is_element_present(pages_view.main_footer_table),
                            'There are no footer table in "Pages view" widget')

        with self.subTest('Departments view'):
            departments_view = DepartmentViewWidget(self.driver)
            self.assertEqual('Přehled oddělení', departments_view.get_title_text(),
                             'Wrong title for "Departments view" widget')
            self.assertTrue(departments_view.is_element_present(departments_view.main_headers_table),
                            'There are no table headers in "Departments view" widget')
            self.assertTrue(departments_view.is_element_present(departments_view.main_content_table),
                            'There are no table content in "Departments view" widget')
            self.assertTrue(departments_view.is_element_present(departments_view.main_footer_table),
                            'There are no footer table in "Departments view" widget')

        with self.subTest('Compared promo'):
            compared_promo = ComparedPromoWidget(self.driver)
            self.assertEqual('Porovnávaná akce', compared_promo.get_title_text(),
                             'Wrong title for "Compared promo" widget')
            self.assertFalse(
                compared_promo.is_button_disabled(compared_promo.add_compared_action_button, 'Add compared promo'),
                '"Add compared promo" button should be active')
            self.assertTrue(compared_promo.is_button_disabled(compared_promo.delete_button, 'Delete'),
                            '"Delete" button should be disabled')
            self.assertTrue(compared_promo.is_element_present(compared_promo.main_headers_table),
                            'There are no table headers in "Compared promo" widget')
            self.assertTrue(compared_promo.is_element_present(compared_promo.main_content_table),
                            'There are no table content in "Compared promo" widget')

        with self.subTest('Compared group of promo'):
            compared_group_promo = ComparedGroupOfPromoWidget(self.driver)
            self.assertEqual('Skupina porovnávaných akcí', compared_group_promo.get_title_text(),
                             'Wrong title for "Compared group of promo" widget')
            self.assertFalse(compared_group_promo.is_button_disabled
                             (compared_group_promo.add_compared_group_button, 'Add compared group'),
                             '"Add compared group" button should be active')
            self.assertTrue(compared_group_promo.is_button_disabled(compared_group_promo.delete_button, 'Delete'),
                            '"Delete" button should be disabled')
            self.assertTrue(compared_group_promo.is_element_present(compared_group_promo.main_headers_table),
                            'There are no table headers in "Compared group of promo" widget')
            self.assertTrue(compared_group_promo.is_element_present(compared_group_promo.main_content_table),
                            'There are no table content in "Compared group of promo" widget')

        self.action_detail_page.click_additional_info()
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
            self.assertFalse(additional_info.is_dropdown_disabled(additional_info.range_input),
                             '"Range" dropdown should be active')
            self.assertFalse(additional_info.is_input_disabled(additional_info.number_range_input),
                             '"Range Number" input should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.setting_targets),
                             '"Setting targets (KPI)" checkbox should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.split_KPI_per_pages),
                             '"Split KPI per pages" checkbox should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.parametrs_split_input),
                             '"Parameters" multiselect should be active')
            self.assertFalse(additional_info.is_assortment_from_additional_info_disabled(),
                             '"Assortment" multiselect should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.one_supplier),
                             '"One supplier" checkbox should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.only_goods),
                             '"Only goods in stock" checkbox should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.order_planning),
                             '"Order planning" checkbox should be active')
            self.assertFalse(additional_info.is_dropdown_disabled(additional_info.how_to_order_input),
                             '"How to order" dropdown should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.region_input),
                             '"Region" multiselect should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.supermarket_input),
                             '"Supermarket" multiselect should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.mutation),
                             '"Mutation" checkbox should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.distribution_channel_input),
                             '"Distribution channel" multiselect should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.advertising_channel_input),
                             '"Advertising channel" multiselect should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.print_advertising_input),
                             '"Print advertising" multiselect should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.format_input),
                             '"Format" multiselect should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.distribution_input),
                             '"Distribution" multiselect should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.electronic_version),
                             '"Electronic version" checkbox should be active')
            self.assertFalse(additional_info.is_input_disabled(additional_info.external_agency_input),
                             '"External agency" input should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.web_globus),
                             '"Web Globus.cz" checkbox should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.web_shop),
                             '"Web shop" checkbox should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.direct_mail),
                             '"Direct mail" checkbox should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.shelf_labels),
                             '"Shelf labels" checkbox should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.type_of_labels_input),
                             '"Type of labeles" multiselect should be active')
            self.assertFalse(additional_info.is_multiselect_disabled(additional_info.pos_support_input),
                             '"POS support" multiselect should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.defined_direct_costs),
                             '"Defined direct costs" checkbox should be active')
            self.assertFalse(additional_info.is_checkbox_disabled(additional_info.suppliers_contributions),
                             '"Suppliers contributions" checkbox should be active')

    def test_1_edit_additional_info(self):
        """Make some changes in additional info, save it, verify value was changed"""
        range = 'Vaucher(s)'
        range_number = 10
        how_to_order = 'cross-dock'
        external_agency = 'New External agency'

        self.action_detail_page.wait_spiner_loading()
        self.action_detail_page.click_additional_info()
        new_promo_page = NewPromoTypePage(self.driver)

        new_promo_page.choose_range(range) \
            .wait_spiner_loading() \
            .enter_value(new_promo_page.number_range_input, range_number,
                         '"Number" input from Range disabled after choosing "Range" option') \
            .uncheck_element(new_promo_page.setting_targets, 'Setting targets (KPI)') \
            .uncheck_element(new_promo_page.split_KPI_per_pages, 'Split KPI per pages') \
            .wait_spiner_loading()
        self.assertTrue(new_promo_page.is_multiselect_disabled(new_promo_page.parametrs_split_input),
                        '"Parameters" multiselect active after uncheck "Split KPI per pages"')
        new_promo_page.uncheck_element(new_promo_page.only_goods, 'Only goods in stock') \
            .uncheck_element(new_promo_page.order_planning, 'Order planning') \
            .choose_how_to_order(how_to_order) \
            .uncheck_element(new_promo_page.mutation, 'Mutation') \
            .enter_value(new_promo_page.external_agency_input, external_agency, '"External agency" is non-interactive') \
            .uncheck_element(new_promo_page.shelf_labels, 'Shelf labels') \
            .wait_spiner_loading()
        self.assertTrue(new_promo_page.is_multiselect_disabled(new_promo_page.type_of_labels_input),
                        '"Type of labeles" still be active after checking "Shelf labels"')
        new_promo_page.click_save_button()

        self.driver.refresh()
        self.action_detail_page.wait_spiner_loading()
        self.action_detail_page.click_additional_info()

        self.assertEqual(str(range_number), new_promo_page.get_input_text(new_promo_page.number_range_input),
                         'Wrong value for "Number" input from Range after saving')
        self.assertFalse(new_promo_page.get_checkbox_value(new_promo_page.setting_targets),
                         'Wrong value for "Setting targets (KPI)" after saving')
        self.assertFalse(new_promo_page.get_checkbox_value(new_promo_page.split_KPI_per_pages),
                         'Wrong value for "Split KPI per pages" after saving')
        self.assertFalse(new_promo_page.get_checkbox_value(new_promo_page.only_goods),
                         'Wrong value for "Only goods in stock" after saving')
        self.assertFalse(new_promo_page.get_checkbox_value(new_promo_page.order_planning),
                         'Wrong value for "Order planning" after saving')
        self.assertFalse(new_promo_page.get_checkbox_value(new_promo_page.mutation),
                         'Wrong value for "Mutation" after saving')
        self.assertEqual(external_agency, new_promo_page.get_input_text(new_promo_page.external_agency_input),
                         'Wrong value for "External agency" after saving')
        self.assertIn(how_to_order, new_promo_page.get_dropdown_value_text(new_promo_page.how_to_order_input),
                      'Wrong value for "How to order" after saving')

    def test_edit_basic_info(self):
        self.assertTrue(self.action_detail_page.is_button_disabled(self.action_detail_page.save_button),
                        'Save button is active without any changes')
        basic_info = BasicInformation(self.driver)

        valid_from = (date.today() + timedelta(days=3)).strftime('%d%m%Y')
        valid_to = (date.today() - timedelta(days=10)).strftime('%d%m%Y')

        basic_info.enter_value(basic_info.validity_from_input, valid_from, 'Validity from input is non editable') \
            .enter_value(basic_info.validity_to_input, valid_to, 'Validity from input is non editable')

        print(basic_info.get_notification_required_field_text(basic_info.validity_from_input))
        print(basic_info.get_notification_required_field_text(basic_info.validity_to_input))
        # TODO

    def test_canceled_action_view(self):
        """Verify disabled state of all elements for canceled action"""

        canceled_action_id = utils.get_canceled_action_id()
        self.driver.get('{}promo-detail/{}'.format(self.base_url, canceled_action_id))
        self.action_detail_page.wait_spiner_loading()
        with self.subTest('Header'):
            self.assertFalse(self.action_detail_page.is_button_disabled(self.action_detail_page.back_button, 'Back'),
                             '"Back" button should be active')
            self.assertTrue(self.action_detail_page.is_button_disabled(self.action_detail_page.save_button, 'Save'),
                            '"Save" button should be disabled')
            self.assertTrue(self.action_detail_page.is_element_absent(self.action_detail_page.cancel_promo_button),
                            '"Cancel" button should not be present')
            self.assertTrue(self.action_detail_page.is_element_absent(self.action_detail_page.copy_button),
                            '"Copy" button should not be present')
            self.assertTrue(
                self.action_detail_page.is_element_absent(self.action_detail_page.generate_reservation_button),
                '"Generate reservation" button should not be present')
            self.assertFalse(self.action_detail_page.is_button_disabled(self.action_detail_page.reservations_button),
                             '"Reservation" button should be active')
            self.assertFalse(self.action_detail_page.is_button_disabled(self.action_detail_page.restart_promo_button,
                                                                        'Restart'), '"Restart" button should be active')
        with self.subTest('Basic information'):
            basic_info = BasicInformation(self.driver)

            self.assertTrue(basic_info.is_input_disabled(basic_info.code_input), '"Code" input should be disabled')
            self.assertTrue(basic_info.is_input_disabled(basic_info.external_code_input),
                            '"External code" input should be disabled')
            self.assertTrue(basic_info.is_input_disabled(basic_info.name_input), '"Name" input should be disabled')
            self.assertTrue(basic_info.is_input_disabled(basic_info.promo_type_input),
                            '"Type" input should be disabled')
            self.assertTrue(basic_info.is_dropdown_disabled(basic_info.promo_kind_input),
                            '"Promo kind" dropdown should be disabled')
            self.assertTrue(basic_info.is_multiselect_disabled(basic_info.validity_from_input),
                            '"Validity from" input should be disabled')
            self.assertTrue(basic_info.is_multiselect_disabled(basic_info.validity_to_input),
                            '"Validity to" input should be disabled')
            self.assertTrue(basic_info.is_input_disabled(basic_info.description_input),
                            '"Description" input should be disabled')
            self.assertTrue(basic_info.is_input_disabled(basic_info.status_input), '"Status" input should be disabled')
            self.assertTrue(basic_info.is_input_disabled(basic_info.deadline_input),
                            '"Deadline" input should be disabled')
            self.assertTrue(basic_info.is_checkbox_disabled(basic_info.confirm_checkbox),
                            '"Confirm" checkbox should be disabled')

        with self.subTest('Financial information'):
            financial_info = FinancialInformation(self.driver)
            table = Table(self.driver, financial_info.get_table_content())
            second_cell = 1

            self.assertFalse(table.is_input_in_cell(table.get_row(financial_info.turnover_row)[second_cell]),
                             'There should not be input in financial info')
            self.assertFalse(table.is_input_in_cell(table.get_row(financial_info.title_page_row)[second_cell]),
                             'There should not be input in financial info')
            self.assertFalse(table.is_input_in_cell(table.get_row(financial_info.margin_row)[second_cell]),
                             'There should not be input in financial info')
            self.assertFalse(table.is_input_in_cell(table.get_row(financial_info.gross_profit_row)[second_cell]),
                             'There should not be input in financial info')
            self.assertFalse(
                table.is_input_in_cell(table.get_row(financial_info.suppliers_contribution_row)[second_cell]),
                'There should not be input in financial info')
            self.assertFalse(table.is_input_in_cell(table.get_row(financial_info.total_gross_profit_row)[second_cell]),
                             'There should not be input in financial info')

        with self.subTest('Financial information - Groups of promotions'):
            financial_groups = GroupsOfPromotions(self.driver)
            self.assertTrue(financial_groups.is_element_present(financial_groups.main_headers_table),
                            'There are no table headers in "Financial information" widget')
            self.assertTrue(financial_groups.are_plan_inputs_disabled())

        with self.subTest('Workflow'):
            workflow = WorkflowWidget(self.driver)
            self.assertTrue(workflow.is_element_present(workflow.main_headers_table),
                            'There are no table headers in "Workflow" widget')

        with self.subTest('Pages view'):
            pages_view = PagesViewWidget(self.driver)
            self.assertTrue(pages_view.is_button_disabled(pages_view.new_page_button, 'New page'),
                            '"New page" button should be disabled')
            self.assertTrue(pages_view.is_button_disabled(pages_view.delete_button, 'Delete'),
                            '"Delete" button should be disabled')
            self.assertTrue(pages_view.is_element_present(pages_view.main_headers_table),
                            'There are no table headers in "Pages view" widget')
            self.assertTrue(pages_view.is_element_present(pages_view.main_footer_table),
                            'There are no footer table in "Pages view" widget')
            # table = Table(self.driver, pages_view.get_table_content())
            # TODO check disabled inputs

        with self.subTest('Departments view'):
            departments_view = DepartmentViewWidget(self.driver)
            self.assertTrue(departments_view.is_element_present(departments_view.main_headers_table),
                            'There are no table headers in "Departments view" widget')
            self.assertTrue(departments_view.is_element_present(departments_view.main_content_table),
                            'There are no table content in "Departments view" widget')
            self.assertTrue(departments_view.is_element_present(departments_view.main_footer_table),
                            'There are no footer table in "Departments view" widget')

        with self.subTest('Compared promo'):
            compared_promo = ComparedPromoWidget(self.driver)
            self.assertTrue(
                compared_promo.is_button_disabled(compared_promo.add_compared_action_button, 'Add compared promo'),
                '"Add compared promo" button should be disabled')
            self.assertTrue(compared_promo.is_button_disabled(compared_promo.delete_button, 'Delete'),
                            '"Delete" button should be disabled')
            self.assertTrue(compared_promo.is_element_present(compared_promo.main_headers_table),
                            'There are no table headers in "Compared promo" widget')
            self.assertTrue(compared_promo.is_element_present(compared_promo.main_content_table),
                            'There are no table content in "Compared promo" widget')

        with self.subTest('Compared group of promo'):
            compared_group_promo = ComparedGroupOfPromoWidget(self.driver)
            self.assertTrue(compared_group_promo.is_button_disabled
                            (compared_group_promo.add_compared_group_button, 'Add compared group'),
                            '"Add compared group" button should be disabled')
            self.assertTrue(compared_group_promo.is_button_disabled(compared_group_promo.delete_button, 'Delete'),
                            '"Delete" button should be disabled')
            self.assertTrue(compared_group_promo.is_element_present(compared_group_promo.main_headers_table),
                            'There are no table headers in "Compared group of promo" widget')
            self.assertTrue(compared_group_promo.is_element_present(compared_group_promo.main_content_table),
                            'There are no table content in "Compared group of promo" widget')

        self.action_detail_page.click_additional_info()
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

    def test_cancel_action(self):
        """There is a possibility to cancel a promo ONLY if the promo is not started yet"""

        valid_from = [(date.today() - timedelta(days=10)).strftime('%Y-%m-%d'),
                      (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')]
        print(valid_from)
        valid_to = (date.today() + timedelta(days=20)).strftime('%Y-%m-%d')

        for i in range(len(valid_from)):
            self.data_base.execute("UPDATE [PromoToolGlobus].[PromoTool].[PromoAction] "
                                   "SET ActiveFrom = '{}', ActiveTo = '{}' "
                                   "WHERE Id = {}".format(valid_from[i], valid_to, self.action_id))
            self.driver.refresh()
            self.action_detail_page.wait_spiner_loading()
            time.sleep(5)

            self.assertTrue(self.action_detail_page.is_button_disabled(self.action_detail_page.cancel_promo_button,
                                                                       'Cancel promo'),
                            'Cancel promo button should be disabled if promo has already started')
            if i == 1:
                self.assertFalse(self.action_detail_page.is_button_disabled(self.action_detail_page.cancel_promo_button,
                                                                            'Cancel promo'),
                                 'Cancel promo button should be active if promo has not already started')
        self.action_detail_page.click_cancel_promo_button().wait_spiner_loading()

        time.sleep(5)
        # TODO
