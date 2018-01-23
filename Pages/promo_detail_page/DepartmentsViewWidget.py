from selenium.webdriver.common.by import By

from utilities.BaseWidget import BaseWidget


class DepartmentViewWidget(BaseWidget):

    def __init__(self, driver):
        super(DepartmentViewWidget, self).__init__(driver,
                                                   (By.CSS_SELECTOR, 'div.b-list-of-promo-departments.k-widget'),
                                                   'Department view')
