import random
import time
from datetime import date, timedelta

from BaseTest import BaseTest
from Pages.article_list_page.ArticleFilterForm import ArticleFilterForm
from Pages.article_list_page.ArticleListPage import ArticleListPage
from Pages.order_details_page.OrderDetailsPage import OrderDetailsPage
from Pages.page_planning.PagePlanning import PagePlanning
from Pages.positions_view.PositionsView import PositionsView
from Pages.promo_detail_page.BasicInformationForm import BasicInformation
from Pages.promo_detail_page.PagesViewWidget import PagesViewWidget
from Pages.promo_order_page.PromoOrderPage import PromoOrderPage
from Pages.promo_type_page.NewPromoTypePage import NewPromoTypePage
from utilities import utils
from utilities.PromoRequest import PromoRequest
from utilities.Table import Table, TableFilter


class PilotFlowTest(BaseTest):
    action_id = None

    @classmethod
    def setUpClass(cls):
        cls.promo_type_id = 1
        cls.type_valid_from = (date.today() - timedelta(days=random.randint(1, 15))).strftime('%d%m%Y')
        cls.type_valid_to = (date.today() + timedelta(weeks=random.randint(1, 8), days=random.randint(1, 15))) \
            .strftime('%d%m%Y')

    @classmethod
    def tearDownClass(cls):
        global action_id
        if cls.action_id is not None:
            super(PilotFlowTest, cls).setUp()
            PromoRequest(cls.driver).authorization_by_request(login=cls.pilot_admin_user['login'],
                                                              password=cls.pilot_admin_user['password'], language='en')

            PromoRequest(cls.driver).delete_promo_action(cls.action_id)
            cls.driver.close()

    def setUp(self):
        super(PilotFlowTest, self).setUp()
        PromoRequest(self.driver).authorization_by_request(login=self.pilot_admin_user['login'],
                                                           password=self.pilot_admin_user['password'], language='en')

    def test_promo_action_flow(self):
        global action_id
        action_name = 'Action for pilot test {}'.format(random.randint(0, 100))
        action_description = 'AutoTest'
        base_date = utils.get_valid_date_from_for_action(self.driver, self.promo_type_id)
        action_valid_from_date = base_date.strftime('%d%m%Y')
        action_valid_to_date = (base_date + timedelta(weeks=3)).strftime('%d%m%Y')
        first_row = 0
        edit_column = 2
        assortment_for_position = [0, 1, 2, 3, 4, 5]

        self.driver.get('{}promo-type/{}'.format(self.base_url, self.promo_type_id))
        type_page = NewPromoTypePage(self.driver)

        type_page.enter_date(type_page.validy_from_input, self.type_valid_from,
                             "Can't enter new value for Valid from input on Promo type page") \
            .enter_date(type_page.validy_to_input, self.type_valid_to,
                        "Can't enter new value for Valid to input on Promo Type page") \
            .click_save_button().wait_spiner_loading()

        action_detail_page = type_page.click_new_promo_button()
        type_page.wait_for_url_contain('{}promo-detail/'.format(self.base_url),
                                       'Promo detail page was not loaded after creating new promo page')
        action_id = self.driver.current_url.split('promo-detail/')[1]
        print('-----------------{}-------------------'.format(action_id))
        action_detail_page.wait_spiner_loading()

        basic_info = BasicInformation(self.driver).wait_spiner_loading()
        basic_info.enter_value(basic_info.name_input, action_name,
                               "Can't enter new value for Name input on Promo Detail page") \
            .enter_value(basic_info.description_input, action_description,
                         "Can't enter new value for Description input on Promo Detail page") \
            .enter_value(basic_info.validity_from_input, action_valid_from_date,
                         "Can't enter new value for Validity from input on Promo Detail page") \
            .enter_value(basic_info.validity_to_input, action_valid_to_date,
                         "Can't enter new value for Validity to input on Promo Detail page")

        pages_view = PagesViewWidget(self.driver).wait_spiner_loading()
        pages_view.add_new_page() \
            .add_new_page() \
            .choose_assortment(first_row)
        action_detail_page.click_save_button().wait_spiner_loading()
        time.sleep(3)

        pages_view_new = PagesViewWidget(self.driver)
        pages_view_new.get_position_page_by_row_number(first_row)

        action_detail_page.wait_for_url_contain('{}promo-positions/'.format(self.base_url),
                                                'Promo position page was not loaded')

        position_page = PositionsView(self.driver)
        position_page.wait_spiner_loading() \
            .add_new_position() \
            .add_new_position() \
            .click_assortment_field(row_index=first_row).choose_option_by_index(assortment_for_position)
        position_page.click_save()
        time.sleep(1)
        position_page.click_back()
        position_page.wait_for_url_contain('promo-detail',
                                           'Promo detail page was not loaded after saving promo position page and go back')

        page_planning = PagesViewWidget(self.driver).wait_spiner_loading().get_planning_page_by_row_index(first_row)
        page_planning.wait_for_url_contain('{}article-planning/'.format(self.base_url),
                                           'Page planning page was not loaded')

        page_planning = PagePlanning(self.driver)
        planning_table = Table(self.driver,
                               page_planning.get_table_content('Table content for page planning is absent'))
        page_planning.check_edit_checkbox(planning_table.get_row(first_row)[edit_column]) \
            .select_position_page_planning(first_row, header_locator=page_planning.number_header)
        page_planning.get_add_goods_button().click()
        page_planning.get_article_list_button().click()
        page_planning.wait_for_url_contain('{}articles-list/'.format(self.base_url),
                                           'Article list page was not loaded')

        article_filter = ArticleFilterForm(self.driver)
        article_filter.clear_field(article_filter.article_code_input) \
            .clear_field(article_filter.promo_type_input) \
            .apply_filter()
        article_list_page = ArticleListPage(self.driver)
        article_list_page.check_all_checkboxes_article_list()

        page_planning = PagePlanning(self.driver)
        page_planning.wait_spiner_loading()
        # for load all added articles
        # TODO check for match added articles
        time.sleep(5)
        page_planning.click_save()

        page_planning = PagePlanning(self.driver)
        planning_table = Table(self.driver,
                               page_planning.get_table_content('Table content for page planning is absent'))
        page_planning.check_edit_checkbox(planning_table.get_row(first_row)[edit_column]).wait_spiner_loading()

        page_planning.select_position_page_planning(first_row, header_locator=page_planning.number_header)
        page_planning.get_position_mutation(planning_table.get_row(first_row)[1]) \
            .enter_promo_selling_price(first_row, '59') \
            .click_ok_button()
        page_planning.wait_spiner_loading()
        page_planning.check_edit_checkbox(planning_table.get_row(first_row)[edit_column]).wait_spiner_loading()

    def test_promo_order(self):
        globus_hm = 0
        hm_brno_4001 = [0]
        code = 'rgtkey'
        filter_state = 'Contains'
        first_row = 0
        ordered_qty_value = random.randint(1, 500)

        self.open_url('promo-order')
        order_page = PromoOrderPage(self.driver)

        shop_pop_up = order_page.click_shop_input()
        nested_group = shop_pop_up.open_base_treeitem(globus_hm)
        shop_pop_up.choose_option_by_index_from_nested_group(nested_group, hm_brno_4001)

        order_page.wait_spiner_loading()
        self.assertTrue(0 < Table(self.driver, order_page.get_table_content()).count_rows(),
                        'There is no order for chosen shop')

        TableFilter(self.driver).filter_from_header_by_string(order_page.get_header
                                                              (order_page.code_header, 'Code header is absent'),
                                                              filter_state, code)
        order_page.wait_spiner_loading()

        code_cell = Table(self.driver, order_page.get_table_content()).get_row(first_row)[1]
        order_page.click_link_from_cell(code_cell, 'There is no link in Code cell')
        order_page.wait_for_url_contain('order-details', 'Order dateils page was not opened')

        order_details_page = OrderDetailsPage(self.driver)
        selected_order = order_details_page.wait_spiner_loading().select_position(first_row)
        order_details_page.enter_value(selected_order, order_details_page.ordered_qty, ordered_qty_value,
                                       "Can't eneter value in Ordered Qty field")
        selected_order = order_details_page.wait_spiner_loading().select_position(first_row)

        order_details_page.click_split_button(selected_order) \
            .click_save()
