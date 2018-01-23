from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utilities.Table import TableFilter
from selenium.webdriver.support.wait import WebDriverWait
from BasePage import BasePage
from Pages.page_planning.ArticlesMutationPopUp import ArticlesMutationPopUp
from Pages.page_planning.PositionMutationPopUp import PositionMutationPopUp
from utilities.Parser import Parser

class PagePlanning(BasePage):

    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

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

    """TABLE HEADER"""
    assigned_position_header = (By.CSS_SELECTOR, 'th[data-index="0"]')
    edit_header = (By.CSS_SELECTOR, 'th[data-index="1"]')
    number_header = (By.CSS_SELECTOR, 'th[data-index="2"]')
    order_status_a_header = (By.CSS_SELECTOR, 'th[data-index="3"]')
    pos_bonus_a_header = (By.CSS_SELECTOR, 'th[data-index="4"]')
    shop_header = (By.CSS_SELECTOR, 'th[data-index="5"]')
    location_header = (By.CSS_SELECTOR, 'th[data-index="6"]')
    icon_header = (By.CSS_SELECTOR, 'th[data-index="7"]')
    name_header = (By.CSS_SELECTOR, 'th[data-index="8"]')
    number_of_ean_header = (By.CSS_SELECTOR, 'th[data-index="9"]')
    sp_promo_header = (By.CSS_SELECTOR, 'th[data-index="10"]')
    sp_promo_a_header = (By.CSS_SELECTOR, 'th[data-index="11"]')
    confirmation_header = (By.CSS_SELECTOR, 'th[data-index="12"]')
    planned_turn_over_header = (By.CSS_SELECTOR, 'th[data-index="13"]')
    forecasted_turn_over_header = (By.CSS_SELECTOR, 'th[data-index="14"]')
    req_disc_a_header = (By.CSS_SELECTOR, 'th[data-index="15"]')
    expected_margin_header = (By.CSS_SELECTOR, 'th[data-index="16"]')
    suppliers_contribution_header = (By.CSS_SELECTOR, 'th[data-index="17"]')
    pp_promotional_a_header = (By.CSS_SELECTOR, 'th[data-index="18"]')
    req_pp_discount_header = (By.CSS_SELECTOR, 'th[data-index="19"]')
    promotional_gross_profit_header = (By.CSS_SELECTOR, 'th[data-index="20"]')
    note_header = (By.CSS_SELECTOR, 'th[data-index="21"]')
    restrictions_header = (By.CSS_SELECTOR, 'th[data-index="22"]')
    picture_header = (By.CSS_SELECTOR, 'th[data-index="23"]')
    calculated_turn_over_header = (By.CSS_SELECTOR, 'th[data-index="24"]')
    hidden_sales_header = (By.CSS_SELECTOR, 'th[data-index="25"]')
    hidden_purchase_header = (By.CSS_SELECTOR, 'th[data-index="26"]')
    tag_header = (By.CSS_SELECTOR, 'th[data-index="27"]')
    documents_header = (By.CSS_SELECTOR, 'th[data-index="28"]')
    assortment_header = (By.CSS_SELECTOR, 'th[data-index="29"]')
    type_of_promotion_header = (By.CSS_SELECTOR, 'th[data-index="30"]')
    globus_bonus_header = (By.CSS_SELECTOR, 'th[data-index="31"]')
    hidden_planned_sales_qty_header = (By.CSS_SELECTOR, 'th[data-index="32"]')
    deviation_header = (By.CSS_SELECTOR, 'th[data-index="33"]')
    validity_from_header = (By.CSS_SELECTOR, 'th[data-index="34"]')
    validity_to_header = (By.CSS_SELECTOR, 'th[data-index="35"]')
    validity_from_purchase_price = (By.CSS_SELECTOR, 'th[data-index="36"]')
    validity_to_purchase_price = (By.CSS_SELECTOR, 'th[data-index="37"]')
    clearance_sales = (By.CSS_SELECTOR, 'th[data-index="38"]')

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
        nested_parent_webelement = self.wait.until(EC.presence_of_element_located(self.nested_table_parent),
                                                                            "Nested parent table is not visible")
        return nested_parent_webelement

    def get_title(self):
        title_web_element = self.wait.until(EC.presence_of_element_located(self.title), 'Title on Page Planning is absent')
        return title_web_element

    def get_button_back(self):
        back_button_web_element = self.wait.until(EC.presence_of_element_located(self.back_button_locator),
                                                  'Button "Back" is absent')
        return back_button_web_element

    def get_save_button(self):
        save_button_web_element = self.wait.until(EC.presence_of_element_located(self.save_button_locator),
                                                  'Button "Save" is absent')
        return save_button_web_element

    def get_add_goods_button(self):
        add_goods_button_web_element = self.wait.until(EC.presence_of_element_located(self.add_goods_button_locator),
                                                  'Button "Add goods" is absent')
        return add_goods_button_web_element

    def get_add_reference_promo_button(self):
        add_reference_promo_button_web_element = self.wait.until(EC.presence_of_element_located(
                            self.add_reference_promo_button_locator), 'Button "Add reference promo" is absent')
        return add_reference_promo_button_web_element

    def get_article_list_button(self):
        if self.is_element_present(self.article_list_button):
            return self.get_visible_element(self.article_list_button)


    def get_page_header_button(self):
        add_reference_promo_button_web_element = self.wait.until(EC.presence_of_element_located(
                            self.page_header_hide_button), 'Button "Page header" is absent')
        return add_reference_promo_button_web_element

    def get_graphic_elements_button(self):
        graphic_elements_button_web_element = self.wait.until(EC.presence_of_element_located(
                            self.graphic_elements_button), 'Button "Graphic elements" is absent')
        return graphic_elements_button_web_element

    def get_buttons_toolbar(self):
        buttons_toolbar_web_element = self.wait.until(EC.presence_of_element_located(
                            self.buttons_toolbar), 'Buttons toolbar is absent')
        return buttons_toolbar_web_element

    def get_header_pane(self):
        page_header_pane_web_element = self.wait.until(EC.presence_of_element_located(
                            self.page_header_pane), 'Header pane is absent')
        return page_header_pane_web_element

    def get_article_planning_graphs(self):
        article_planning_graphs_toolbar_web_element = self.wait.until(EC.presence_of_element_located(
                            self.article_planning_graphs_toolbar), 'Article planning graph toolbar is absent')
        return article_planning_graphs_toolbar_web_element

    def get_overview_of_positions_graph(self):
        overview_of_positions_graph_web_element = self.wait.until(EC.presence_of_element_located(
                            self.overview_of_positions_graph), 'Overview of position graph is absent')
        return overview_of_positions_graph_web_element

    def get_gross_profit_planned_vs_calculated(self):
        gross_profit_planned_vs_calculated_web_element = self.wait.until(EC.presence_of_element_located(
                            self.gross_profit_planned_vs_calculated), 'Gross profit planned vs calculated is absent')
        return gross_profit_planned_vs_calculated_web_element

    def get_expected_margin(self):
        expected_margin_web_element = self.wait.until(EC.presence_of_element_located(
                            self.expected_margin), 'Expected margin is absent')
        return expected_margin_web_element

    def get_plan_view(self):
        plan_view_web_element = self.wait.until(EC.presence_of_element_located(self.plan_view),
                                                'Plan view graph is absent')
        return plan_view_web_element

    def get_graphs_pane(self):
        graphs_pane_web_element = self.wait.until(EC.presence_of_element_located(
                            self.graphs_pane_without_button), 'Graphs pane is absent')
        return graphs_pane_web_element

    def check_edit_checkbox(self, cell_element):
        checkbox = WebDriverWait(cell_element, 5).until(EC.element_to_be_clickable(self.edit_checkbox),
                                                        '"Edit" checkbox is not clickable')
        self.driver.execute_script("return arguments[0].scrollIntoView();", checkbox)
        checkbox.click()
        self.wait_spiner_loading()
        return self

    def get_position_mutation(self, element):
        try:
            menu = self.get_context_menu(element, 'Context menu for Main position on page planning is absent')
            mutation = WebDriverWait(menu, 2).until(EC.visibility_of_any_elements_located
                                                    ((By.CSS_SELECTOR, 'li[class="k-item k-state-default k-last"]')),
                                                    'Options from context menu for Main position on page planning '
                                                    'is invisible')[0]
        except:
            menu = self.get_context_menu(element, 'Context menu for Main position on page planning is absent')
            mutation = WebDriverWait(menu, 5).until(EC.visibility_of_any_elements_located
                                                    ((By.CSS_SELECTOR, 'li[class="k-item k-state-default k-last"]')),
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

    def get_first_nested_row(self):

        nesty_table_web_element = self.wait.until(EC.presence_of_element_located(self.nested_table),
                                            'The 1st nested row cant be located')
        return nesty_table_web_element

    def get_nested_rows(self):

        parent_elem = self.wait.until(EC.presence_of_element_located(self.nested_table_parent),
                                      'The parent nested table cant be located')

        element_list = parent_elem.find_elements_by_tag_name("tr")

        return element_list

    def select_position_page_planning(self, row_number):

        position_web_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "(//table[@role='treegrid']/tbody[@role='rowgroup']/tr[@role='row'])['"+row_number+"']")))
            # WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(By.XPATH, "(//table[@role='treegrid']/tbody[@role='rowgroup']/tr[@role='row'])['"+row_number+"']"), error)

        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", position_web_element)
        else:
            position_web_element.click()

        return position_web_element
