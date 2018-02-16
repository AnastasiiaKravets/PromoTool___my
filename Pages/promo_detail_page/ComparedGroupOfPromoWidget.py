from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.BaseWidget import BaseWidget


class ComparedGroupOfPromoWidget(BaseWidget):
    add_compared_group_button = (By.CLASS_NAME, 'button-success')
    delete_button = (By.CLASS_NAME, 'button-danger')

    def __init__(self, driver):
        super(ComparedGroupOfPromoWidget, self).__init__(driver,
                                                  (By.CSS_SELECTOR, 'div.b-promo-action-compare-group'),
                                                  'Compared group of promo')

    def click_add_compared_group(self):
        button = self.wait.until(EC.visibility_of_element_located(self.add_compared_group_button),
                                 '"Add compared group" button is invisible')
        button.click()
        return self