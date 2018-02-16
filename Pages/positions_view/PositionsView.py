from selenium.webdriver.common.by import By

from utilities.Table import Table
from selenium.webdriver.support.wait import WebDriverWait
from BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC

from utilities.TreeListPopUp import TreeListPopUp


class PositionsView(BasePage):
    title = (By.CSS_SELECTOR, 'a.title k-button k-state-disabled')
    assortment_field = (By.CSS_SELECTOR, "div[data-role='assortment']")

    """BUTTONS"""
    new_position_button_locator = (By.CSS_SELECTOR, 'a.add-button.button-success')

    delete_button_locator = (
        By.CSS_SELECTOR, "a.delete-button.button-danger.k-button.k-button-icontext[style='visibility: visible;']")

    save_button_locator = (By.CSS_SELECTOR,
                           "a.save-button.button-success")

    back_button_locator = (By.CSS_SELECTOR,
                           "a.back-button")

    def get_title(self):
        return self.get_visible_element(self.title, "Title on Positions View is absent")

    def get_save_button(self):
        return self.get_visible_element(self.save_button_locator, "Button 'Save' is absent in Positions View")

    def get_new_position_button(self):
        return self.get_visible_element(self.new_position_button_locator, "Button 'New position' is absent")

    def get_back_button(self):
        return self.get_visible_element(self.back_button_locator, "Button 'New position' is absent")

    def add_new_position(self):
        button = self.wait.until(EC.visibility_of_element_located(self.new_position_button_locator),
                                 'New position button is missing')
        if self.is_button_disabled(self.new_position_button_locator, 'New position'):
            raise Exception('"New position" button should be active')
        else:
            button.click()
            self.wait_spiner_loading()
        return self

    def click_save(self):
        button = self.wait.until(EC.visibility_of_element_located(self.save_button_locator),
                                 'Save button is missing')
        if self.is_button_disabled(self.save_button_locator, 'Save'):
            raise Exception('"Save" button should be active')
        else:
            button.click()
            self.wait_spiner_loading()
        return self

    def click_back(self):
        button = self.wait.until(EC.visibility_of_element_located(self.back_button_locator),
                                 'Back button is missing')
        if self.is_button_disabled(self.back_button_locator, 'Back'):
            raise Exception('"Back" button should be active')
        else:
            button.click()
            self.wait_spiner_loading()
        return self

    def click_assortment_field(self, row_index=0):
        table = Table(self.driver, self.get_table_content())
        assortment_field = table.find_element_in_row(row_index, self.assortment_field, 'Assortment field is missing')
        assortment_field.click()
        return TreeListPopUp(self.driver, 'Assortment')

