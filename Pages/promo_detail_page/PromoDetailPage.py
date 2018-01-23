from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from BasePage import BasePage


class PromoDetailPage(BasePage):

    back_button = (By.ID, 'back')
    save_button = (By.ID, 'save')
    cancel_promo_button = (By.ID, 'cancel-promo')
    cancel_template_button = (By.ID, 'cancel-template')
    create_promo_button = (By.ID, 'create-promo')
    copy_button = (By.ID, 'copy-button')
    restart_promo_button = (By.ID, 'restart-promo')
    generate_reservation_button = (By.ID, 'generate-reservation')
    reservations_button = (By.ID, 'reservations')

    """WIDGETS
    compared_promo_widget = (By.CSS_SELECTOR, 'div[class="b-promo-compare k-grid k-widget"]')
    compared_group_widget = (By.CSS_SELECTOR, 'div[class="b-promo-action-compare-group k-grid k-widget"]')
    departments_view_widget = (By.CSS_SELECTOR, 'div[class="b-list-of-promo-departments k-grid k-widget"]')
    pages_view_widget = (By.CSS_SELECTOR, 'div[class="b-list-of-promo-pages k-grid k-widget"]')
    workflow_widget = (By.CSS_SELECTOR, 'div[class="b-promo-action-workflow"]')

    #Main locator for financial info widgets. Each widget finding from it
    financial_info_block = (By.CSS_SELECTOR, 'div[class="b-financial-information"]')"""




    def click_back_button(self):
        self.wait.until(EC.element_to_be_clickable(self.back_button), '"Back" button is not clickable') \
            .click()
        return self

    def click_save_button(self):
        self.wait.until(EC.element_to_be_clickable(self.save_button), '"Save" button is not clickable') \
            .click()
        return self

    def click_cancel_template_button(self):
        self.wait.until(EC.element_to_be_clickable(self.cancel_template_button),
                        '"Cancel Template" button is not clickable') \
            .click()
        return self

    def click_create_promo_button(self):
        self.wait.until(EC.element_to_be_clickable(self.create_promo_button), '"Create promo" button is not clickable') \
            .click()
        return self

    def get_promo_detail_tab(self):
        tab_strip = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[class="k-tabstrip-items k-reset"]')),
            'Tab strip is invisible')
        return WebDriverWait(tab_strip, 5).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'k-item')),
                                                 'Tabs are invisible')[0]

    def get_additional_info_tab(self):
        tab_strip = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[class="k-tabstrip-items k-reset"]')),
            'Tab strip is invisible')
        return WebDriverWait(tab_strip, 5).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'k-item')),
                                                 'Tabs are invisible')[1]

    def click_promo_detail(self):
        self.get_promo_detail_tab().click()
        return self

    def click_additional_info(self):
        self.get_additional_info_tab().click()
        return self
