from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Pages.page_planning.PagePlanning import PagePlanning
from Pages.positions_view.PositionsView import PositionsView
from utilities.BaseWidget import BaseWidget
from utilities.Table import TableFilter
from utilities.Table import Table
from selenium.webdriver.support.wait import WebDriverWait

class PagesViewWidget(BaseWidget):

    new_page_button = (By.CSS_SELECTOR, 'button.button-success')
    delete_button = (By.CSS_SELECTOR, 'button.button-danger')

    position_button = (By.CSS_SELECTOR, 'div[data-role="elink"]')
    planning_button = (By.CSS_SELECTOR, 'div[data-role="elink"]')


    """HEADERS"""
    assortment_header = (By.CSS_SELECTOR, 'th[data-field="Assortment"]')



    promo_page = {
        'Number': 0,
        'Name': '',
        'Assortment': '',
        'Position': 0,
        'Planned turnover': 0,
        'Planned margin %': 0,
        'Planned gross profit': 0,
        'Planned contributions from suppliers': 0,
        'Planned total gross profit': 0,
        'Compared Position': 0,
        'Compared planned turnover': '',
        'Compared planned margin %': '',
        'Compared planned gross profit': '',
        'Compared planned contributions from suppliers': '',
        'Compared planned total gross profit': ''
    }

    def __init__(self, driver):
        super(PagesViewWidget, self).__init__(driver,
                                              (By.CSS_SELECTOR, 'div.b-list-of-promo-pages.k-grid.k-widget'),
                                              'Pages view')
    def get_tabel_labels(self):
        table_filter = TableFilter(self.driver)
        table = table_filter.get_all_headers_table()[0]
        print(table_filter.get_all_headers_from_table_as_text(table))

    def choose_assortment(self, row_index:int):
        table = Table(self.driver, self.get_table_content())
        assortment = table.get_row(row_index)[table.get_column_index(self.assortment_header)]
        self.driver.execute_script("return arguments[0].scrollIntoView();", assortment)
        assortment.click()
        pop_up = WebDriverWait(self.driver, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div.k-window')), '"Assortment" window is invisible')[0]
        list = WebDriverWait(pop_up, 5).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'span[class="k-in"]')),
                               'There is no option for Assortment')
        for el in list:
            el.click()
        close_btn = WebDriverWait(pop_up, 5) \
            .until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[class="k-icon k-i-close"]')), 'There is no close button on Assortment pop up')
        close_btn.click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'k-window')),
                                            'Pop up window was not closed')
        return self

    def get_assortment_value(self, row):
        assortment_field = row[Table(self.driver, self.get_table_content()).get_column_index(self.assortment_header)]
        self.driver.execute_script("return arguments[0].scrollIntoView();", assortment_field)
        list_elements = assortment_field.find_elements_by_tag_name('li')
        list_options_text = []
        for el in list_elements:
            list_options_text.append(el.text)
        return list_options_text

    def add_new_page(self):
        new_page_button = self.wait.until(EC.visibility_of_element_located(self.new_page_button), 'New page button is invisible')
        self.wait_element_has_not_state(self.new_page_button, 'k-state-disabled',
                                        '"New page" button still be disabled')
        new_page_button.click()
        self.wait_spiner_loading()
        return self

    def delete_page_with_yes_or_no_option(self, row_index: int, yes_no_option: str):
        delete_button = self.wait.until(EC.visibility_of_element_located(self.delete_button), 'Delete button is not visible')
        table = Table(self.driver, self.get_table_content())
        number_cell = table.get_row(row_index)[2]
        number_cell.click()
        if self.is_button_disabled(self.delete_button, 'Delete'):
            raise Exception('Delete button is disabled after highlighting row')
        delete_button.click()
        # TODO yes_no_option
        return self

    def get_position_page_by_row_number(self, row_index=0):
        table = Table(self.driver, self.get_table_content())
        position_cell = table.get_row(row_index)[1]
        button = WebDriverWait(position_cell, 5)\
            .until(EC.presence_of_element_located(self.position_button), 'Position button is absent')
        self.driver.execute_script("return arguments[0].scrollIntoView();", button)
        button.click()
        return PositionsView(self.driver)

    def get_planning_page_by_row_index(self, row_index=0):
        table = Table(self.driver, self.get_table_content())
        planning_cell = table.get_row(row_index)[0]
        button = WebDriverWait(planning_cell, 5)\
            .until(EC.presence_of_element_located(self.planning_button), 'Position button is absent')
        self.driver.execute_script("return arguments[0].scrollIntoView();", button)
        button.click()
        return PagePlanning(self.driver)




    def click_on_page_planning_by_its_number(self, page_number):
        """
        This method is used when we want to click on the page planning link found by the number of page in Page view

        :param page_number: the page number can be found in Number column of the Page view
        :return: nothing
        """
        table_web_element = self.get_table_content()
        table_instance = Table(self.driver, table_web_element)

        planning_page_number = table_instance.count_rows()

        # there should be at least 1 page planning and the input page number shouldn't exceed the number of pages
        if planning_page_number > 0 and int(page_number) <= planning_page_number:

            # page_planning_row_element - is web element of the cell where our page is located
            # (2, "1", 0) - first parameter is column index in Page view(column "Number" has index 2)
            # 2nd parameter is the serial number of page planning we need to open (converted to string)
            # 3rd parameter is the column index where the page link is located(in our case the page planning link is in the 1st column)
            page_planning_row_element = table_instance.get_web_element_of_cell_or_row_by_column_index_and_text_in_cell(
                                                                                                2, str(page_number), 0)
            # click on the link of the page found by its number
            page_planning_row_element.click()

    def get_page_planning_data_by_its_number(self, page_number):
        """
        This method is used when we want to get the data related to page planning found by the number of page in Page view

        :param page_number: the page number can be found in Number column of the Page view
        :return: dictionary with the page parameters according to the column names and row values
        """
        table_web_element = self.get_table_content()
        table_instance = Table(self.driver, table_web_element)

        planning_page_number = table_instance.count_rows()

        # there should be at least 1 page planning and the input page number shouldn't exceed the number of pages
        if planning_page_number > 0 and int(page_number) <= planning_page_number:

            # page_planning_row_element - is web element of the cell where our page is located
            # (2, "1", 0) - first parameter is column index in Page view(column "Number" has index 2)
            # 2nd parameter is the serial number of page planning we need to open (converted to string)
            # 3rd parameter is the column index where the page link is located(in our case the page planning link is in the 1st column)
            # if the 4th parameter is True , method will return the webelement of full row with the page
            page_planning_row_element = table_instance.get_web_element_of_cell_or_row_by_column_index_and_text_in_cell(
                                                                                        2, str(page_number), 0, True)
            # page_planning_row_element

            self.promo_page['Number'] = int(page_planning_row_element[2].get_attribute("textContent"))
            # self.promo_page['Name'] = page_planning_row_element[3].get_attribute("textContent")
            self.promo_page['Assortment'] = page_planning_row_element[4].find_element_by_tag_name("option").get_attribute("textContent")
            self.promo_page['Position'] = page_planning_row_element[5].find_element_by_tag_name("input").get_attribute("value")

            planned_turn_over_str = page_planning_row_element[6].find_element_by_tag_name("div").get_attribute('data-value')
            if planned_turn_over_str != 'null':
                self.promo_page['Planned turnover'] = int(planned_turn_over_str)

            planned_contributions_from_suppliers = page_planning_row_element[9].find_element_by_tag_name("div").get_attribute('data-value')
            if planned_contributions_from_suppliers != 'null':
                self.promo_page['Planned contributions from suppliers'] = int(planned_contributions_from_suppliers)

            self.promo_page['Planned total gross profit'] = int(page_planning_row_element[10].
                                                                get_attribute('textContent').replace(u"\u00A0", ""))

            compared_promo_position = page_planning_row_element[11].get_attribute("textContent").\
                                                                                            replace(u"\u00A0", "")
            self.promo_page['Compared Position'] = int(compared_promo_position)

            compared_planned_turnover = page_planning_row_element[12].get_attribute("textContent").\
                                                                                            replace(u"\u00A0", "")
            self.promo_page['Compared planned turnover'] = int(compared_planned_turnover)

            compared_planned_margin = page_planning_row_element[13].get_attribute('textContent')
            self.promo_page['Compared planned margin %'] = (compared_planned_margin)

            compared_planned_gross_profit = page_planning_row_element[14].get_attribute('textContent')
            self.promo_page['Compared planned gross profit'] = (compared_planned_gross_profit)

            compared_planned_contributions_from_suppliers = page_planning_row_element[15].get_attribute('textContent')
            self.promo_page['Compared planned contributions from suppliers'] = (compared_planned_contributions_from_suppliers)

            compared_planned_total_gross_profit = page_planning_row_element[16].get_attribute('textContent')
            self.promo_page['Compared planned total gross profit'] = (compared_planned_total_gross_profit)


            return self.promo_page

