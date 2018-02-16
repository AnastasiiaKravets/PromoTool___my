from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from BasePage import BasePage
from Pages.promo_type_page.NewPromoTypePage import NewPromoTypePage
from utilities.Table import Table


class PromoTypePage(BasePage):
    new_type_button = (By.CSS_SELECTOR, 'a[class="button-success k-button k-button-icontext"]')
    title = (By.TAG_NAME, 'h2')

    """TABLE HEADER"""
    id_header = (By.CSS_SELECTOR, 'th[data-field="Id"]')
    name_header = (By.CSS_SELECTOR, 'th[data-field="Name"]')
    template_header = (By.CSS_SELECTOR, 'th[data-field="TemplateId"]')

    """Filter column"""
    id_checkbox = (By.CSS_SELECTOR, 'input[data-field="Id"]')
    name_checkbox = (By.CSS_SELECTOR, 'input[data-field="Name"]')
    template_checkbox = (By.CSS_SELECTOR, 'input[data-field="TemplateId"]')


    def get_new_type_button(self):
        return self.wait.until(EC.visibility_of_element_located(self.new_type_button), 'New type button is not visible')

    def click_new_type_button(self):
        button = self.wait.until(EC.visibility_of_element_located(self.new_type_button),
                                 'New type button is not clicable')
        button.click()
        return NewPromoTypePage(self.driver)

    def get_header_text(self, header_element):
        header = self.wait.until(EC.presence_of_element_located(header_element), 'Header of column is not present')
        return header.find_element_by_css_selector('a[class="k-link"]').text

    def is_table_visible(self):
        try:
            self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'k-grid-content')), 'Table is not visible')
            return True
        except ElementNotVisibleException:
            return False

    def get_name_header_element(self):
        return self.wait.until(EC.presence_of_element_located(self.name_header))

    def get_id_header_element(self):
        return self.wait.until(EC.presence_of_element_located(self.id_header))

    def get_template_header_element(self):
        return self.wait.until(EC.presence_of_element_located(self.template_header))

    def click_promo_type_by_id(self, id_row):
        table = Table(self.driver, self.get_table_content())
        first = 0
        last = table.count_rows() - 1
        i = 0
        while True:
            if int(table.get_row(first)[0].text) == int(id_row):

                self.click_link_from_cell(table.get_row(first)[1], 'Promo Type with ID {0} does not open'.format(id_row))
                break
            if int(table.get_row(last)[0].text) == int(id_row):
                self.click_link_from_cell(table.get_row(last)[1], 'Promo Type with ID {0} does not open'.format(id_row))
                break
            if int(table.get_row(int(last/2))[0].text) < int(id_row):
                first = int(last/2)
                last -=1
            else:
                last = int(last/2)
                first +=1
            if i == 50:
                raise Exception('There is no promo type with id {0}'.format(id_row))
            i += 1
        return NewPromoTypePage(self.driver)

    def is_template_button_present(self, row):
        try:
            WebDriverWait(row[2], 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn')))
            return True
        except:
            return False

