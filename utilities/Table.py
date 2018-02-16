import time
from selenium.common.exceptions import InvalidElementStateException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from BasePage import BasePage
from utilities.Parser import Parser


class TableFilter(object):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def call_a_dropdown_menu(self, header_element):
        """
        Scroll to header element. Click on arrow in header to call a dropdown menu.
        :param header_element: webelement of column header
        :return:
        """
        self.driver.execute_script("return arguments[0].scrollIntoView();", header_element)
        arrow_icon = header_element.find_element_by_class_name('k-i-arrowhead-s')
        arrow_icon.click()
        time.sleep(0.5)

    def hide_a_dropdown_menu(self, header_element):
        self.driver.execute_script("return arguments[0].scrollIntoView();", header_element)
        arrow_icon = header_element.find_element_by_class_name('k-i-arrowhead-s')
        arrow_icon.click()

    def sort_ascending(self, header_element):
        """
        :param header_element: webelement of column header
        :return: True if sort ascending has selected state, otherwise False
        """
        self.call_a_dropdown_menu(header_element)
        sort_element = self.wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'k-sort-asc')))[0]
        sort_element.click()
        if 'k-state-selected' in sort_element.get_attribute('class'):
            return True
        else:
            return False

    def sort_with_mouse(self, header_element):
        """
        :param header_element: webelement of column header
        :return: True if sort ascending has selected state, otherwise False
        """
        if Parser().get_browser_name() is 'IE':
            # self.driver.execute_script("arguments[0].click();", header_element)
            # self.driver.execute_script("arguments[0].click();", header_element)
            # self.driver.execute_script("arguments[0].click();", header_element)
            # self.driver.execute_script("arguments[0].click();", header_element)
            actionChains = ActionChains(self.driver)
            actionChains.double_click(header_element).perform()
            # actionChains.double_click(header_element).perform()
        else:
            actionChains = ActionChains(self.driver)
            actionChains.double_click(header_element).perform()
            # actionChains.double_click(header_element).perform()
            # header_element.click()
            # header_element.click()
            # header_element.click()
            # header_element.click()

    def sort_descending(self, header_element):
        """
        :param header_element: webelement of column header
        :return: True if sort descending has selected state, otherwise False
        """
        self.call_a_dropdown_menu(header_element)
        sort_element = self.wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'k-sort-desc')))[0]
        sort_element.click()
        if 'k-state-selected' in sort_element.get_attribute('class'):
            return True
        else:
            return False

    def columns_settings(self, header, elements):
        """
        :param header: webelement of column header
        :param elements: locators to be checked/unchecked
        :return: list of True/False for checked/unchecked state
        """
        elements_to_click = []
        result = []
        if type(elements) is not list:
            elements_to_click.append(elements)
        else:
            elements_to_click = elements

        self.call_a_dropdown_menu(header)
        columns = self.wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'k-columns-item')))[0]
        columns.click()
        time.sleep(0.5)

        for checkbox in elements_to_click:
            el = self.wait.until(EC.visibility_of_any_elements_located(checkbox))[0]
            el.click()
            result.append(el.is_selected())
        self.hide_a_dropdown_menu(header)
        return result

    def is_column_displayed(self, header_locator):
        column = self.wait.until(EC.presence_of_element_located(header_locator))
        style = column.get_attribute('style')
        if 'display: none;' in style:
            return False
        else:
            return True

    def is_checkbox_enabled(self, checkbox_locator):
        checkbox = self.wait.until(EC.visibility_of_any_elements_located(checkbox_locator))[0]
        if checkbox.is_enabled():
            return True
        else:
            return False

    def get_filter_form(self, header):
        """ Call Filtering form
        :param header: webelement of column header
        :return:
        """
        self.call_a_dropdown_menu(header)
        try:
            filter_btn = WebDriverWait(self.driver, 2).until(EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, 'li.k-item.k-filter-item.k-state-default.k-last')))[0]
        except:
            time.sleep(0.1)
            self.call_a_dropdown_menu(header)
            filter_btn = self.wait.until(EC.visibility_of_any_elements_located
                                         ((By.CSS_SELECTOR, 'li.k-item.k-filter-item.k-state-default.k-last')))[0]
        time.sleep(0.1)  # for click exactly on Filter option
        filter_btn.click()
        return self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div.k-filterable.k-content')),
                               'Filterable content element is absent')[0]

    def submit_filtering(self):

        filter_btn = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                                                            'button[type="submit"]')))[0]
        if filter_btn.is_enabled():
            try:
                filter_btn.click()
            except:
                time.sleep(0.1)
                filter_btn.click()
        else:
            raise InvalidElementStateException('In submit Filter button is not clickable')

    def clear_filter_form(self, header):
        self.get_filter_form(header)
        clear_btn = self.wait.until(EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'button[type="reset"]')))[0]
        if clear_btn.is_enabled():
            clear_btn.click()
        else:
            raise InvalidElementStateException('In filter Clear button is not clickable')

    def choose_and_or_option(self, and_or_state=None):
        if and_or_state is not None:
            and_or_dropdown = WebDriverWait(self.driver, 15).until(EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, 'span.k-widget.k-dropdown.k-header.k-filter-and')))[0]
            try:
                and_or_dropdown.click()
            except:
                time.sleep(0.1)
                and_or_dropdown.click()
            select_and_or_main = self.wait.until(EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, "ul[class='k-list k-reset']")))[0]
            and_or_options = WebDriverWait(select_and_or_main, 5).until(EC.visibility_of_all_elements_located
                                                                        ((By.CSS_SELECTOR, 'li[role="option"]')))
            if and_or_state in 'and':
                try:
                    and_or_options[0].click()
                except:
                    time.sleep(0.1)
                    and_or_options[0].click()
            if and_or_state in 'or':
                and_or_options[1].click()

    def select_option_from_dropdown(self, state_dict, state):
        main_select = self.wait.until(EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, "ul[class='k-list k-reset']")))[0]
        options = main_select.find_elements_by_css_selector('li[role="option"]')
        self.driver.execute_script("return arguments[0].scrollIntoView();", options[state_dict[state]])
        time.sleep(0.1)  # for click exactly on the option
        options[state_dict[state]].click()

    def filter_from_header_by_string(self, header, first_state=None, first_state_string=None, second_state=None,
                                     second_state_string=None, and_or_state=None):
        """
        Filtering by string value. Filtering occurs only on the transmitted data.
        :param header: webelement of column header
        :param first_state: string representation of dropdown option
        :param first_state_string: value for input
        :param second_state: string representation of dropdown option
        :param second_state_string: value for input
        :param and_or_state: string representation of dropdown option
        :return:
        """
        state = {
            'Is equal to': 0,
            'Is not equal to': 1,
            'Starts with': 2,
            'Contains': 3,
            'Does not contain': 4,
            'Ends with': 5,
            'Is null': 6,
            'Is not null': 7,
            'Is empty': 8,
            'Is not empty': 9
        }
        state_dropdown = (By.CSS_SELECTOR, 'span[class="k-widget k-dropdown k-header"]')

        filter_content = self.get_filter_form(header)
        filter_wait = WebDriverWait(filter_content, 5)

        if first_state is not None:
            first_state_dropdown = filter_wait.until(EC.visibility_of_any_elements_located(state_dropdown))[0]
            first_state_dropdown.click()

            self.select_option_from_dropdown(state_dict=state, state=first_state)
        if first_state_string is not None:
            first_input = filter_wait.until(
                EC.visibility_of_any_elements_located(
                    (By.CSS_SELECTOR, 'input[data-bind="value:filters[0].value"]')))[0]
            first_input.clear()
            first_input.send_keys(first_state_string)
        self.choose_and_or_option(and_or_state)
        if second_state is not None:
            second_state_dropdown = filter_wait.until(EC.visibility_of_any_elements_located(state_dropdown))[1]
            second_state_dropdown.click()
            self.select_option_from_dropdown(state_dict=state, state=second_state)
        if second_state_string is not None:
            second_input = filter_wait.until(
                EC.visibility_of_any_elements_located(
                    (By.CSS_SELECTOR, 'input[data-bind="value: filters[1].value"]')))[0]
            second_input.clear()
            second_input.send_keys(second_state_string)
        self.submit_filtering()

    def filter_from_header_by_radiobutton(self, header, boolean=True):
        self.get_filter_form(header)
        filtermenu = self.wait.until(EC.visibility_of_any_elements_located
                                     ((By.CSS_SELECTOR, 'div[class="k-filterable k-content"]')))[0]
        # labels = filtermenu.find_elements_by_tag_name('label')
        radiobuttons = filtermenu.find_elements_by_css_selector('input[type = "radio"]')
        yes_radiobutton = radiobuttons[0]
        no_radiobutton = radiobuttons[1]
        if boolean:
            yes_radiobutton.click()
        else:
            no_radiobutton.click()
        self.submit_filtering()

    def filter_from_header_by_number(self, header, first_state=None, first_state_string=None, second_state=None,
                                     second_state_string=None, and_or_state=None):
        """
        Filtering by integer value. Filtering occurs only on the transmitted data.
        :param header: webelement of column header
        :param first_state: string representation of dropdown option
        :param first_state_string: value for input
        :param second_state: string representation of dropdown option
        :param second_state_string: value for input
        :param and_or_state: string representation of dropdown option
        :return:
        """
        state = {
            'Is equal to': 0,
            'Is not equal to': 1,
            'Is greater than or equal to': 2,
            'Is greater than': 3,
            'Is less than or equal to': 4,
            'Is less than': 5,
            'Is null': 6,
            'Is not null': 7
        }
        state_dropdown = 'span[class="k-widget k-dropdown k-header"]'

        self.get_filter_form(header)
        filter_form = self.wait.until(EC.visibility_of_any_elements_located
                                      ((By.CSS_SELECTOR, 'div[class="k-filterable k-content"]')))[0]
        if first_state is not None:
            first_state_dropdown = filter_form.find_elements_by_css_selector(state_dropdown)[0]
            first_state_dropdown.click()
            self.select_option_from_dropdown(state_dict=state, state=first_state)
        if first_state_string is not None:
            first_input = filter_form.find_elements(By.CSS_SELECTOR, 'input[class="k-formatted-value k-input"]')[0]
            '''In order to bypass the occurrence of an error when clearing the field'''
            first_input.send_keys('')
            ActionChains(self.driver).key_down(Keys.LEFT_CONTROL).send_keys('a').key_up(Keys.LEFT_CONTROL) \
                .send_keys(first_state_string).perform()
        self.choose_and_or_option(and_or_state)
        if second_state is not None:
            second_state_dropdown = filter_form.find_elements_by_css_selector(state_dropdown)[1]
            second_state_dropdown.click()
            self.select_option_from_dropdown(state_dict=state, state=second_state)
        if second_state_string is not None:
            second_input = filter_form.find_elements(By.CSS_SELECTOR, 'input[class="k-formatted-value k-input"]')[1]
            second_input.send_keys('')
            ActionChains(self.driver).key_down(Keys.LEFT_CONTROL).send_keys('a').key_up(Keys.LEFT_CONTROL) \
                .send_keys(second_state_string).perform()
        self.submit_filtering()

    def filter_from_header_by_date(self, header, first_state=None, first_date=None, second_state=None,
                                   second_date=None, and_or_state=None):
        """
        Filtering by date value. Filtering occurs only on the transmitted data.
        :param header: webelement of column header
        :param first_state: string representation of dropdown option
        :param first_date: value for input
        :param second_state: string representation of dropdown option
        :param second_date: value for input
        :param and_or_state: string representation of dropdown option
        :return:
        """
        state = {
            'Is equal to': 0,
            'Is not equal to': 1,
            'Is after or equal to': 2,
            'Is after': 3,
            'Is before or equal to': 4,
            'Is before': 5,
            'Is null': 6,
            'Is not null': 7
        }
        state_dropdown = 'span[class="k-widget k-dropdown k-header"]'

        self.get_filter_form(header)
        filter_form = self.wait.until(EC.visibility_of_any_elements_located
                                      ((By.CSS_SELECTOR, 'div[class="k-filterable k-content"]')))[0]
        if first_state is not None:
            first_state_dropdown = filter_form.find_elements_by_css_selector(state_dropdown)[0]
            first_state_dropdown.click()
            self.select_option_from_dropdown(state_dict=state, state=first_state)
        if first_date is not None:
            first_input = filter_form.find_element(By.CSS_SELECTOR, 'input[data-bind="value:filters[0].value"]')
            '''In order to bypass the occurrence of an error when clearing the field'''
            first_input.clear()
            first_input.send_keys(first_date)
        self.choose_and_or_option(and_or_state)
        if second_state is not None:
            second_state_dropdown = filter_form.find_elements_by_css_selector(state_dropdown)[1]
            second_state_dropdown.click()
            self.select_option_from_dropdown(state_dict=state, state=second_state)
        if second_date is not None:
            second_input = filter_form.find_element(By.CSS_SELECTOR, 'input[data-bind="value: filters[1].value"]')
            second_input.clear()
            second_input.send_keys(second_date)
        self.submit_filtering()

    def filter_from_header_by_percent(self):
        # TODO filtering from header by percent value
        pass

    def change_column_location(self, changing_header, new_location_header):

        if Parser().get_browser_name() is 'IE':
            pass
        else:
            ActionChains(self.driver).drag_and_drop(changing_header, new_location_header).perform()

    def wait_table_to_load(self, table_element):
        WebDriverWait(table_element, 15).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[class="k-loading-image"]')), 'Table was not loaded')
        return self

    def get_all_headers_table(self):
        BasePage(self.driver).wait_spiner_loading()
        return self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'k-grid-header-wrap')))

    def get_all_headers_from_table(self, table, error='There are no headers in table'):
        return WebDriverWait(table, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'th[role="columnheader"]')), error)

    def get_all_headers_from_table_as_text(self, table):

        all_headers_tmp = WebDriverWait(table, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'th')))
        list_of_headers = []

        for item in all_headers_tmp:
            self.driver.execute_script("return arguments[0].scrollIntoView(true);", item)

            if len(item.text) == 0:
                splited_string = item.text
            elif item.text.find("\n") < 0:
                splited_string = item.text
            elif item.text.find("\n") >= 0:
                splited_string = (item.text).split("\n", 1)[1]

            list_of_headers.append(splited_string)
        return list_of_headers

    def get_context_menu(self, header):
        self.driver.execute_script("return arguments[0].scrollIntoView();", header)
        ActionChains(self.driver).context_click(header).perform()
        return self.wait.until(EC.visibility_of_any_elements_located
                               ((By.CSS_SELECTOR, 'div[class="k-animation-container"]')),
                               'Context menu for "' + header.get_attribute('title') + '" is absent')[0]

    def export_to_pdf(self, header):
        menu = self.get_context_menu(header)
        try:
            el = WebDriverWait(menu, 2).until(EC.visibility_of_any_elements_located
                                              ((By.CSS_SELECTOR, 'li[data-export-type="PDF"]')),
                                              'Options from context menu for "{0}" is invisible'
                                              .format(header.get_attribute('title')))[0]
        except:
            menu = self.get_context_menu(header)
            el = WebDriverWait(menu, 5).until(EC.visibility_of_any_elements_located
                                              ((By.CSS_SELECTOR, 'li[data-export-type="PDF"]')),
                                              'Options from context menu for "{0}" is invisible'
                                              .format(header.get_attribute('title')))[0]
        if 'k-state-disabled' in el.get_attribute('class'):
            raise Exception('Option "Export to PDF" from context menu "{0}" is disabled'.format(header.get_attribute
                                                                                                ('title')))
        el.click()
        return self

    def export_to_excel(self, header):
        menu = self.get_context_menu(header)
        try:
            el = WebDriverWait(menu, 2).until(EC.visibility_of_any_elements_located
                                              ((By.CSS_SELECTOR, 'li[data-export-type="Excel"]')),
                                              'Options from context menu for "{0}" is invisible'
                                              .format(header.get_attribute('title')))[0]
        except:
            menu = self.get_context_menu(header)
            el = WebDriverWait(menu, 5).until(EC.visibility_of_any_elements_located
                                              ((By.CSS_SELECTOR, 'li[data-export-type="Excel"]')),
                                              'Options from context menu for "{0}" is invisible'
                                              .format(header.get_attribute('title')))[0]
        if 'k-state-disabled' in el.get_attribute('class'):
            raise Exception('Option "Export to Excel" from context menu "{0}" is disabled'.format(header.get_attribute
                                                                                                  ('title')))
        el.click()
        if Parser().get_browser_name() is 'IE':
            time.sleep(2)

            """handle = GetForegroundWindow()
            app = Application().connect(handle=handle)
            window = app['Internet Explorer']['Frame Notification Bar']
            #keyboard.SendKeys('{VK_MENU}n')
            window.type_keys('{VK_CONTROL}n')
            time.sleep(1)
            #app['Internet Explorer'].type_keys('{SPACE}')"""

            # menu.send_keys(Keys.CONTROL + 'a')
            action = ActionChains(self.driver)
            action.key_down(Keys.LEFT_ALT).perform()
            time.sleep(1)
            action.send_keys('n').key_up(Keys.LEFT_ALT).perform()

            # menu.send_keys(Keys.CONTROL + 'a')
            # menu.send_keys(Keys.SPACE)

        return self

    def wait_for_prepare_pdf(self):
        WebDriverWait(self.driver, 180, 1).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, 'k-loading-pdf-progress')),
            'Loading bar did not disappeared')


