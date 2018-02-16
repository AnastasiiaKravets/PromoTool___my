import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utilities.Table import TableFilter, Table
from selenium.webdriver.support.wait import WebDriverWait
from BasePage import BasePage
from Pages.page_planning.ArticlesMutationPopUp import ArticlesMutationPopUp
from Pages.page_planning.PositionMutationPopUp import PositionMutationPopUp
from utilities.Parser import Parser

class PagePlanning(BasePage):


    table_locator = (By.CSS_SELECTOR, 'table[role = "treegrid"]')
    table_locator_with_controls = (By.CSS_SELECTOR, 'div.b-article-planning__grid.k-grid.k-widget.k-reorderable')
    nested_table_parent = (By.XPATH, "(//tbody[@role='rowgroup'])")
    edit_checkbox = (By.CSS_SELECTOR, 'input[class="edit-position-checkbox"]')
    title = (By.CSS_SELECTOR, 'a.title.k-button.k-state-disabled')

    buttons_toolbar = (By.CSS_SELECTOR, "div.b-article-planning__toolbar.k-toolbar.k-widget.k-toolbar-resizable")
    page_header_pane = (By.CSS_SELECTOR, "div.b-article-planning__header")#(By.CSS_SELECTOR, "div.b-form-generator")

    article_planning_graphs_toolbar = (By.CSS_SELECTOR, "div.b-article-planning-graphs__content")
    overview_of_positions_graph = (By.CSS_SELECTOR, "div.b-article-planning-graphs__content div:nth-child(1)")
    gross_profit_planned_vs_calculated = (By.CSS_SELECTOR, "div.b-article-planning-graphs__content div:nth-child(2)")
    expected_margin = (By.CSS_SELECTOR, "div.b-article-planning-graphs__content div:nth-child(3)")
    plan_view = (By.CSS_SELECTOR, "div.b-article-planning-graphs__content div:nth-child(4)")
    graphs_pane_without_button = (By.CSS_SELECTOR, "div[class^='b-custom-content b-article-planning-graphs']")

    no_table_locator = (By.CSS_SELECTOR, "div.k-grid-norecords")
    nested_table = (By.CSS_SELECTOR, "td.k-hierarchy-cell")
    # nested_tables_inner_tables = (By.CSS_SELECTOR, "div.nested-grid-widget.k-grid.k-widget.k-reorderable")

    """BUTTONS"""
    back_button_locator = (By.CSS_SELECTOR, "div.b-article-planning__toolbar.k-toolbar.k-widget.k-toolbar-resizable a:nth-child(2)")
    save_button_locator = (By.CSS_SELECTOR, "div.b-article-planning__toolbar.k-toolbar.k-widget.k-toolbar-resizable a:nth-child(3)")
    add_goods_button_locator = (By.CSS_SELECTOR, "div.add-goods-dropdown")
    add_reference_promo_button_locator = (By.CSS_SELECTOR, "div.b-article-planning__toolbar.k-toolbar.k-widget.k-toolbar-resizable a:nth-child(5)")
    page_header_hide_button = (By.CSS_SELECTOR, "div.b-form__title.b-form__title_expand")
    graphic_elements_button = (By.CSS_SELECTOR, "div.b-custom-header.b-article-planning-graphs__control")
    article_list_button = (By.CSS_SELECTOR, "ul.k-group.k-menu-group.k-popup.k-reset.k-state-border-up li:nth-of-type(1)")

    """MAIN TABLE HEADER"""
    assigned_position_header = (By.CSS_SELECTOR, 'th[data-field="IsActive"]')
    # edit_header = (By.CSS_SELECTOR, 'th[data-index="1"]')
    number_header = (By.CSS_SELECTOR, 'th[data-field="Number"]')
    order_status_a_header = (By.CSS_SELECTOR, 'th[data-field="OrderStatusA"]')
    pos_bonus_a_header = (By.CSS_SELECTOR, 'th[data-field="POSBonusA"]')
    # shop_header = (By.CSS_SELECTOR, 'th[data-field="Number"]')
    location_header = (By.CSS_SELECTOR, 'th[data-field="EPLLocation"]')
    icon_header = (By.CSS_SELECTOR, 'th[data-field="Icons"]')
    name_header = (By.CSS_SELECTOR, 'th[data-field="Name"]')
    number_of_ean_header = (By.CSS_SELECTOR, 'th[data-field="Number of EAN"]')
    sp_promo_header = (By.CSS_SELECTOR, 'th[data-field="SalesPricePromotional"]')
    sp_promo_a_header = (By.CSS_SELECTOR, 'th[data-field="SalesPricePromotionalA"]')
    confirmation_header = (By.CSS_SELECTOR, 'th[data-field="IsConfirmed"]')
    planned_turn_over_header = (By.CSS_SELECTOR, 'th[data-field="TurnoverPlanned"]')
    forecasted_turn_over_header = (By.CSS_SELECTOR, 'th[data-field="ForecastedTurnover"]')
    req_disc_a_header = (By.CSS_SELECTOR, 'th[data-field="ReqDiscountA"]')
    expected_margin_header = (By.CSS_SELECTOR, 'th[data-field="Margin"]')
    suppliers_contribution_header = (By.CSS_SELECTOR, 'th[data-field="SupplierContributionEffective"]')
    pp_promotional_a_header = (By.CSS_SELECTOR, 'th[data-field="PurchasePricePromotionalA"]')
    req_pp_discount_header = (By.CSS_SELECTOR, 'th[data-field="ReqPPDiscountA"]')
    promotional_gross_profit_header = (By.CSS_SELECTOR, 'th[data-field="GrossProfitPromotional"]')
    note_header = (By.CSS_SELECTOR, 'th[data-field="Notes.IsExists"]')
    restrictions_header = (By.CSS_SELECTOR, 'th[data-field="Restrictions"]')
    picture_header = (By.CSS_SELECTOR, 'th[data-field="Pictures.Length"]')
    calculated_turn_over_header = (By.CSS_SELECTOR, 'th[data-field="TurnoverCalculated"]')
    hidden_sales_header = (By.CSS_SELECTOR, 'th[data-field="SalesAmountPlanned"]')
    hidden_purchase_header = (By.CSS_SELECTOR, 'th[data-field="PurchaseAmountPlanned"]')
    tag_header = (By.CSS_SELECTOR, 'th[data-field="Tags.IsExists"]')
    documents_header = (By.CSS_SELECTOR, 'th[data-field="Attachments.IsExists"]')
    assortment_header = (By.CSS_SELECTOR, 'th[data-field="Assortment"]')
    type_of_promotion_header = (By.CSS_SELECTOR, 'th[data-field="TypeOfPromotion"]')
    globus_bonus_header = (By.CSS_SELECTOR, 'th[data-field="IsGlobusBonus"]')
    hidden_planned_sales_qty_header = (By.CSS_SELECTOR, 'th[data-field="SalesQtyPlanned"]')
    deviation_header = (By.CSS_SELECTOR, 'th[data-field="Deviation"]')
    validity_from_header = (By.CSS_SELECTOR, 'th[data-field="ValidityFrom"]')
    validity_to_header = (By.CSS_SELECTOR, 'th[data-field="ValidityTo"]')
    validity_from_purchase_price = (By.CSS_SELECTOR, 'th[data-field="PPValidFrom"]')
    validity_to_purchase_price = (By.CSS_SELECTOR, 'th[data-field="PPValidTo"]')
    clearance_sales = (By.CSS_SELECTOR, 'th[data-field="ClearanceSale"]')


    column_headers_text_list = [' ', 'Přiřazená pozice', 'Upravit', 'Číslo', 'Stav objednávky V', 'POS bonus V', 'Prodejna', 'Umístění', 'Ikona',
     'Název', 'Počet EAN kodů', 'akční PC', 'Akční PC V', 'Potvrzeno', 'Plánovaný obrat', 'Předpovídaný obrat',
     'Pož. sleva V', 'Očekávaná marže %', 'Příspěvěk dodavatele', 'Akční NC V', 'NC Pož sleva V',
     'Hrubý zisk akce', 'Poznámka', 'Omezení', 'Obrázek', 'Vypočítaný obrat', 'Skrytý prodej', 'Skrytý nákup', 'Štítek',
     'Dokumenty', 'Sortiment', 'Typ akce', 'Globus bonus', 'Skryté plánované tržby v ks', 'Odchylka', 'Platnost od',
     'Platnost do', 'Platnost od kupní ceny', 'Platnost do kupní ceny', 'Doprodej', '']

    def verify_tabel_headers_text(self):
        table_filter = TableFilter(self.driver)
        table = table_filter.get_all_headers_table()[0]
        # print(table_filter.get_all_headers_from_table_as_text(table))

        table_headers_text = table_filter.get_all_headers_from_table_as_text(table)

        if len(self.column_headers_text_list) == len(table_headers_text):
            for header_name, table_header_gui in zip(self.column_headers_text_list, table_headers_text):
                if header_name != table_header_gui:
                    return False
        else:
            return False

        return True

    def verify_tabel_headers_web_elements(self):
        table_filter = TableFilter(self.driver)
        table = table_filter.get_all_headers_table()[0]
        # print(table_filter.get_all_headers_from_table_as_text(table))

        table_headers_web = table_filter.get_all_headers_from_table(table)

        for header_name in table_headers_web:
            if header_name.is_enabled() is False:
                return False

        return True

    def get_table(self):
        table_content_webelement = self.get_visible_element(self.table_locator_with_controls, "Page planning table is not visible")
        return table_content_webelement

    def get_nested_parent(self):
        return  self.get_visible_element(self.nested_table_parent, "Page planning table is not visible")

    def get_title(self):
        return self.get_visible_element(self.title, "Title on Page Planning is absent")

    def get_button_back(self):
        return self.get_visible_element(self.back_button_locator, "'Back' is absent")

    def get_save_button(self):
        return self.get_visible_element(self.save_button_locator, "Button 'Save' is absent")

    def get_add_goods_button(self):
        return self.get_visible_element(self.add_goods_button_locator, "Button 'Add goods' is absent")

    def get_add_reference_promo_button(self):
        return self.get_visible_element(self.add_reference_promo_button_locator, "Button 'Add reference promo' is absent")

    def get_article_list_button(self):
        if self.is_element_present(self.article_list_button):
            return self.get_visible_element(self.article_list_button, "Button 'Article list' is absent")

    def get_page_header_button(self):
        return self.get_visible_element(self.page_header_hide_button, "Button 'Page header' is absent")

    def get_graphic_elements_button(self):
        return self.get_visible_element(self.graphic_elements_button, "Button 'Graphic elements' is absent")

    def get_buttons_toolbar(self):
        return self.get_visible_element(self.buttons_toolbar, "Buttons toolbar is absent")

    def get_header_pane(self):
        return self.get_visible_element(self.page_header_pane, "Page header pane is absent")

    def get_article_planning_graphs(self):
        return self.get_visible_element(self.article_planning_graphs_toolbar, "Article planning graph toolbar is absent")

    def get_overview_of_positions_graph(self):
        return self.get_visible_element(self.overview_of_positions_graph, "Overview of position graph is absent")

    def get_gross_profit_planned_vs_calculated(self):
        return self.get_visible_element(self.gross_profit_planned_vs_calculated, "Gross profit planned vs calculated is absent")

    def get_expected_margin(self):
        return self.get_visible_element(self.expected_margin, "Expected margin is absent")

    def get_plan_view(self):
        return self.get_visible_element(self.plan_view, "Plan view graph is absent")

    def get_graphs_pane(self):
        return self.get_visible_element(self.graphs_pane_without_button, "Graphs pane is absent")

    def check_edit_checkbox(self, cell_element):
        try:
            checkbox = WebDriverWait(cell_element, 5).until(EC.element_to_be_clickable(self.edit_checkbox),
                                                            '"Edit" checkbox is not clickable')
            self.driver.execute_script("return arguments[0].scrollIntoView();", checkbox)
            checkbox.click()
            self.wait_spiner_loading()
        except WebDriverException:
            raise Exception('Some one else already locked this position')
        return self

    def get_position_mutation(self, element):
        try:
            menu = self.get_context_menu(element, 'Context menu for Main position on page planning is absent')
            time.sleep(0.1)
            mutation = WebDriverWait(menu, 5).until(EC.visibility_of_any_elements_located
                                                    ((By.CSS_SELECTOR, 'li.k-item.k-state-default.k-last')),
                                                    'Options from context menu for Main position on page planning '
                                                    'is invisible')[0]
        except:
            menu = self.get_context_menu(element, 'Context menu for Main position on page planning is absent')
            mutation = WebDriverWait(menu, 5).until(EC.visibility_of_any_elements_located
                                                    ((By.CSS_SELECTOR, 'li.k-item.k-state-default.k-last')),
                                                    'Options from context menu for Main position on page planning '
                                                    'is invisible')[0]
        if 'k-state-disabled' in mutation.get_attribute('class'):
            raise Exception('Option "Mutation" for position mutation from context menu is disabled')
        mutation.click()
        return PositionMutationPopUp(self.driver)

    def get_article_mutation(self, element):
        try:
            menu = self.get_context_menu(element, 'Context menu for nested table on page planning is absent')
            mutation = WebDriverWait(menu, 2).until(EC.visibility_of_any_elements_located
                                                    ((By.CLASS_NAME, 'k-item')),
                                                    'Options from context menu for nested table on page planning '
                                                    'is invisible')[1]
        except:
            menu = self.get_context_menu(element, 'Context menu for nested table on page planning is absent')
            mutation = WebDriverWait(menu, 2).until(EC.visibility_of_any_elements_located
                                                    ((By.CLASS_NAME, 'k-item')),
                                                    'Options from context menu for nested table on page planning '
                                                    'is invisible')[1]
        if 'k-state-disabled' in mutation.get_attribute('class'):
            raise Exception('Option "Mutation" for article mutation from context menu is disabled')
        mutation.click()
        return ArticlesMutationPopUp(self.driver)

    def check_if_main_table_exist(self):
        full_table_web_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.table_locator_with_controls), 'Main table with controls is absent')

        webelements_with_no_records = full_table_web_element.find_elements_by_class_name('k-grid-norecords')

        if len(webelements_with_no_records) == 0:
            return True
        return False

    def select_position_page_planning(self, row_number: int=0, column_index: int=0, header_locator=None):
        """"
        Select position with mouse click on the Page Planning page and returns webelement of this row
        :param row_number - the index number of the row, where position is located
               column_index - the index number of the column, where position is located

        :return: the webelement of the row, where position is located
        """
        table = Table(self.driver, self.get_table_content())
        row = table.get_master_row_as_webelement(row_number)

        if header_locator is not None:
            column_index = table.get_column_index(header_locator) + 1
        cell = table.get_master_row(row_number)[column_index]

        try:
            self.driver.execute_script("return arguments[0].scrollIntoView();", cell)
            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", cell)
            else:
                cell.click()
            return row
        except WebDriverException:
            raise Exception('Some one else already locked this position')

    def click_save(self):
        button = self.wait.until(EC.visibility_of_element_located(self.save_button_locator),
                                 'Save button is missing')
        if self.is_button_disabled(self.save_button_locator, 'Save'):
            raise Exception('"Save" button should be active')
        else:
            button.click()
            self.wait_spiner_loading()
        return self
