import time
import unittest
from datetime import date, timedelta
from random import randrange, randint

import utilities
from BaseTest import BaseTest
from Pages.promo_type_page.NewPromoTypePage import NewPromoTypePage
from Pages.promo_type_page.PromoTypePage import PromoTypePage
from utilities.DataBase import DataBase
from utilities.PromoRequest import PromoRequest
from utilities.Table import Table, TableFilter


class PromoTypeTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.driver.get(self.base_url + '404')
        PromoRequest(self.driver).authorization_by_request(login=self.autotest_user['login'],
                                                           password=self.autotest_user['password'], language='cs')
        self.driver.get(self.base_url + 'promo-type')
        self.promo_type_page = PromoTypePage(self.driver)

    def test_verify_presence_of_all_elements_on_PromoType_page(self):
        """Verify presence of title, New Type button, headers, table"""
        with self.subTest():
            self.assertEqual('Typ akce', self.promo_type_page.get_title_text(), 'Promo Type title text is incorrect')
            self.assertEqual('Nový typ', self.promo_type_page.get_new_type_button().text,
                             'New button text is incorrect')
            self.assertTrue(self.promo_type_page.is_table_visible(), 'Table is not visible')
            self.assertEqual('ID', self.promo_type_page.get_header_text(self.promo_type_page.id_header),
                             'ID header text is incorrect')
            self.assertEqual('Název', self.promo_type_page.get_header_text(self.promo_type_page.name_header),
                             'Name header text is incorrect')
            self.assertEqual('Šablona', self.promo_type_page.get_header_text(self.promo_type_page.template_header),
                             'Template header text is incorrect')

    @unittest.skip('Not stable test')
    def test_open_existed_promo_type(self):
        """Randomly open three promo types, checking the matching of name and id in url to the values in the table"""
        new_promo_type_page = NewPromoTypePage(self.driver)
        for i in range(3):
            new_promo_type_page.wait_spiner_loading()
            TableFilter(self.driver).wait_table_to_load(self.promo_type_page.get_table_content())
            table = Table(self.driver, self.promo_type_page.get_table_content())
            row_number = table.count_rows()
            row = table.get_row(randrange(row_number))
            id = row[0].text
            current_url = self.base_url + 'promo-type/' + id
            name = row[1].text
            self.promo_type_page.click_link_from_cell(row[1], 'Promo Type' + name + 'does not open')
            self.assertEqual(current_url, self.driver.current_url, 'Wrong prototype is opened')
            new_promo_type_page.click_back_button() \
                .wait_for_url_contain(self.base_url + 'promo-type')
            self.assertEqual(self.base_url + 'promo-type', self.driver.current_url)

    def test_column_filtering(self):
        """Check/uncheck visibility of every column in header filter"""
        filter = TableFilter(self.driver)
        id_header = self.promo_type_page.get_id_header_element()
        filter.columns_settings(id_header, [self.promo_type_page.template_checkbox, self.promo_type_page.name_checkbox])
        self.assertTrue(filter.is_column_displayed(self.promo_type_page.id_header),
                        'ID column invisible after unchecking Name and Template column')
        self.assertFalse(filter.is_column_displayed(self.promo_type_page.template_header),
                         'Template column still be visible after unchecking column')
        self.assertFalse(filter.is_column_displayed(self.promo_type_page.name_header),
                         'Name column still be visible after unchecking column')
        filter.wait_table_to_load(self.promo_type_page.get_table_content())
        filter.columns_settings(id_header, self.promo_type_page.template_checkbox)

        self.assertTrue(filter.is_column_displayed(self.promo_type_page.id_header),
                        'ID column invisible after unchecking Name and Template column')
        self.assertTrue(filter.is_column_displayed(self.promo_type_page.template_header),
                        'Template column invisible after checking column')
        self.assertFalse(filter.is_column_displayed(self.promo_type_page.name_header),
                         'Name column still be visible after unchecking column')
        filter.wait_table_to_load(self.promo_type_page.get_table_content())
        filter.columns_settings(self.promo_type_page.get_template_header_element(),
                                [self.promo_type_page.name_checkbox, self.promo_type_page.id_checkbox])

        self.assertFalse(filter.is_column_displayed(self.promo_type_page.id_header),
                         'ID column still be visible after unchecking column')
        self.assertTrue(filter.is_column_displayed(self.promo_type_page.template_header),
                        'Template column invisible after checking other column')
        self.assertTrue(filter.is_column_displayed(self.promo_type_page.name_header),
                        'Name column still be invisible after checking column')

    def test_verify_default_view_of_new_promo_type_form(self):
        new_promo_page = self.promo_type_page.click_new_type_button()
        labels_list = ['Název', 'Klíč názvu akce', 'Klíč kódu akce', 'Druh akce', 'Platnost',
                       'Číslo', 'Začátek platnosti (den v týdnu)', 'Datum', 'Rozsah', 'Číslo', 'Stanovení cílů (KPI)',
                       'Dělení KPI na stránkách', 'Parametry', 'Sortiment', 'Jediný dodavatel akce',
                       'Pouze zboží skladem', 'Plánování objednacího množství', 'Způsob objednání',
                       'Regionální platnost', 'Přímý výběr obchodu', 'Mutace', 'Distribuční kanál',
                       'Reklamní kanál', 'Tištěná inzerce', 'Formát', 'Distribuce',
                       'Elektronická verze',
                       'Externí agentura', 'Web Globus.cz', 'Web shop', 'Direct email', 'POS prezentace',
                       'Regálové etikety', 'Typ etiket', 'Podpora POS',
                       'Definované přímé náklady', 'Příspěvky dodavatele', 'Workflow', 'Trvání',
                       'Platnost od', 'Platnost do']
        real_labels = new_promo_page.get_all_labels_text()
        with self.subTest():
            self.assertEqual('Nový akce', new_promo_page.get_title(), 'Title is incorrect')
            self.assertEqual('Zpět', new_promo_page.get_visible_element(new_promo_page.back_button,
                                                                        '"Back" button is not visible').text)
            self.assertEqual('Uložit', new_promo_page.get_visible_element(new_promo_page.save_button,
                                                                          '"Save" button is not visible').text)
            self.assertTrue(new_promo_page.is_button_disabled(new_promo_page.save_button, 'Save'))
            for i in range(len(labels_list)):
                self.assertEqual(labels_list[i], real_labels[i], 'Wrong translation for labels')
            # Necessary field
            self.assertTrue(new_promo_page.is_field_required(new_promo_page.name_input), '"Name" should be required')
            self.assertTrue(new_promo_page.is_field_required(new_promo_page.key_promotion_code_input),
                            '"Key for promotion code" should be required')
            self.assertTrue(new_promo_page.is_supermarket_required(), '"Supermarket" should be required')

            # Disabled inputs
            self.assertFalse(new_promo_page.is_input_disabled(new_promo_page.name_input), '"Name" field is disabled')
            self.assertFalse(new_promo_page.is_input_disabled(new_promo_page.key_promotion_name_input),
                             '"Key for promotion name" field is disabled')
            self.assertFalse(new_promo_page.is_input_disabled(new_promo_page.key_promotion_code_input),
                             '"Key for promotion code" field is disabled')
            self.assertTrue(new_promo_page.is_input_disabled(new_promo_page.number_validy_input),
                            '"Number" field in Validy does not disabled')
            self.assertTrue(new_promo_page.is_input_disabled(new_promo_page.number_range_input),
                            '"Number" field in Range does not disabled')
            self.assertFalse(new_promo_page.is_input_disabled(new_promo_page.external_agency_input),
                             '"External agency" field is disabled')
            self.assertFalse(new_promo_page.is_input_disabled(new_promo_page.duration_input),
                             '"Duration" field is disabled')

            # Disabled dropdowns
            self.assertFalse(new_promo_page.is_dropdown_disabled(new_promo_page.promo_kind_input),
                             '"Promo kind" field is disabled')
            self.assertFalse(new_promo_page.is_dropdown_disabled(new_promo_page.validity_input),
                             '"Validity" field is disabled')
            self.assertFalse(new_promo_page.is_dropdown_disabled(new_promo_page.range_input),
                             '"Range" field is disabled')
            self.assertFalse(new_promo_page.is_dropdown_disabled(new_promo_page.how_to_order_input),
                             '"How to order" field is disabled')
            self.assertFalse(new_promo_page.is_dropdown_disabled(new_promo_page.workflow_input),
                             '"Workflow" field is disabled')
            self.assertTrue(new_promo_page.is_dropdown_disabled(new_promo_page.start_date_validy_input),
                            '"Start date (day of week)" field does not disabled')
            self.assertTrue(new_promo_page.is_dropdown_disabled(new_promo_page.date_validy_input),
                            '"Date" field does not disabled')

            # Presence of checkboxes
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.setting_targets),
                            '"Setting targets (KPI)" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.split_KPI_per_pages),
                            '"Split KPI per pages" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.one_supplier),
                            '"One supplier" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.only_goods),
                            '"Only goods in stock" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.order_planning),
                            '"Order planning" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.mutation), '"Mutation" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.electronic_version),
                            '"Electronic version" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.web_globus),
                            '"Web Globus.cz" field is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.web_shop), '"Web shop" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.direct_mail),
                            '"Direct mail" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.shelf_labels),
                            '"Shelf labels" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.defined_direct_costs),
                            '"Defined direct costs" checkbox is invisible')
            self.assertTrue(new_promo_page.is_element_present(new_promo_page.suppliers_contributions),
                            '"Suppliers contributions" checkbox is invisible')

            # Disabled multiselect
            self.assertTrue(new_promo_page.is_multiselect_disabled(new_promo_page.parametrs_split_input),
                            '"Parameters" field does not disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.assortment_input),
                             '"Assortment" field is disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.region_input),
                             '"Region" field is disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.supermarket_input),
                             '"Supermarket" field is disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.distribution_channel_input),
                             '"Distribution channel" field is disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.advertising_channel_input),
                             '"Advertising channel" field is disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.print_advertising_input),
                             '"Print advertising" field is disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.format_input),
                             '"Format" field is disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.distribution_input),
                             '"Distribution" field is disabled')
            self.assertTrue(new_promo_page.is_multiselect_disabled(new_promo_page.type_of_labels_input),
                            '"Type of labeles" field does not disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.pos_support_input),
                             '"POS support" field is disabled')

            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.validy_from_input),
                             '"Valid from" field is disabled')
            self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.validy_to_input),
                             '"Valid to" field is disabled')

    def test_add_empty_promotype(self):
        """Press Save button without filling fields"""
        data_base = DataBase(utilities.DataBase.get_connection_parameters())
        last_id = data_base.get_last_id('[PromoToolGlobus].[PromoTool].[PromoActionType]')
        new_promo_page = self.promo_type_page.click_new_type_button()\

        self.assertTrue(new_promo_page.is_button_disabled(new_promo_page.save_button, 'Save'),
                        '"Save" button should be disabled')

        self.assertEqual(self.base_url + 'promo-type/0', self.driver.current_url,
                         'Promo type should not save with empty required fields')
        new_id = data_base.get_last_id('[PromoToolGlobus].[PromoTool].[PromoActionType]')
        if not last_id == new_id:
            data_base.execute(
                'DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionTypeToSite] WHERE [PromoActionTypeId]={0}' \
                    .format(new_id))
            data_base.execute(
                'DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionType] WHERE [Id]={0}'.format(new_id))
            raise Exception("Empty New promo type was created")

    def test_add_new_promo_type_with_existed_Name_or_KeyCode(self):
        """Fill in new promo type form with existed Name and Key for promotion code fields"""
        data_base = DataBase(utilities.DataBase.get_connection_parameters())
        last_id = data_base.get_last_id('[PromoToolGlobus].[PromoTool].[PromoActionType]')
        existed_data = data_base.select_in_list(
            'SELECT TOP (1) [Name],[KeyCode] FROM [PromoToolGlobus].[PromoTool].[PromoActionType]')
        name = existed_data[0][0]
        key = existed_data[0][1]

        new_promo_page = self.promo_type_page.click_new_type_button()
        new_promo_page.enter_value(new_promo_page.name_input, name, '"Name" field is non-interactive') \
            .enter_value(new_promo_page.key_promotion_code_input, key,
                         '"Key for promotion code" field is non-interactive') \
            .choose_supermarket() \
            .click_save_button()
        notification_error = new_promo_page.get_all_notification_text()
        if len(notification_error) == 0:
            raise Exception("Missing notification about creating promo type with existed data")
        self.assertEqual('errorPromo action type with the same name or key for promotion code already exists',
                         notification_error[0], 'Wrong notification text')
        # Check if there are unexpected notification
        with self.subTest():
            if len(notification_error) > 1:
                raise Exception(notification_error)
        self.assertEqual(self.base_url + 'promo-type', self.driver.current_url,
                         'After error should be opened Promo Type page')
        new_id = data_base.get_last_id('[PromoToolGlobus].[PromoTool].[PromoActionType]')
        if not last_id == new_id:
            data_base.execute(
                'DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionTypeToSite] WHERE [PromoActionTypeId]={0}'.
                    format(new_id))
            data_base.execute(
                'DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionType] WHERE [Id]={0}'.format(new_id))
            raise Exception("New promo type with existed name was created")


    def test_add_valid_promotype_with_full_form(self):
        """Fill in all fields in new promo type form, choose all available data in multiselect and try to save"""
        name = 'Name for AutoTest' + str(randint(0, 1000))
        key_for_promotion_name = 'Key ;,./!@#$%^&*()_+'
        key_for_promotion_code = 'KeyCode 1234 ;,./!@#$%^&*()_+' + str(randint(0, 1000))
        promo_kind = 'Promo kind 1'
        validity_number = '12'
        start_date = 'Friday'
        date_str = 'First day of quarter'
        range = 'Article(s)'
        how_to_order = 'cross-dock'
        external_agency = 'External agency'
        workflow = 'test_restart'
        duration = '1234'
        valid_from = date.today().strftime('%d%m%Y')
        valid_to = (date.today() + timedelta(days=3)).strftime('%d%m%Y')
        data_base = DataBase(utilities.DataBase.get_connection_parameters())
        last_id = data_base.get_last_id('[PromoToolGlobus].[PromoTool].[PromoActionType]')

        new_promo_page = self.promo_type_page.click_new_type_button()
        new_promo_page.enter_value(new_promo_page.name_input, name, '"Name" is non-interactive') \
            .enter_value(new_promo_page.key_promotion_name_input, key_for_promotion_name,
                         '"Key for promotion name" is non-interactive') \
            .enter_value(new_promo_page.key_promotion_code_input, key_for_promotion_code,
                         '"Key for promotion code" is non-interactive') \
            .choose_promo_kind(promo_kind)

        new_promo_page.choose_validity('Day(s)')
        with self.subTest():
            new_promo_page.wait_spiner_loading()
            self.assertFalse(new_promo_page.is_input_disabled(new_promo_page.number_validy_input),
                             '"Number" input from Validity disabled after choosing option "Day" in Validy')
            self.assertFalse(new_promo_page.is_dropdown_disabled(new_promo_page.start_date_validy_input),
                             '"Start date (day of week)" dropdown disabled after choosing option "Day" in Validy')
        new_promo_page.enter_value(new_promo_page.number_validy_input, validity_number,
                                   '"Number" input is non-interaction') \
            .choose_start_date(start_date)

        new_promo_page.choose_validity('Month(s)')
        with self.subTest():
            new_promo_page.wait_spiner_loading()
            self.assertTrue(new_promo_page.is_input_disabled(new_promo_page.number_validy_input),
                            '"Number" input from Validity active after choosing option "Month" in Validy')
            self.assertTrue(new_promo_page.is_dropdown_disabled(new_promo_page.start_date_validy_input),
                            '"Start date (day of week)" dropdown active after choosing option "Month" in Validy')
            self.assertEqual(validity_number, new_promo_page.get_input_text(new_promo_page.number_validy_input),
                             '"Number" is displayed not correctly')
            self.assertFalse(new_promo_page.is_dropdown_disabled(new_promo_page.date_validy_input),
                             '"Date" dropdown disabled after choossing option "Month"')
        new_promo_page.choose_date(date_str) \
            .choose_range(range) \
            .wait_spiner_loading() \
            .enter_value(new_promo_page.number_range_input, '123456',
                         '"Number" input from Range disabled after choosing "Range" option') \
            .check_element(new_promo_page.setting_targets, 'Setting targets (KPI)') \
            .check_element(new_promo_page.split_KPI_per_pages, 'Split KPI per pages')
        self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.parametrs_split_input),
                         '"Parameters" multiselect disabled after check "Split KPI per pages"')
        new_promo_page.multiple_select_by_index_from_input(new_promo_page.parametrs_split_input,
                                                           select_name='Parameters') \
            .choose_assortment() \
            .check_element(new_promo_page.one_supplier, 'One supplier') \
            .check_element(new_promo_page.only_goods, 'Only goods in stock') \
            .check_element(new_promo_page.order_planning, 'Order planning') \
            .choose_how_to_order(how_to_order) \
            .multiple_select_by_index_from_input(new_promo_page.region_input, select_name='Region') \
            .choose_supermarket() \
            .check_element(new_promo_page.mutation, 'Mutation') \
            .multiple_select_by_index_from_input(new_promo_page.distribution_channel_input,
                                                 select_name='Distribution channel') \
            .multiple_select_by_index_from_input(new_promo_page.advertising_channel_input,
                                                 select_name='Advertising channel') \
            .multiple_select_by_index_from_input(new_promo_page.print_advertising_input,
                                                 select_name='Print advertising') \
            .multiple_select_by_index_from_input(new_promo_page.format_input, select_name='Format') \
            .multiple_select_by_index_from_input(new_promo_page.distribution_input, select_name='Distribution') \
            .check_element(new_promo_page.electronic_version, 'Electronic version') \
            .enter_value(new_promo_page.external_agency_input, external_agency, '"External agency" is non-interactive') \
            .check_element(new_promo_page.web_globus, 'Web Globus.cz') \
            .check_element(new_promo_page.web_shop, 'Web shop') \
            .check_element(new_promo_page.direct_mail, 'Direct mail') \
            .check_element(new_promo_page.shelf_labels, 'Shelf labels')
        self.assertFalse(new_promo_page.is_multiselect_disabled(new_promo_page.type_of_labels_input),
                         '"Type of labeles" still be disabled after checking "Shelf labels"')
        new_promo_page.multiple_select_by_index_from_input(new_promo_page.type_of_labels_input,
                                                           select_name='Type of labeles') \
            .multiple_select_by_index_from_input(new_promo_page.pos_support_input, select_name='POS support') \
            .check_element(new_promo_page.defined_direct_costs, 'Defined direct costs') \
            .check_element(new_promo_page.suppliers_contributions, 'Suppliers contributions') \
            .enter_value(new_promo_page.duration_input, duration, '"Duration" is non-interactive') \
            .choose_workflow(workflow) \
            .enter_value(new_promo_page.validy_from_input, valid_from, '"Valid from" is non-interactive') \
            .enter_value(new_promo_page.validy_to_input, valid_to, '"Valid to" is non-interactive') \
            .click_save_button()
        # new_promo_page.wait_for_url_matches(self.base_url + 'promo-type')
        # new_promo_page.wait_spiner_loading()
        time.sleep(1)
        new_id = data_base.get_last_id('[PromoToolGlobus].[PromoTool].[PromoActionType]')
        print(last_id, new_id)
        if last_id == new_id:
            raise Exception("New promo type wasn't created")
        else:
            data_base.execute(
                'DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionTypeToSite] WHERE [PromoActionTypeId]={0}'.
                    format(new_id))
            data_base.execute(
                'DELETE FROM [PromoToolGlobus].[PromoTool].[PromoActionType] WHERE [Id]={0}'.format(new_id))

    def test_edit_existed_template(self):
        # TODO this
        pass

    def test_unsaved_data_pop_up(self):
        # TODO
        pass

    def change_columns_location(self):
        # TODO
        id_column = self.promo_type_page.get_id_header_element()
        name_column = self.promo_type_page.get_name_header_element()
        template_column = self.promo_type_page.get_template_header_element()
        filter = TableFilter(self.driver)

        filter.change_column_location(id_column, template_column)
