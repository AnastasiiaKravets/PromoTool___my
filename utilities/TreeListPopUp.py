from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.BasePopUp import BasePopUp


class TreeListPopUp(BasePopUp):
    expand_icon = (By.CSS_SELECTOR, 'span.k-icon.k-i-expand')
    nested_group = (By.CSS_SELECTOR, 'ul.k-group')

    def __init__(self, driver, name: str):
        super(TreeListPopUp, self).__init__(driver, name)
        self.list_rows = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'li[role="treeitem"]')),
                               'There is no option in treelist {}'.format(self.pop_up_name))
        self.list = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'span[class="k-in"]')),
                               'There is no option in treelist {}'.format(self.pop_up_name))

    def choose_all_options(self):
        for el in self.list:
            el.click()
        self.close_widget_window()
        return self

    def choose_option_by_index(self, list_of_index):
        try:
            for index in list_of_index:
                self.list[index].click()
        except IndexError:
            print('There is no element with index ' + str(list_of_index))
        self.close_widget_window()
        return self

    def select_list_of_webelements_from_tree_by_names(self, list_of_names):
        '''Select assortment items from the tree according to assortment names'''

        for name in list_of_names:
            assortment_xpath = "//ul[@class='k-group k-treeview-lines']//span[./text()= '%s']" % name
            el_list = WebDriverWait(self.pop_up, 5).until(EC.presence_of_element_located((By.XPATH,
                             assortment_xpath)), 'Assortment is absent')
            el_list.click()

    def open_base_treeitem(self, index):
        expand_icon = WebDriverWait(self.list_rows[index], 5).until(EC.visibility_of_element_located(self.expand_icon),
                                                                    'Category has not child items')
        expand_icon.click()
        nested_group = WebDriverWait(self.list_rows[index], 5).until(EC.visibility_of_element_located(self.nested_group),
                                                                    'Category has not child items')
        return nested_group

    def choose_all_options_from_nested_group(self, nested_group_element):
        nested_list = WebDriverWait(nested_group_element, 5).until\
            (EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'span[class="k-in"]')),
                               'There is no option in nested treelist {}'.format(self.pop_up_name))
        for el in nested_list:
            el.click()
        self.close_widget_window()
        return self

    def choose_option_by_index_from_nested_group(self, nested_group_element, list_of_index):
        nested_list = WebDriverWait(nested_group_element, 5).until\
            (EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'span[class="k-in"]')),
                               'There is no option in nested treelist {}'.format(self.pop_up_name))
        try:
            for index in list_of_index:
                nested_list[index].click()
        except IndexError:
            print('There is no element with index ' + str(list_of_index) + ' in nested group')
        self.close_widget_window()
        return self



