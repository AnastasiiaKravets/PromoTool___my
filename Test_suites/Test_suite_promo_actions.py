import time
import unittest
from datetime import date, timedelta

from selenium import webdriver

import utilities
from Pages.promo_detail_page import PromoDetailLabels
from Pages.promo_detail_page.BasicInformationForm import BasicInformation
from Pages.promo_detail_page.FinancialInformationWidget import FinancialInformation
from Pages.promo_detail_page.PromoDetailPage import PromoDetailPage
from Pages.promo_type_page.NewPromoTypePage import NewPromoTypePage
from utilities import utils
from utilities.DataBase import DataBase
from utilities.Parser import Parser
from Pages.promo_detail_page.PagesViewWidget import PagesViewWidget
from Pages.promo_actions_page.PromoActionsPage import PromoActionsPage
from utilities.PromoRequest import PromoRequest

from BaseTest import BaseTest


class PromoActionDetailTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        cls.data_base = DataBase(utilities.DataBase.get_connection_parameters())
        # cls.promo_type_id = utils.add_full_promo_type()

        cls.promo_type_id = 101

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
        # driver.close()
        cls.action_id = 536043

    @classmethod
    def tearDownClass(cls):
        # utils.delete_promo_action(cls.action_id)
        pass

    def setUp(self):
        super().setUp()
        self.driver.get(self.base_url + '404')
        request = PromoRequest(self.driver)
        request.authorization_by_request(login=self.autotest_user['login'],
                                         password=self.autotest_user['password'], language='cs')
        self.driver.get('{}promo-detail/{}'.format(self.base_url, self.action_id))
        self.action_detail_page = PromoDetailPage(self.driver)

    @unittest.expectedFailure  # Add translation
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
        message = ['Platnost typu akce není nastavena',
                   'Platnost typu akce skončila',
                   'Typem akce ještě nezačala']
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
        data_list = utils.get_promo_type_info_from_database_and_request(driver=self.driver, promo_id=self.promo_type_id,
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
            additional_info = NewPromoTypePage(self.driver)
            additional_info.wait_spiner_loading()

            self.assertIn(additional_info.get_dropdown_value_text(additional_info.validity_input),
                          data_list['validity'],
                          '"validity" in action does not coincide with Promo type data')
            self.assertEqual(data_list['validity number'],
                             additional_info.get_input_text(additional_info.number_validy_input),
                             '"validity number" in action does not coincide with Promo type data')
            self.assertIn(additional_info.get_dropdown_value_text(additional_info.start_date_validy_input),
                          data_list['day of week'],
                          '"day of week" in action does not coincide with Promo type data')
            self.assertIn(additional_info.get_dropdown_value_text(additional_info.date_validy_input),
                          data_list['date'],
                          '"date" in action does not coincide with Promo type data')
            self.assertIn(additional_info.get_dropdown_value_text(additional_info.range_input),
                          data_list['range'],
                          '"range" in action does not coincide with Promo type data')
            self.assertEqual(data_list['range number'],
                             additional_info.get_input_text(additional_info.number_range_input),
                             '"range number" in action does not coincide with Promo type data')
            self.assertEqual(data_list['setting targets'],
                             additional_info.get_checkbox_value(additional_info.setting_targets),
                             '"setting targets" in action does not coincide with Promo type data')
            self.assertEqual(data_list['split KPI per pages'],
                             additional_info.get_checkbox_value(additional_info.split_KPI_per_pages),
                             '"split KPI per pages" in action does not coincide with Promo type data')
            for i in range(len(data_list['parameters'])):
                self.assertIn(additional_info.get_multiselect_value_text(additional_info.parametrs_split_input)[i],
                              data_list['parameters'][i],
                              '"parameters" in action does not coincide with Promo type data')
            self.assertListEqual(data_list['assortment'],
                                 additional_info.get_assortment_value_from_additional_info(),
                                 '"assortment" in action does not coincide with Promo type data')
            self.assertEqual(data_list['one supplier'],
                             additional_info.get_checkbox_value(additional_info.one_supplier),
                             '"one supplier" in action does not coincide with Promo type data')
            self.assertEqual(data_list['only goods in stock'],
                             additional_info.get_checkbox_value(additional_info.only_goods),
                             '"only goods in stock" in action does not coincide with Promo type data')
            self.assertEqual(data_list['order planning'],
                             additional_info.get_checkbox_value(additional_info.order_planning),
                             '"order planning" in action does not coincide with Promo type data')
            self.assertIn(additional_info.get_dropdown_value_text(additional_info.how_to_order_input),
                          data_list['how to order'],
                          '"how to order" in action does not coincide with Promo type data')
            for i in range(len(data_list['region'])):
                self.assertIn(additional_info.get_multiselect_value_text(additional_info.region_input)[i],
                              data_list['region'][i],
                              '"region" in action does not coincide with Promo type data')
            for i in range(len(data_list['supermarket'])):
                self.assertIn(data_list['supermarket'][i],
                              additional_info.get_multiselect_value_text(additional_info.supermarket_input)[i],
                              '"supermarket" in action does not coincide with Promo type data')
            self.assertEqual(data_list['mutation'], additional_info.get_checkbox_value(additional_info.mutation),
                             '"mutation" in action does not coincide with Promo type data')
            for i in range(len(data_list['distribution channel'])):
                self.assertIn(additional_info.get_multiselect_value_text(
                    additional_info.distribution_channel_input)[i], data_list['distribution channel'][i],
                              '"distribution channel" in action does not coincide with Promo type data')
            for i in range(len(data_list['advertising channel'])):
                self.assertIn(additional_info.get_multiselect_value_text(
                    additional_info.advertising_channel_input)[i], data_list['advertising channel'][i],
                              '"advertising channel" in action does not coincide with Promo type data')
            for i in range(len(data_list['print advertising'])):
                self.assertIn(additional_info.get_multiselect_value_text(
                    additional_info.print_advertising_input)[i], data_list['print advertising'][i],
                              '"print advertising" in action does not coincide with Promo type data')
            for i in range(len(data_list['format'])):
                self.assertIn(additional_info.get_multiselect_value_text(additional_info.format_input)[i],
                              data_list['format'][i],
                              '"format" in action does not coincide with Promo type data')
            for i in range(len(data_list['distribution'])):
                self.assertIn(additional_info.get_multiselect_value_text(additional_info.distribution_input)[i],
                              data_list['distribution'][i],
                              '"distribution" in action does not coincide with Promo type data')
            self.assertEqual(data_list['electronic version'],
                             additional_info.get_checkbox_value(additional_info.electronic_version),
                             '"electronic version" in action does not coincide with Promo type data')
            self.assertEqual(data_list['external agency'],
                             additional_info.get_input_text(additional_info.external_agency_input),
                             '"external agency" in action does not coincide with Promo type data')
            self.assertEqual(data_list['web globus'],
                             additional_info.get_checkbox_value(additional_info.web_globus),
                             '"web globus" in action does not coincide with Promo type data')
            self.assertEqual(data_list['web shop'], additional_info.get_checkbox_value(additional_info.web_shop),
                             '"web shop" in action does not coincide with Promo type data')
            self.assertEqual(data_list['direct mail'],
                             additional_info.get_checkbox_value(additional_info.direct_mail),
                             '"direct mail" in action does not coincide with Promo type data')
            self.assertEqual(data_list['shelf labels'],
                             additional_info.get_checkbox_value(additional_info.shelf_labels),
                             '"shelf labels" in action does not coincide with Promo type data')
            for i in range(len(data_list['type of labeles'])):
                self.assertIn(additional_info.get_multiselect_value_text(additional_info.type_of_labels_input)[i],
                              data_list['type of labeles'][i],
                              '"type of labeles" in action does not coincide with Promo type data')
            for i in range(len(data_list['POS support'])):
                self.assertIn(additional_info.get_multiselect_value_text(additional_info.pos_support_input)[i],
                              data_list['POS support'][i],
                              '"POS support" in action does not coincide with Promo type data')
            self.assertEqual(data_list['defined direct costs'],
                             additional_info.get_checkbox_value(additional_info.defined_direct_costs),
                             '"defined direct costs" in action does not coincide with Promo type data')
            self.assertEqual(data_list['suppliers contributions'],
                             additional_info.get_checkbox_value(additional_info.suppliers_contributions),
                             '"suppliers contributions" in action does not coincide with Promo type data')
        try:
            utils.delete_promo_action(action_id)
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

            real_financial_info_labels = financial_info.get_all_tables_labels()
            for i in range(len(origin_financial_info_labels)):
                self.assertEqual(origin_financial_info_labels[i], real_financial_info_labels[i],
                                 'Wrong translation for labels in Financial information table')
