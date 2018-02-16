from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.Table import TableFilter
import time

class BasePopUp(BasePage, TableFilter):

    def __init__(self, driver, pop_up_name: str):
        self.driver = driver
        self.pop_up_name = pop_up_name

        self.pop_up = WebDriverWait(self.driver, 10)\
            .until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div.k-widget.k-window')),
                   '"{}" pop up window is absent'.format(self.pop_up_name))[0]
        self.wait = WebDriverWait(self.pop_up, 10)

    def get_title_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[k-window-title]')),
                               'Title of "{}" pop up is invisible'.format(self.pop_up_name)).text

    def close_widget_window(self):
        close_btn = self.wait.until(EC.visibility_of_any_elements_located
                                    ((By.CLASS_NAME, 'k-i-close')),
                                    'There is no "Close" button for "{}" pop up window'.format(self.pop_up_name))[0]
        close_btn.click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'k-window')),
                                            '"{}" pop up window was not closed'.format(self.pop_up_name))
        return self






