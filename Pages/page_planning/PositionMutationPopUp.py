from utilities.BasePopUp import BasePopUp
from utilities.Table import Table
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PositionMutationPopUp(BasePopUp):

    ok_button = (By.CLASS_NAME, 'b-position-mutation__toolbar-ok')
    cancel_button = (By.CLASS_NAME, 'b-position-mutation__toolbar-cancel')


    def __init__(self, driver):
        super(PositionMutationPopUp, self).__init__(driver, 'Position Mutation')

    def click_ok_button(self):
        self.wait.until(EC.element_to_be_clickable(self.ok_button), '"Ok" button is not clickable')\
            .click()
        self.wait_spiner_loading()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.k-widget.k-window')),
                        'Position mutation pop up is still visible after clicking Ok')
        return self

    def click_cancel_button(self):
        self.wait.until(EC.element_to_be_clickable(self.cancel_button), '"Cancel" button is not clickable')\
            .click()

    def enter_promo_selling_price(self, row_index, price):
        price_cell = Table(self.driver, self.get_table_content()).get_row(row_index)[4]
        input = WebDriverWait(price_cell, 5).until(EC.visibility_of_any_elements_located((By.TAG_NAME, 'input')),
                                                   'PromoSelling Price from Position Mutation pop up is not visible')[0]
        input.clear()
        """After clearing another input should be visible"""
        input = WebDriverWait(price_cell, 5).until(EC.visibility_of_any_elements_located((By.TAG_NAME, 'input')),
                                                   'PromoSelling Price from Position Mutation pop up is not visible')[0]
        input.send_keys(price)
        return self


