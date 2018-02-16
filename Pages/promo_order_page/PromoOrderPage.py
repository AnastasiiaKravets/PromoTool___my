from utilities.BaseForm import BaseForm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.TreeListPopUp import TreeListPopUp


class PromoOrderPage(BaseForm):

    """Filter fields"""
    shop_input = (By.CSS_SELECTOR, 'div.b-react-custom-select-tree.hide-clear-item')


    """headers"""

    code_header = (By.CSS_SELECTOR, 'th[data-title="Code"]')



    def click_shop_input(self):
        input = self.wait.until(EC.visibility_of_element_located(self.shop_input), 'Shop input is invisible')
        input.click()
        return TreeListPopUp(self.driver, 'Shop')


