from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities.Table import Table
from BasePage import BasePage


class ArticleListPage(BasePage):

    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

    title = (By.CSS_SELECTOR, 'a.title.k-button.k-state-disabled')
    article_table = (By.CSS_SELECTOR, 'table[role="treegrid"]')

    def get_title(self):
        title_web_element = self.wait.until(EC.presence_of_element_located(self.title), 'Title on Article list is absent')
        return title_web_element

    def get_article_table(self):
        table_web_element = self.wait.until(EC.presence_of_element_located(self.article_table), 'Table with articles is absent')
        return table_web_element

    def get_list_of_checkbox_locators(self):
        article_table = self.get_table_content()

        article_table_inst = Table(self.driver, article_table)

        all_rows = article_table_inst.get_all_cells_element()

        checkboxes_list = []

        for row in all_rows:
            checkboxes_list.append(row[0])

        return