from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities.Table import Table
from BasePage import BasePage


class ArticleListPage(BasePage):

    title = (By.CSS_SELECTOR, 'a.title.k-button.k-state-disabled')
    article_table = (By.CSS_SELECTOR, 'table[role="treegrid"]')
    # checkbox_locator_article_list = (By.XPATH, "//input[@type='checkbox' and @class='checkbox-product']")
    checkbox_locator_article_list = (By.CLASS_NAME, "checkbox-product")
    back_button_locator = (By.CSS_SELECTOR, "a[class^='back-button'][style='visibility: visible;']")
    add_button_locator = (By.CSS_SELECTOR, "a.add-button.button-success.k-button-icontext")

    def get_title(self):
        title_web_element = self.wait.until(EC.presence_of_element_located(self.title), 'Title on Article list is absent')
        return title_web_element

    def get_back_button(self):
        return self.wait.until(EC.visibility_of_element_located(self.back_button_locator), 'Back button on Article list is absent')

    def get_add_button(self):
        return self.wait.until(EC.visibility_of_element_located(self.add_button_locator), 'Add button on Article list is absent')

    def get_article_table(self):
        table_web_element = self.wait.until(EC.presence_of_element_located(self.article_table), 'Table with articles is absent')
        return table_web_element

    def check_all_checkboxes_article_list(self):
        '''Gets webelements of checkboxes in the 1st column of Article list table, locates checkboxes and click them one-by-one'''
        self.wait_spiner_loading()

        article_table_inst = Table(self.driver, self.get_table_content())
        # rows_num = article_table_inst.count_rows()

        # get double array of all webelements from the table in order to get the webelements of checkbox cells
        all_rows = article_table_inst.get_all_cells_element()

        checkboxes_list = []
        # in the article table the "select" checkboxes are in the first column
        for row in all_rows:
            if len(row) > 0:
                checkboxes_list.append(row[0])

        self.wait_spiner_loading()

        ### ====== Because the table with Articles is dynamic, meaning when we check one article,
        ### ====== one or many subarticles will appear, thus the new elements will appear in the table's DOM ======= ###
        ### ====== The below code will create new instance  of table each time the article is clicked,  ======= ###
        ### ====== but this version is very slow, instead the below loop can check half of the articles
        ### ====== (in case 1 article has 1 subarticle after click) ======= ###
        """TODO: method for dynamically loading table and checking checkboxes """
        # inx = 0
        # while True:
        #     try:
        #         article_table = self.get_table_content()
        #         article_table_inst = Table(self.driver, article_table)
        #         # article_table_inst.get_row_as_webelement(inx)
        #
        #         cell = article_table_inst.get_cell_by_row_and_column_inx(inx, 0)
        #
        #         checkbox_webelement = WebDriverWait(cell, 15).until(EC.element_to_be_clickable(
        #                 self.checkbox_locator_article_list), "Checkbox is not available in Article list")
        #
        #         if not checkbox_webelement.is_selected():
        #             checkbox_webelement.click()
        #
        #         self.wait_spiner_loading()
        #         inx += 1
        #
        #     except:
        #         break

        for cell in checkboxes_list:
            try:
                checkbox_webelement = WebDriverWait(cell, 5).until(EC.element_to_be_clickable(
                    self.checkbox_locator_article_list), "Checkbox is not available in Article list")
            except:
                continue

            if not checkbox_webelement.is_selected():
                checkbox_webelement.click()

            self.wait_spiner_loading()

        add_button = self.wait.until(EC.visibility_of_element_located(self.add_button_locator),
                                      'Add button was not found')

        if add_button.is_enabled():
            add_button.click()