class Table:
    nested_table_parent = (By.XPATH, "(//tbody[@role='rowgroup'])")

    def __init__(self, driver, table_content):
        """
        :param driver:
        :param table_content: webelement of table content
        """
        self.driver = driver
        self.table_element = table_content
        self.wait = WebDriverWait(self.table_element, 15)

    def count_rows(self):
        """
        :return: number of rows
        """
        rows = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        return len(rows)

    def count_master_rows(self):
        """
        :return: number of rows in main table, exclude nested rows
        """
        rows = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'tr.k-master-row')))
        return len(rows)

    def get_all_cells_element(self):
        """
        :return: two-dimensional list of webelements. Each webelement is cell 
        """
        cells_list = []
        try:
            rows = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        except:
            return cells_list

        for row in rows:
            cells = row.find_elements_by_tag_name('td')
            cells_list.append(cells)
        return cells_list

    def find_web_element_text_from_all_cells(self, cells_list, text_list_to_search):
        """
        Search predefined text in the table and makes sure that those text strings are located in the same row.
        :param cells_list: all rows from the table as a list of webelements
        :param text_list_to_search: list of strings which has to be found in one row

        :return: True - if the row with predefined values was found, False - otherwise
        """
        # number of cell values which has to be found in the table
        items_number_to_search = len(text_list_to_search)
        # verify if the table is not empty
        if len(cells_list) > 0:

            # loop for iteration of double list cells_list[][] which is representation of the table from web grid
            for val in cells_list:
                # val is representation of the whole row from grid, verify if the row is not empty
                if len(val) > 0:
                    # in row_text_list we save the list of text, which was extracted from the row
                    row_text_list = []
                    for val_inner in val:
                        row_text_list.append(val_inner.get_attribute("textContent"))

                    # counter which calculates how many text strings were found in the list representing one row
                    items_number_already_found = 0
                    for text in text_list_to_search:
                        for web_text in row_text_list:
                            # if the text extracted from webelement and text from user are the same
                            # then we incremented the counter of found strings
                            if text.strip().lower() == web_text.strip().lower():
                                items_number_already_found = items_number_already_found + 1
                    # if all strings were found in one row , then it is the row which we were looking for
                    if items_number_to_search == items_number_already_found:
                        return True
        return False

    def get_row(self, index=0):
        """
        :type index: int
        :param index: serial number of the row, for default get first row
        :return: list of cell webelements are contained in row
        """
        row = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))[index]
        cells = row.find_elements_by_tag_name('td')
        return cells

    def get_master_row(self, index=0):
        """
        :type index: int
        :param index: serial number of the row, for default get first row
        :return: list of cell webelements are contained in row
        """
        row = self.wait.until(EC.presence_of_all_elements_located
                                                          ((By.CSS_SELECTOR, 'tr.k-master-row')))[index]
        cells = row.find_elements_by_tag_name('td')
        return cells

    def get_row_as_webelement(self, index=0):
        """
        :param index: serial number of the row, for default get first row
        :return: single webelement of row
        """
        try:
            row = self.wait.until(EC.presence_of_all_elements_located
                                                              ((By.TAG_NAME, 'tr')))[index]
        except Exception as error:
            raise Exception('There is not {}-th row. {}'.format(index+1, error))
        return row

    def get_master_row_as_webelement(self, index=0):
        """
        :param index: serial number of the row, for default get first row
        :return: single webelement of master row
        """
        try:
            row = self.wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'tr.k-master-row')))[index]
        except Exception as error:
            raise Exception('There is not {}-th row. {}'.format(index+1, error))
        return row

    def get_row_by_id(self, id_row, column=0):
        """
        :param id_row: item id to find row
        :param column: in which column should find id
        :return: list of webelements of row with the desired item id
        """
        first = 0
        last = self.count_rows() - 1
        i = 0
        while True:
            if len(self.get_row(first)[column].text) > 0 and int(self.get_row(first)[column].text) == int(id_row):
                return self.get_row(first)
            if len(self.get_row(last)[column].text) > 0 and int(self.get_row(last)[column].text) == int(id_row):
                return self.get_row(last)
            if len(self.get_row(int(last / 2))[column].text) > 0 and int(
                    self.get_row(int(last / 2))[column].text) < int(id_row):
                first = int(last / 2)
                last -= 1
            else:
                last = int(last / 2)
                first += 1
            if i == 50:
                raise Exception('There is no {} id'.format(id_row))
            i += 1

    def get_nested_columns(self, column_number: int=0):

        parent_elem = WebDriverWait(self.table_element, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME,
                            "td")), 'The nested row cant be located')

        # element_list = parent_elem.find_elements_by_tag_name("td")
        return parent_elem[column_number]

    def wait_table_to_load(self):
        BasePage(self.driver).wait_spiner_loading()
        self.wait.until(EC.visibility_of_any_elements_located((By.TAG_NAME, 'tr')),
                                                    'Table was not loaded')
        return self

    def open_nested_table(self, cell_element):
        self.driver.execute_script("return arguments[0].scrollIntoView();", cell_element)
        expand_webelement = WebDriverWait(cell_element, 5).until(EC.element_to_be_clickable
                                                                 ((By.CSS_SELECTOR, 'a[class="k-icon k-i-expand"]')),
                                                                 'Icon in hierarchy cell is absent')
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", expand_webelement)
        else:
            expand_webelement.click()

        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_any_elements_located((By.CLASS_NAME, 'nested-grid-widget')),
            'Nested table is absent')

    def close_nested_table(self, cell_element):
        self.driver.execute_script("return arguments[0].scrollIntoView();", cell_element)
        WebDriverWait(cell_element, 5).until(EC.element_to_be_clickable
                                             ((By.CSS_SELECTOR, 'a[class="k-icon k-i-collapse"]')),
                                             'Icon in hierarchy cell is absent').click()
        return self

    def get_value_from_input(self, cell_element, error=None):
        input = WebDriverWait(cell_element, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')), error)
        return input.get_attribute('value')

    def is_input_disabled(self, cell_element, error=None):
        input = WebDriverWait(cell_element, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')), error)
        span_parent = WebDriverWait(input, 5).until(EC.presence_of_element_located((By.XPATH, '..')),
                                                    'Span parent element is absent')
        if 'disabled' in span_parent.get_attribute('class'):
            return True
        else:
            return False

    def is_input_in_cell(self, cell_element):
        try:
            WebDriverWait(cell_element, 0).until(EC.presence_of_element_located((By.TAG_NAME, 'input')))
            return True
        except:
            return False

    def get_nested_rows(self, error=None):
        '''For Page planning nested table (child tables can be closed or opened)'''
        parent_elem = WebDriverWait(self.table_element, 5).until(EC.presence_of_element_located(
            (By.XPATH, "(//tbody[@role='rowgroup'])[1]")), error)

        nested_tables_list = parent_elem.find_elements_by_tag_name("tr")

        return nested_tables_list

    def get_opened_nested_tables(self, error=None):
        '''For Page planning nested table when child tables were opened'''
        parent_elem = WebDriverWait(self.table_element, 5).until(EC.presence_of_element_located(
            (By.XPATH, "(//tbody[@role='rowgroup'])[1]")), error)

        nested_tables_list = parent_elem.find_elements_by_xpath('//tr[contains(@class,"k-detail-row")]')

        nested_table_list_res = []

        for nested_table_one in nested_tables_list:
            nested_table_temp = nested_table_one.find_elements_by_tag_name("tbody")
            nested_table_list_res.append(nested_table_temp[0])

        return nested_table_list_res

    def open_all_nested_tables(self):

        nested_tables_list = self.get_nested_rows()

        for nested_element in nested_tables_list:

            self.driver.execute_script("return arguments[0].scrollIntoView(true);", nested_element)
            expand_webelement = WebDriverWait(nested_element, 5).until(EC.element_to_be_clickable
                                                                       ((By.CSS_SELECTOR,
                                                                         'a[class="k-icon k-i-expand"]')),
                                                                       'Icon in hierarchy cell is absent')
            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", expand_webelement)
            else:
                expand_webelement.click()

    def close_all_nested_tables(self, list_of_webelements_nested_tables):

        # nested_tables_list = self.get_nested_tables()

        for nested_element in list_of_webelements_nested_tables:

            self.driver.execute_script("return arguments[0].scrollIntoView(true);", nested_element)

            collapse_webelement = WebDriverWait(nested_element, 5).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a[class="k-icon k-i-collapse"]')), 'Icon in hierarchy cell is absent')

            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", collapse_webelement)
            else:
                collapse_webelement.click()

    def find_element_in_row(self, row_index, element_locator, error='The wanted element is missing in the row'):
        """
        :param row_index: int
        :type element_locator: tuple
        :return: Webelement by locator
        """
        row = self.get_row_as_webelement(row_index)
        return WebDriverWait(row, 5).until(EC.presence_of_element_located(element_locator), error)


    def get_web_element_of_cell_or_row_by_column_index_and_text_in_cell(self, column_inx_of_name, name_to_search,
                                                                        column_inx_with_link, full_row=False):
        """
        This method is used only when we want to get the webelement of cell with link, which later can be used
        for clicking on the link in this row

        :param column_inx_of_name: index number of the column we want to search in
        :param name_to_search: name of the link we would like to find and press on it
        :param column_inx_with_link: the column index where the link is located

        :return: webelement of the the cell with link, otherwise return 0 (int)
        """
        last_index = self.count_rows()
        index_list = [i for i in range(last_index)]

        for inx in index_list:

            row_web = self.get_row(inx)
            cell_web = row_web[column_inx_of_name]
            cell_val = cell_web.get_attribute("textContent")

            if full_row is False and cell_val == name_to_search and column_inx_with_link < len(
                    row_web) and full_row is False:
                return row_web[column_inx_with_link]
            elif cell_val == name_to_search and column_inx_with_link < len(row_web) and full_row is True:
                return row_web
        return 0

    def click_checkbox_in_the_row_by_column_number(self, row_webelement, column_inx: int):
        """
        This method is used to get the webelement of cell from the row webelement by knowing the index of column

        :param column_inx: index number of the column we want to search in
        :param row_webelement: the webelement of row or the list of webelements of cells

        :return: webelement of the the cell
        """
        cell_element = row_webelement

        if type(row_webelement) is not list:
            try:
                cell_webelement_list = WebDriverWait(row_webelement, 5).until(EC.visibility_of_all_elements_located((
                    By.TAG_NAME, 'input')), 'Lock checkbox in the page planning row is not available')
            except:
                return
        else:
            cell_webelement_list = row_webelement

        if len(cell_webelement_list) > 0:
            cell_element = cell_webelement_list[column_inx]

        # "2" - serial number of column where the checkbox for unblocking the position is located
        # cell_element = self.table_element.get_cell_from_list_of_columns(row_webelement, 2)

        self.driver.execute_script("return arguments[0].scrollIntoView(true);", cell_element)

        checkbox_element = WebDriverWait(cell_element, 5).until(EC.element_to_be_clickable((By.TAG_NAME, 'input')))

        self.driver.execute_script("return arguments[0].scrollIntoView(true);", cell_element)

        checkbox_element.click()

        return self

    def get_cell_by_row_and_column_inx(self, row_inx: int=0, column_inx: int=0):
        """
        This method is used to get the webelement of cell from the row webelement by knowing the indexes of row and column

        :param column_inx: index number of the column we want to search in
        :param row_inx: the row index

        :return: webelement of the the cell
        """
        row_webelement = self.get_row_as_webelement(row_inx)

        cell_webelement_list = WebDriverWait(row_webelement, 5).until(EC.visibility_of_all_elements_located((
            By.TAG_NAME, 'td')), 'cell web element in Table is not available')

        return cell_webelement_list[column_inx]

    def get_column_index(self, column_header_locator):
        """
        Method for find out the current location of the column
        :param column_header_locator: header locator of desired column
        :return: int column index
        """
        parent_div = self.wait.until(EC.presence_of_element_located
                                     ((By.XPATH, 'parent::div[contains(@class, "k-grid")]')),
                                     "Can't find parent element for table content")
        header_table = WebDriverWait(parent_div, 5).until(EC.presence_of_element_located(BasePage.main_headers_table),
                                                          'There is not headers table for table content')
        column_header = WebDriverWait(header_table, 5).until(EC.presence_of_element_located(column_header_locator),
                                                             'There is not desired header')
        if 'display: none;' in column_header.get_attribute('style'):
            raise Exception('Desired column is invisible')
        return int(column_header.get_attribute('data-index'))

