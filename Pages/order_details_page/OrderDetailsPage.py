import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from BasePage import BasePage
from utilities.Table import Table

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OrderDetailsPage(BasePage):

    save_button = (By.CSS_SELECTOR, 'a.button-success.k-button.k-button-icontext')
    left_table = (By.CSS_SELECTOR, 'div.k-grid-content-locked')

    """Left table fields"""
    ordered_qty = (By.CSS_SELECTOR, 'div[data-field="OrderedQty"]')
    split_button = (By.CSS_SELECTOR, 'div[data-field="Split"]')



    def get_left_table_content(self):
        return self.wait.until(EC.presence_of_element_located(self.left_table),
                               'Left table content for order detail page is absent')


    def select_position(self, row_index):
        try:
            table = Table(self.driver, self.get_left_table_content())
            row = table.get_row_as_webelement(row_index)
            self.driver.execute_script("return arguments[0].scrollIntoView();", row)
            row.click()
            self.wait_spiner_loading()
            time.sleep(0.1)
            selected_row = table.get_row_as_webelement(row_index)
            assert selected_row.get_attribute('aria-selected') in 'true'
        except:
            raise Exception('Row was not selected')
        return selected_row


    def enter_value(self, selected_row_webelement, element_locator, value, error_message=None):
        try:
            input = WebDriverWait(selected_row_webelement, 5).until(EC.presence_of_element_located(element_locator))\
                .find_element_by_tag_name('input')
            input.click()
            input.clear()

            input.send_keys(value)
            input.send_keys(Keys.ENTER)
            self.wait_spiner_loading()

            return self
        except:
            raise Exception(error_message)

    def click_split_button(self, selected_row_webelement):
        split_button = WebDriverWait(selected_row_webelement, 5).until(EC.visibility_of_element_located(self.split_button),
                                                        'Split button is absent')
        try:
            split_button.click()
            self.wait_spiner_loading()
        except:
            raise Exception('Split button is not clickable')
        return self

    def click_save(self):
        self.wait_spiner_loading()
        button = self.wait.until(EC.visibility_of_element_located(self.save_button),
                                 'Save button is missing')
        self.wait_element_has_not_state(self.save_button, 'k-state-disabled', 'Save button is disabled')
        button.click()
        self.wait_spiner_loading()
        return self

