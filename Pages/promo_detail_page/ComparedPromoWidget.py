from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Pages.promo_detail_page.ComparedActionPopUp import ComparedActionPopUp
from utilities.BaseWidget import BaseWidget


class ComparedPromoWidget(BaseWidget):
    add_compared_action_button = (By.CLASS_NAME, 'button-success')
    delete_button = (By.CSS_SELECTOR, 'button.button-danger')

    def __init__(self, driver):
        super(ComparedPromoWidget, self).__init__(driver,
                                                  (By.CSS_SELECTOR, 'div[class="b-promo-compare k-grid k-widget"]'),
                                                  'Compared promo')

    def click_add_compared_action(self):
        button = self.wait.until(EC.visibility_of_element_located(self.add_compared_action_button),
                                 '"Add compared action" button is invisible')
        button.click()
        return ComparedActionPopUp(self.driver)
