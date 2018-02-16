from utilities.BaseForm import BaseForm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ArticleFilterForm(BaseForm):

    promo_type_input = (By.CSS_SELECTOR, 'input[data-bind="value: PromoType"]')
    article_code_input = (By.CSS_SELECTOR, 'input[data-bind="value: ArticleCode"]')

    apply_button = (By.CSS_SELECTOR, 'div[name="label_0_APPLY"]')


    def __init__(self, driver):
        super(ArticleFilterForm, self).__init__(driver)
        filter = WebDriverWait(self.driver, 10) \
            .until(EC.presence_of_element_located((By.CLASS_NAME, 'b-articles-list__filter')),
                   'Article list filter is absent')
        self.driver.execute_script("return arguments[0].scrollIntoView();", filter)
        self.wait = WebDriverWait(filter, 10)

    def apply_filter(self):
        apply_button = self.wait.until(EC.visibility_of_element_located(self.apply_button),
                                 'Apply button is missing')
        if self.is_button_disabled(self.apply_button, 'Apply'):
            raise Exception('"Apply" button should be active')
        else:
            self.driver.execute_script("return arguments[0].scrollIntoView();", apply_button)
            apply_button.click()
            self.wait_spiner_loading()
        return self





