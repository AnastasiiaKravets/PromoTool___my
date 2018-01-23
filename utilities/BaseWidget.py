from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.Table import TableFilter


class BaseWidget(BasePage):

    def __init__(self, driver, widget_locator, name: str):
        self.driver = driver
        self.widget_name = name
        self.widget = WebDriverWait(self.driver, 10)\
            .until(EC.presence_of_element_located(widget_locator),
                   '"{}" widget window is absent'.format(self.widget_name))
        self.driver.execute_script("return arguments[0].scrollIntoView();", self.widget)
        self.wait = WebDriverWait(self.widget, 10)

    def get_title_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.k-header.k-grid-toolbar.k-green-table-header')),
                               'Title of "{}" pop up is invisible'.format(self.widget_name)).text

