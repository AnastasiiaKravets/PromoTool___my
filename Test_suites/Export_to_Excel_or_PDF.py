import random
import shutil
import time
import unittest

from BaseTest import BaseTest
from Pages.home_page.HomePage import HomePage
from Pages.page_planning.PagePlanning import PagePlanning
from Pages.promo_detail_page.ComparedPromoWidget import ComparedPromoWidget
from utilities.BasePopUp import BasePopUp
from utilities.Parser import Parser
from utilities.PresenceFile import PresenceFile
from utilities.PromoRequest import PromoRequest
from utilities.Table import TableFilter, Table


# TODO Calendars?????


@unittest.skipIf(Parser().get_browser_name() in 'IE', 'Export in Internet Explorer is impossible')
class ExportTableTest(BaseTest):
    path = BaseTest.download_directory

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.path, ignore_errors=False)

    def setUp(self):
        super().setUp()
        self.driver.get(self.base_url + '404')
        PromoRequest(self.driver).authorization_by_request(login=self.admin_user['login'],
                                                           password=self.admin_user['password'], language='cs')
        self.page_table = TableFilter(self.driver)
        self.file_presents = PresenceFile(self.path)

    def export_in_pdf_excel(self, table, page):
        filter = TableFilter(self.driver)
        headers = [header for header in self.page_table.get_all_headers_from_table(table)
                   if 'display: none;' not in header.get_attribute('style')]
        index = random.randint(0, len(headers) - 1)
        filter.export_to_excel(headers[index])
        self.file_presents.is_new_excel_file_present(page)
        index = random.randint(0, len(headers) - 1)
        filter.export_to_pdf(headers[index])
        filter.wait_for_prepare_pdf()
        self.file_presents.is_new_pdf_file_present(page)

    @unittest.skip('long loading')
    def test_export_promo_actions(self):
        page_url = self.base_url + 'promo-actions'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    @unittest.skip('long loading')
    def test_export_promo_order(self):
        page_url = self.base_url + 'promo-order'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    @unittest.expectedFailure
    def test_export_promo_details(self):
        page_url = self.base_url + 'promo-detail/17787'
        self.driver.get(page_url)
        time.sleep(3)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)
            compared_action_table = ComparedPromoWidget(self.driver).click_add_compared_action().get_all_headers_table()
            for table in compared_action_table:
                self.export_in_pdf_excel(table, page_url)

    def test_export_list_of_compared_groups(self):
        page_url = self.base_url + 'list-of-compared-groups/17787'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_generate_reservation(self):
        page_url = self.base_url + 'generate-reservation/17787'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_evaluation(self):
        page_url = self.base_url + 'home'
        self.driver.get(page_url)
        HomePage(self.driver).click_evaluation_menuitem()
        with self.subTest():
            tables = BasePopUp(self.driver, 'Evaluation').get_all_headers_table()
            for table in tables:
                if table.is_displayed():
                    self.export_in_pdf_excel(table, page_url)

    def test_export_page_planning(self):
        page_url = self.base_url + 'article-planning/17787/1'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                # костиль, але потрібно позбавитись від останнього хедера
                filter = TableFilter(self.driver)
                headers = [header for header in self.page_table.get_all_headers_from_table(table)
                           if 'display: none;' not in header.get_attribute('style')]
                index = random.randint(0, len(headers) - 2)
                filter.export_to_excel(headers[index])
                self.file_presents.is_new_excel_file_present(page_url)
                index = random.randint(0, len(headers) - 2)
                filter.export_to_pdf(headers[index])
                filter.wait_for_prepare_pdf()
                self.file_presents.is_new_pdf_file_present(page_url)
            new_table = Table(self.driver, PagePlanning(self.driver).get_table())
            cells = new_table.wait_table_to_load().get_row(0)
            nested_table = new_table.open_nested_table(cells[0])[0]
            self.export_in_pdf_excel(nested_table, page_url)

    # TODO
    @unittest.skip('TODO')
    def test_mutation(self):
        page_url = self.base_url + 'article-planning/17787/1'
        self.driver.get(page_url)
        planning_page = PagePlanning(self.driver)
        # article mutation
        page_table = Table(self.driver, planning_page.get_table())
        cells = page_table.wait_table_to_load().get_row(0)
        nested_table = page_table.open_nested_table(cells[0])[0]
        nested_table_content = nested_table.find_element_by_class_name('k-grid-content')
        nested_cells = Table(self.driver, nested_table_content).get_row(0)
        nested_cells[0].click()
        time.sleep(3)
        article_mutation = planning_page.get_article_mutation(nested_cells[0])
        article_mutation_tables = article_mutation.get_all_headers_table()
        for table in article_mutation_tables:
            self.export_in_pdf_excel(table, page_url)
        time.sleep(5)
        """self.export_in_pdf_excel(nested_table, page_url)

        planning_page = PagePlanning(self.driver)
        cells = Table(self.driver, planning_page.get_table_content()).wait_table_to_load().get_row(0)
        cells[3].click()
        mutation = planning_page.get_position_mutation(cells[3])
        mutation.click_ok_button()

        planning_page.check_edit_checkbox(cells[2])
        time.sleep(5)

        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)"""

    @unittest.skip('need to add export')
    def test_export_positions_view(self):
        page_url = self.base_url + 'promo-positions/17787/1'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_department_planning(self):
        page_url = self.base_url + 'article-planning-department/535836/34'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                # костиль, але потрібно позбавитись від останнього хедера
                filter = TableFilter(self.driver)
                headers = [header for header in self.page_table.get_all_headers_from_table(table)
                           if 'display: none;' not in header.get_attribute('style')]
                # print('count header', len(headers))
                index = random.randint(0, len(headers) - 2)
                filter.export_to_excel(headers[index])
                self.file_presents.is_new_excel_file_present(page_url)
                index = random.randint(0, len(headers) - 2)
                filter.export_to_pdf(headers[index])
                filter.wait_for_prepare_pdf()
                self.file_presents.is_new_pdf_file_present(page_url)

            new_table = Table(self.driver, PagePlanning(self.driver).get_table())
            cells = new_table.wait_table_to_load().get_row(0)
            nested_table = new_table.open_nested_table(cells[0])[0]
            self.export_in_pdf_excel(nested_table, page_url)

    def test_export_article_list(self):
        page_url = self.base_url + 'articles-list/17787/44135/26708'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_article_details(self):
        page_url = self.base_url + 'article-detail/5/690'
        self.driver.get(page_url)
        i = 0
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                if table.is_displayed():
                    if not i == 1:  # skip Picture table
                        self.export_in_pdf_excel(table, page_url)
                    i += 1

    def test_export_reservation_list(self):
        page_url = self.base_url + 'reservations-list'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_reservation_detail(self):
        page_url = self.base_url + 'reservation-detail/1'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    @unittest.skip('long loading')
    def test_export_suppliers(self):
        page_url = self.base_url + 'suppliers'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    @unittest.skip('long loading')
    def test_export_supplier_detail(self):
        page_url = self.base_url + 'supplier-detail/30002'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    @unittest.skip('long loading')
    def test_export_bonus_list(self):
        page_url = self.base_url + 'bonus-list'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_bonus_detail(self):
        page_url = self.base_url + 'bonus-detail/1'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_list_of_collisions(self):
        page_url = self.base_url + 'collisions-list'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    @unittest.skip('long loading')
    def test_export_product_database(self):
        page_url = self.base_url + 'product-database'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_users(self):
        page_url = self.base_url + 'admin/users'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_roles(self):
        page_url = self.base_url + 'admin/roles'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_operations(self):
        page_url = self.base_url + 'admin/operations'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_dictionaries(self):
        page_url = self.base_url + 'admin/dictionaries'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_promo_type(self):
        page_url = self.base_url + 'promo-type'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    @unittest.skip('long loading')
    def test_export_locale(self):
        page_url = self.base_url + 'admin/locale'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    def test_export_reports_list(self):
        page_url = self.base_url + 'reports-list'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    # TODO в панелі інструментів
    @unittest.skip('TODO')
    def test_export_order_details(self):
        page_url = self.base_url + 'order-details/535795/4001'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)

    # TODO
    @unittest.skip('TODO')
    def test_home_grids_widget(self):
        pass

    # TODO
    @unittest.skip('TODO')
    def test_export_reference_promo(self):
        page_url = self.base_url + 'promo-reference/17787/44135/26708'
        self.driver.get(page_url)
        with self.subTest():
            tables = self.page_table.get_all_headers_table()
            for table in tables:
                self.export_in_pdf_excel(table, page_url)
