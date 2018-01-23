import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.Parser import Parser


class BasePage(object):

    main_headers_table = (By.CSS_SELECTOR, 'div.k-grid-header')
    main_content_table = (By.CSS_SELECTOR, 'div.k-grid-content')
    main_footer_table = (By.CSS_SELECTOR, 'div.k-grid-footer')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def get_title_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h2')), 'Title is invisible').text

    def get_title_from_toolbar(self):
        return self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'title')), 'Title is invisible').text

    def enter_value(self, element_locator, value, error_message=None):
        try:
            input = self.wait.until(EC.visibility_of_element_located(element_locator))
            input.clear()
            input.send_keys(value)
            return self
        except:
            raise Exception(error_message)

    def click_and_select_dropdown_option(self, state_dict, state, error_message=None, dropdown_element=None):
        dropdown_element.click()
        try:
            select_frame = WebDriverWait(self.driver, 2).until(EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, "ul[class='k-list k-reset']")))[0]
        except:
            dropdown_element.click()
        try:
            select_frame = self.wait.until(EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, "ul[class='k-list k-reset']")))[0]
            options = select_frame.find_elements_by_css_selector('li[role="option"]')
            self.driver.execute_script("return arguments[0].scrollIntoView();", options[state_dict[state]])
            time.sleep(0.1)  # for click exactly on the option
            options[state_dict[state]].click()
            return self
        except:
            raise Exception(error_message)

    def check_element(self, element_locator, checkbox_name=None):
        checkbox = self.wait.until(EC.element_to_be_clickable(element_locator),
                                   "Checkbox " + str(checkbox_name) + " is not clickable")
        self.driver.execute_script("return arguments[0].scrollIntoView();", checkbox)
        checkbox.click()
        self.wait_spiner_loading()
        checkbox = self.wait.until(EC.element_to_be_clickable(element_locator),
                                   "Checkbox " + str(checkbox_name) + " is not clickable")
        if not checkbox.is_selected():
            raise Exception('Checkbox ' + checkbox_name + ' had not been checked')
        return self

    def uncheck_element(self, element_locator, checkbox_name=None):
        checkbox = self.wait.until(EC.element_to_be_clickable(element_locator),
                                   "Checkbox " + str(checkbox_name) + " is not clickable")
        self.driver.execute_script("return arguments[0].scrollIntoView();", checkbox)
        checkbox.click()
        self.wait_spiner_loading()
        checkbox = self.wait.until(EC.element_to_be_clickable(element_locator),
                                   "Checkbox " + str(checkbox_name) + " is not clickable")
        if checkbox.is_selected():
            raise Exception('Checkbox ' + checkbox_name + ' had not been unchecked')
        return self

    def get_link_from_cell(self, cell_element, error_message=None):
        try:
            link = WebDriverWait(cell_element, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
            return link
        except:
            raise Exception(error_message)

    def click_link_from_cell(self, cell_element, error_message=None):
        link = self.get_link_from_cell(cell_element, error_message)
        self.driver.execute_script("return arguments[0].scrollIntoView();", link)
        link.click()

    def get_visible_element(self, element_locator, error_message=None):
        return self.wait.until(EC.visibility_of_element_located(element_locator), error_message)

    def get_text_from_element(self, element_locator, error_message=None):
        return self.wait.until(EC.presence_of_element_located(element_locator), error_message).text

    def is_element_present(self, element_locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(element_locator))
            if 'display: none;' in element.get_attribute('style'):
                return False
            else:
                return True
        except:
            return False

    def get_all_notification_text(self):
        notification = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'k-notification-wrap')),
            'Notification is not visible')
        message_list = []
        for element in notification:
            message_list.append(element.text)
        return message_list

    def get_last_notification_text(self):
        el = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'k-notification-wrap')),
            'Notification is not visible')
        return el[len(el) - 1].text

    def wait_for_url_contain(self, expected_url, error=None):
        WebDriverWait(self.driver, 5).until(EC.url_contains(expected_url), error)

    def wait_for_url_matches(self, expected_url, error=None):
        WebDriverWait(self.driver, 5).until(EC.url_matches(expected_url), error)

    def get_widget_window(self, error=None):
        return self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div.k-window')), error)[0]

    def close_widget_window(self, error=None):
        close_btn = WebDriverWait(self.get_widget_window(error), 5) \
            .until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[class="k-icon k-i-close"]')), error)
        close_btn.click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'k-window')),
                                            'Pop up window was not closed')
        return self

    def wait_spiner_loading(self):
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[class="k-loading-image"]')))
        return self

    def multiple_select_by_index(self, index_list=None, select_name=None):
        """
        If Index_list is None all options will be selected
        :type index_list: list
        """
        options = self.wait.until(EC.visibility_of_any_elements_located
                                  ((By.CSS_SELECTOR, 'ul[class="k-list k-reset"]')),
                                  'There is no dropdown options for "{0}"'.format(str(select_name)))[0] \
            .find_elements_by_css_selector('li[role="option"]')
        if index_list is None:
            index_list = range(len(options))
        try:
            for i in index_list:
                self.driver.execute_script("return arguments[0].scrollIntoView();", options[i])
                options[i].click()
        except IndexError:
            print("{0} dropdown has not so many options".format(str(select_name)))
        # close multiselect
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="b-header__title"]')),
                        '"Globus Promo Tool" header is not visible').click()
        return self

    def is_button_disabled(self, locator, button_name=None):
        button = self.wait.until(EC.presence_of_element_located(locator), '"{0}" button is absent'.format(button_name))
        if 'k-state-disabled' in button.get_attribute('class'):
            return True
        else:
            return button.get_attribute('disabled')

    def get_context_menu(self, element, error_message=None):
        self.driver.execute_script("return arguments[0].scrollIntoView();", element)
        ActionChains(self.driver).context_click(element).perform()
        return self.wait.until(EC.visibility_of_any_elements_located
                               ((By.CSS_SELECTOR, 'div[class="k-animation-container"]')),
                               error_message)[0]

    def get_dialog_message(self, error_message='Message text in the dialog pop up is missing'):
        message = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div[data-role="dialog"]')),
                                  error_message)[0].text
        return message

    def click_ok_to_pop_up_dialog(self):
        self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'ul[role="toolbar"]')),
                        '"OK" button is not clickable')[0].click()
        return self

    def click_yes_to_pop_up_dialog(self):
        toolbar = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'ul[role="toolbar"]')),
                                  'Buttons group is not visible in Message pop up')[0]

        WebDriverWait(toolbar, 5).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'li[role="button"]')),
                                        'Buttons are not visible in Message pop up')[0].click()
        return self

    def click_no_to_pop_up_dialog(self):
        toolbar = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'ul[role="toolbar"]')),
                                  'Buttons group is not visible in Message pop up')[0]

        WebDriverWait(toolbar, 5).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'li[role="button"]')),
                                        'Buttons are not visible in Message pop up')[1].click()
        return self

    def click_element(self, element_locator, error_massege):
        self.wait.until(EC.element_to_be_clickable(element_locator), error_massege)
        return self

    def get_table_content(self, error_message='Tables content is absent'):
        '''Returns the webelement of table's content without additional elements'''
        return self.wait.until(EC.presence_of_element_located(self.main_content_table), error_message) \
            .find_element_by_tag_name('table')

    def get_headers_table(self, error_message='Headers table is absent'):
        return self.wait.until(EC.presence_of_element_located(self.main_headers_table), error_message)
