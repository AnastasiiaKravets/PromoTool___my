from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utilities.BasePopUp import BasePopUp


class ArticlesMutationPopUp(BasePopUp):

    ok_button = (By.CLASS_NAME, 'button-success')
    cancel_button = (By.CLASS_NAME, 'button-danger')

    def __init__(self, driver):
        super(ArticlesMutationPopUp, self).__init__(driver, 'Articles mutation')

    def click_ok_button(self):
        self.wait.until(EC.element_to_be_clickable(self.ok_button), '"Ok" button is not clickable')\
            .click()

    def click_cancel_button(self):
        self.wait.until(EC.element_to_be_clickable(self.cancel_button), '"Cancel" button is not clickable')\
            .click()

