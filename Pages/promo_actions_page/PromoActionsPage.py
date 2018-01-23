from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import datetime
from BasePage import BasePage
from utilities.Table import Table
from utilities.BaseForm import BaseForm

class PromoActionsPage(BaseForm):

    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

    title = (By.CSS_SELECTOR, 'div.b-promo-actions__toolbar-content.k-toolbar.k-widget.k-toolbar-resizable')
    filters_pane = (By.CSS_SELECTOR, 'div.b-form__content')
    validity_period = (By.CSS_SELECTOR, 'div.b-form__td.b-form__td_label')
    table_locator = (By.CSS_SELECTOR, 'div.k-grid-content.k-auto-scrollable')
    go_to_the_next_page = (By.CSS_SELECTOR, "div.k-pager-wrap.k-grid-pager.k-widget.k-floatwrap a:nth-child(4)")
    go_to_the_last_page = (By.CSS_SELECTOR, "a.k-link.k-pager-nav.k-pager-last")
    items_per_page = (By.CSS_SELECTOR, 'div.k-pager-wrap.k-grid-pager.k-widget.k-floatwrap span.k-dropdown-wrap.k-state-default')


    promo_action_row_data = {
        'Deadline': 0,
        'Code': 0,
        'Name': '',
        'Type': '',
        'Valid From': datetime.date.today(),
        'Valid To': datetime.date.today(),
        'Duration': 0,
        'Page': 0,
        'External code': 0
    }

    def get_title_text(self):
        title_web = self.wait.until(EC.visibility_of_element_located(self.title), 'Promo Actions page title is absent')
        return title_web.text

    def find_promo_action_by_name(self, promo_action_name, last_page=False):

        self.wait_spiner_loading()
        last_table_button_web_element = self.wait.until(EC.visibility_of_element_located(self.go_to_the_last_page),
                                                        'The last page button in not available')
        tables_number = int(last_table_button_web_element.get_attribute('data-page'))

        btn_state = self.is_button_disabled(self.go_to_the_last_page, 'Last page button, Page planning')
        if btn_state is None:
            button_disabled = False
        else:
            button_disabled = True

        if last_page is True and button_disabled is False:
            last_table_button_web_element.click()
        else:
            dropdown = self.get_dropdown(self.items_per_page)
            state_dict = {
                '10': 0,
                '50': 1,
                '100': 2
            }
            self.click_and_select_dropdown_option(state_dict, '100', "Items per page is not selectable", dropdown)

        tables_list = [i for i in range(tables_number)]

        for ind in tables_list:

            self.wait_spiner_loading()
            table_web_element = self.get_table_content()
            table_instance = Table(self.driver, table_web_element)

            cell_web_element = table_instance.get_web_element_of_cell_or_row_by_column_index_and_text_in_cell(5, promo_action_name, 5)
            if cell_web_element != 0:
                return cell_web_element

            last_table_button_web_element = self.wait.until(
                    EC.visibility_of_element_located(self.go_to_the_next_page), 'The next page button in not available')
            last_table_button_web_element.click()

        return 0

    def get_promo_action_details_by_name(self, promo_action_name, last_page=False):

        self.wait_spiner_loading()

        last_table_button_web_element = self.wait.until(
            EC.visibility_of_element_located(self.go_to_the_last_page), 'The last page button in not available')

        btn_state = self.is_button_disabled(self.go_to_the_last_page, 'Last page button, Page planning')
        if btn_state is None:
            button_disabled = False
        else:
            button_disabled = True

        if last_page is True and button_disabled is False:
            last_table_button_web_element.click()
        else:
            dropdown = self.get_dropdown(self.items_per_page)
            state_dict = {
                '10': 0,
                '50': 1,
                '100': 2
            }
            self.click_and_select_dropdown_option(state_dict, '100', "Items per page is not selectable", dropdown)

        self.wait_spiner_loading()
        # Get and save total number of pages
        tables_number = int(last_table_button_web_element.get_attribute('data-page'))
        # Create list for navigating the pages
        tables_list = [i for i in range(tables_number)]

        for ind in tables_list:

            self.wait_spiner_loading()
            table_web_element = self.get_table_content()
            table_instance = Table(self.driver, table_web_element)

            row_web_element = table_instance.get_web_element_of_cell_or_row_by_column_index_and_text_in_cell(
                                                                                        5, promo_action_name, 5, True)
            if row_web_element != 0:
                row_data_web_element = row_web_element

                deadline_negative_non_formatted_number = row_data_web_element[1].get_attribute("textContent").\
                                                                                                replace(u"\u00A0", "")
                if len(deadline_negative_non_formatted_number) > 0:
                    self.promo_action_row_data['Deadline'] = int(deadline_negative_non_formatted_number)
                self.promo_action_row_data['Code'] = (row_data_web_element[4].get_attribute("textContent"))
                self.promo_action_row_data['Name'] = row_data_web_element[5].get_attribute("textContent")
                self.promo_action_row_data['Type'] = row_data_web_element[8].get_attribute("textContent")
                if len(row_data_web_element[9].get_attribute("textContent")) > 0:
                    self.promo_action_row_data['Valid From'] = datetime.datetime.strptime(row_data_web_element[9].
                                                                    get_attribute("textContent"), "%d.%m.%Y").date()
                if len(row_data_web_element[10].get_attribute("textContent")) > 0:
                    self.promo_action_row_data['Valid To'] = datetime.datetime.strptime(row_data_web_element[10].
                                                                    get_attribute("textContent"), "%d.%m.%Y").date()
                if len(row_data_web_element[11].get_attribute("textContent")) > 0:
                    self.promo_action_row_data['Duration'] = int(row_data_web_element[11].get_attribute("textContent"))
                if len(row_data_web_element[12].get_attribute("textContent")) > 0:
                    self.promo_action_row_data['Page'] = int(row_data_web_element[12].get_attribute("textContent"))
                if len(row_data_web_element[13].get_attribute("textContent")) > 0:
                    self.promo_action_row_data['External code'] = int(row_data_web_element[13].get_attribute("textContent"))

                return self.promo_action_row_data

            current_table_button_web_element = self.wait.until(
                    EC.visibility_of_element_located(self.go_to_the_next_page), 'The next page button in not available')
            current_table_button_web_element.click()


