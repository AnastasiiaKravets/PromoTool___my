from utilities.PromoRequest import PromoRequest
from Pages.page_planning.PagePlanning import PagePlanning
import time
from BaseTest import BaseTest
from utilities.Parser import Parser
from utilities.Table import Table
from Pages.article_list_page.ArticleListPage import ArticleListPage
from Pages.promo_actions_page.PromoActionsPage import PromoActionsPage
from utilities.PromoRequest import PromoRequest
from Pages.promo_detail_page.PagesViewWidget import PagesViewWidget
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class PagePlanningTest(BaseTest):

    # promo_action_B = 'AG35 VÝPRODEJ NON-FOOD KW 01/2016'
    # promo_action_B = 'Faltblatt 2017 týden 52'
    promo_action_B = 'Mimoleták 2018 týden 04'
    article_name = 'SUNLIGHT ALL-IN-1 EXTRA POWER 52KS'

    go_back_from_article = (By.CSS_SELECTOR, "a.back-button.button-default.k-button.k-button-icontext.k-toolbar-first-visible")


    def setUp(self):
        super().setUp()
        self.driver.get(self.base_url + '404')
        PromoRequest(self.driver).authorization_by_request(login=self.autotest_user['login'],
                                                           password=self.autotest_user['password'], language='cs')
        # time.sleep(2)
        self.driver.get(self.base_url + 'article-planning/535882/2')#'promo-detail/535882')#"article-planning/535835/2" )# 'article-planning/417791/1')# 'article-planning/535797/1')
        self.page_planning_page = PagePlanning(self.driver)
        time.sleep(2)
        self.page_article_list = ArticleListPage(self.driver)
        self.promo_actions_page = PromoActionsPage(self.driver)

    def tearDown(self):
        self.driver.close()

    def test_verify_web_elements_and_text_on_page_planning_page(self):
        """Verify presence of all elements on the Page Planning page"""
        with self.subTest():
            '''Table content'''
            self.assertTrue(len(self.page_planning_page.get_table().size) != 0, 'Page planning table is not visible')
            '''Title text'''
            self.assertEqual('Plánování stránky', self.page_planning_page.get_title().get_attribute("textContent"),
                             'Page planning title text is incorrect')
            '''Buttons text'''
            self.assertEqual('Zpět', self.page_planning_page.get_button_back().get_attribute("textContent"),
                             '"Back" button text is incorrect')
            self.assertEqual('Uložit', self.page_planning_page.get_save_button().get_attribute("textContent"),
                             '"Save" button text is incorrect')
            self.assertEqual('Přidat zbožíSeznam produktůHledání produktů', self.page_planning_page.
                        get_add_goods_button().get_attribute("textContent"), '"Add goods" button text is incorrect')
            self.assertEqual('Přidat referenční akci', self.page_planning_page.get_add_reference_promo_button().
                             get_attribute("textContent"), '"Add reference promo" button text is incorrect')
            self.assertEqual('Záhlaví stránky', self.page_planning_page.get_page_header_button().
                             get_attribute("textContent"), '"Page header" button text is incorrect')
            self.assertEqual('Grafické prvky', self.page_planning_page.get_graphic_elements_button().
                             get_attribute("textContent"), '"Graphic elements" button text is incorrect')
            '''Buttons availability'''
            self.assertTrue(len(self.page_planning_page.get_button_back().size) != 0,
                                                                                '"Back" button is not available')
            self.assertTrue(len(self.page_planning_page.get_save_button().size) != 0,
                                                                                '"Save" button is not available')
            self.assertTrue(len(self.page_planning_page.get_add_goods_button().size) != 0,
                                                                                '"Add goods" button is not available')
            self.assertTrue(len(self.page_planning_page.get_add_reference_promo_button().size) != 0,
                                                                    '"Add reference promo" button is not available')
            self.assertTrue(len(self.page_planning_page.get_page_header_button().size) != 0,
                                                                    '"Page header" button is not available')
            self.assertTrue(len(self.page_planning_page.get_graphic_elements_button().size) != 0,
                                                                    '"Graphic elements" button is not available')
            '''Toolbars'''
            self.assertTrue(len(self.page_planning_page.get_buttons_toolbar().size) != 0,
                                                                                'Buttons toolbar is not visible')
            self.assertTrue(len(self.page_planning_page.get_header_pane().size) != 0, 'Header pane is not visible')
            self.assertTrue(len(self.page_planning_page.get_article_planning_graphs().size) != 0,
                                                                'Article planning toolbar with graphs is not visible')
            self.assertTrue(len(self.page_planning_page.get_overview_of_positions_graph().size) != 0,
                                                                'Overview of positions graph is not visible')
            self.assertTrue(len(self.page_planning_page.get_gross_profit_planned_vs_calculated().size) != 0,
                                                        'Gross profit planned vs calculated is not visible')
            self.assertTrue(len(self.page_planning_page.get_expected_margin().size) != 0,
                                                                        'Expected margin is not visible')
            self.assertTrue(len(self.page_planning_page.get_plan_view().size) != 0,
                                                                        'Plan view graph is not visible')
            '''Table headers'''
            self.assertTrue(self.page_planning_page.verify_tabel_headers_text(), 'Something wrong with name of headers in table')
            self.assertTrue(self.page_planning_page.verify_tabel_headers_web_elements(), 'Something wrong with table headers')

    def test_fold_unfold_active_elements(self):
        # Hide page header button
        button_web_element = self.page_planning_page.get_page_header_button()

        # when header pane is visible 'style' attribute is empty
        header_pane_status_before_click = self.page_planning_page.get_header_pane().get_attribute('style')

        # Click on the hide page header button
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", button_web_element)
        else:
            button_web_element.click()

        # when header pane is visible 'style' attribute is empty
        header_pane_status_after_click = self.page_planning_page.get_header_pane().get_attribute('style')

        # After clicking on the hide page header button the page header pane should disappear
        if header_pane_status_before_click == '' and header_pane_status_after_click == 'height: 30px;':
            pane_is_closed = True

        self.assertTrue(pane_is_closed, 'Pane can not be closed')

        # ------------- Click the button again ------------- #
        header_pane_status_before_click = self.page_planning_page.get_header_pane().get_attribute('style')

        # Click on the hide page header button, this time the pane should be open
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", button_web_element)
        else:
            button_web_element.click()

        # when header pane is visible 'style' attribute is empty
        header_pane_status_after_click = self.page_planning_page.get_header_pane().get_attribute('style')

        # After clicking on the hide page header button the page header pane should disappear
        if header_pane_status_before_click == 'height: 30px;' and header_pane_status_after_click == '':
            pane_is_opened = True

        self.assertTrue(pane_is_opened, 'Pane can not be opened')

        # ------------- Click the graph pane button ------------- #
        graphs_pane_hide_button = self.page_planning_page.get_graphic_elements_button()

        graphs_pane_before_click = self.page_planning_page.get_graphs_pane().get_attribute('class')

        # Click on the hide page header button, this time the pane should be open
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", graphs_pane_hide_button)
        else:
            graphs_pane_hide_button.click()

        graphs_pane_after_click = self.page_planning_page.get_graphs_pane().get_attribute('class')

        if 'closed' not in graphs_pane_before_click and 'closed' in graphs_pane_after_click:
            graph_pane_is_closed = True

        self.assertTrue(graph_pane_is_closed, 'Graph pane can not be closed')

        # ------------- Click the graph pane button again ------------- #
        graphs_pane_before_click = self.page_planning_page.get_graphs_pane().get_attribute('class')

        # Click on the hide page header button, this time the pane should be open
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", graphs_pane_hide_button)
        else:
            graphs_pane_hide_button.click()

        graphs_pane_after_click = self.page_planning_page.get_graphs_pane().get_attribute('class')

        if 'closed' in graphs_pane_before_click and 'closed' not in graphs_pane_after_click:
            graph_pane_is_opened = True

        self.assertTrue(graph_pane_is_opened, 'Graph pane can not be opened')

    def test_open_and_close_positions_from_page_planning_table(self):
        table_web_element = self.page_planning_page.get_table()

        self.page_planning_page.wait_spiner_loading()

        # check if there is at least 1 record/subtable present
        if self.page_planning_page.check_if_main_table_exist():

            nested_table_inst = Table(self.driver, table_web_element)

            list_of_webelements_nested_tables = nested_table_inst.get_nested_tables('The parent nested table cant be located')
            nested_table_inst.open_all_nested_tables()

            nested_table_inst.close_all_nested_tables(list_of_webelements_nested_tables)
            # open 1st position
            nested_table_inst.open_nested_table(list_of_webelements_nested_tables[0])

    # def test_open_article_from_page_planning_table(self):
    #     table_web_element = self.page_planning_page.get_table()
    #
    #     self.page_planning_page.wait_spiner_loading()
    #
    #     # check if there is at least 1 record/subtable present
    #     if self.page_planning_page.check_if_main_table_exist():
    #
    #         nested_table_inst = Table(self.driver, table_web_element)
    #
    #         list_of_webelements_nested_tables = nested_table_inst.get_nested_tables('The parent nested table cant be located')
    #
    #         nested_table_inst.open_nested_table(list_of_webelements_nested_tables[0])
    #
    #         clear_first_nest_table = nested_table_inst.get_opened_nested_tables()
    #         first_nested_table_inst = Table(self.driver, clear_first_nest_table[0])
    #
    #         article_row = first_nested_table_inst.get_web_element_of_cell_or_row_by_column_index_and_text_in_cell(6,
    #                                                                                             self.article_name, 6)
    #
    #         self.driver.execute_script("return arguments[0].scrollIntoView(true);", article_row)
    #
    #         if Parser().get_browser_name() is 'IE':
    #             self.driver.execute_script("arguments[0].click();", article_row)
    #         else:
    #             article_row.click()
    #
    #         article_link = first_nested_table_inst.get_web_element_of_cell_or_row_by_column_index_and_text_in_cell(6,
    #                                                                                             self.article_name, 6)
    #
    #         if Parser().get_browser_name() is 'IE':
    #             self.driver.execute_script("arguments[0].click();", article_link)
    #         else:
    #             article_link.click()
    #
    #         self.assertEqual('Seznam produktů', self.page_article_list.get_title().get_attribute("textContent"),
    #                          'Article list page was not opened')

    def test_page_planning_open_via_promo_actions(self):
        """Verify opening of Page planning via Promo Actions page"""
        self.driver.get(self.base_url + 'promo-actions')
        promo_action_on_last_page = True
        data_from_promo_detail = self.promo_actions_page.get_promo_action_details_by_name(self.promo_action_B, promo_action_on_last_page)

        # open promo action by name
        promo_action_web_element = self.promo_actions_page.find_promo_action_by_name(self.promo_action_B, promo_action_on_last_page)

        if promo_action_web_element != 0:
            promo_action_web_element.click()

        pages_view = PagesViewWidget(self.driver)

        data_from_page_planning = pages_view.get_page_planning_data_by_its_number("2")

        pages_view.click_on_page_planning_by_its_number("2")

        table_web_element = self.page_planning_page.get_table()

        self.page_planning_page.wait_spiner_loading()

        # check if there is at least 1 record/subtable present
        if self.page_planning_page.check_if_main_table_exist():

            nested_table_inst = Table(self.driver, table_web_element)

            list_of_webelements_nested_tables = nested_table_inst.get_nested_tables(
                'The parent nested table cant be located')

            nested_table_inst.open_nested_table(list_of_webelements_nested_tables[0])

            clear_first_nest_table = nested_table_inst.get_opened_nested_tables()
            first_nested_table_inst = Table(self.driver, clear_first_nest_table[0])

            article_row = first_nested_table_inst.get_web_element_of_cell_or_row_by_column_index_and_text_in_cell(
                                                                                            6, self.article_name, 6)

            self.driver.execute_script("return arguments[0].scrollIntoView(true);", article_row)

            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", article_row)
            else:
                article_row.click()

            article_link = first_nested_table_inst.get_web_element_of_cell_or_row_by_column_index_and_text_in_cell(
                                                                                            6, self.article_name, 6)

            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", article_link)
            else:
                article_link.click()

            self.assertEqual('Seznam produktů', self.page_article_list.get_title().get_attribute("textContent"),
                             'Article list page was not opened')

    def test_add_goods_article_list(self):
        table_web_element = self.page_planning_page.get_table()

        self.page_planning_page.wait_spiner_loading()

        if self.page_planning_page.check_if_main_table_exist():
            nested_table_inst = Table(self.driver, table_web_element)

            list_of_webelements_nested_tables = nested_table_inst.get_nested_tables(
                'The parent nested table cant be located')

            self.page_planning_page.select_position_page_planning('1')

            self.page_planning_page.get_add_goods_button().click()

            self.page_planning_page.get_article_list_button().click()

            # article_table = self.page_article_list.get_article_table()

            # article_table_inst = Table(self.driver, article_table)

            all_checkboxes = self.page_article_list.get_list_of_checkbox_locators()

            for checkbox in all_checkboxes:
                checkbox
            None

    # def test_add_goods_havnt_selected_position(self):


    # def test_flow_creating_promo_action_adding_position_verify_page_planning_parameters(self):
    #
    #     table_web_element = self.page_planning_page.get_table()
    #
    #     self.page_planning_page.wait_spiner_loading()


