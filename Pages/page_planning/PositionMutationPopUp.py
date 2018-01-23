from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utilities.BasePopUp import BasePopUp


class PositionMutationPopUp(BasePopUp):

    ok_button = (By.CLASS_NAME, 'b-position-mutation__toolbar-ok')
    cancel_button = (By.CLASS_NAME, 'b-position-mutation__toolbar-cancel')

    def __init__(self, driver):
        super(PositionMutationPopUp, self).__init__(driver, 'Position Mutation')

    def click_ok_button(self):
        self.wait.until(EC.element_to_be_clickable(self.ok_button), '"Ok" button is not clickable')\
            .click()

    def click_cancel_button(self):
        self.wait.until(EC.element_to_be_clickable(self.cancel_button), '"Cancel" button is not clickable')\
            .click()
