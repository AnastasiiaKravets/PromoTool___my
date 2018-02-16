from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BasePage import BasePage


class BaseForm(BasePage):
    def get_header_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-form__title-text')),
                               '"Promo type information" header is not visible').text

    def get_dropdown(self, input_element, error=None):
        hidden_input = self.wait.until(EC.presence_of_element_located(input_element), error)
        # dropdown_parent_span = WebDriverWait(hidden_input, 5).until(EC.presence_of_element_located((By.XPATH, '..')), error)
        dropdown_parent_span = WebDriverWait(hidden_input, 5).until(EC.visibility_of_element_located((By.XPATH, '..')), error)
        dropdown = dropdown_parent_span.find_element_by_css_selector('span[class="k-input"]')
        self.driver.execute_script("return arguments[0].scrollIntoView();", dropdown)
        return dropdown

    def is_field_required(self, field_locator):
        field = self.wait.until(EC.presence_of_element_located(field_locator))
        div_parent_element = WebDriverWait(field, 5).until(EC.presence_of_element_located((By.XPATH, '..')))
        if 'b-form__field_required' in div_parent_element.get_attribute('class'):
            return True
        else:
            return False

    def is_dropdown_disabled(self, field_locator):
        field = self.wait.until(EC.presence_of_element_located(field_locator))
        span_parent_element = WebDriverWait(field, 5).until(EC.presence_of_element_located((By.XPATH, '..')))
        span_element = span_parent_element.find_element_by_tag_name('span')
        if 'k-state-disabled' in span_element.get_attribute('class'):
            return True
        else:
            return False

    def is_input_disabled(self, field_locator, error=None):
        field = self.wait.until(EC.presence_of_element_located(field_locator), error)
        span_parent_element = WebDriverWait(field, 5).until(EC.presence_of_element_located((By.XPATH, '..')))
        if 'readonly' in span_parent_element.get_attribute('class'):
            return True
        else:
            return False

    def is_multiselect_disabled(self, field_locator):
        field = self.wait.until(EC.presence_of_element_located(field_locator))
        if 'true' in field.get_attribute('aria-disabled'):
            return True
        else:
            return False

    def is_checkbox_disabled(self, field_locator, checkbox_name=None):
        checkbox = self.wait.until(EC.presence_of_element_located(field_locator),
                                   '"{}" checkbox is missing'.format(checkbox_name))
        return checkbox.get_attribute('disabled')

    def get_notification_required_field_text(self, field_locator, error_message=None):
        try:
            field = self.wait.until(EC.presence_of_element_located(field_locator))
            div_parent_element = WebDriverWait(field, 5).until(EC.presence_of_element_located((By.XPATH, '..')))
            return div_parent_element.find_element_by_class_name('b-form__error').text
        except:
            raise Exception(error_message)

    def get_input_text(self, input_locator, error_message=None):
        return self.wait.until(EC.visibility_of_any_elements_located(input_locator), error_message)[0] \
            .get_attribute('value')

    def get_dropdown_value_text(self, input_locator, error_message=None):
        return self.get_dropdown(input_locator, error_message).text

    def get_checkbox_value(self, input_locator, error_message=None):
        checkbox = self.wait.until(EC.visibility_of_any_elements_located(input_locator), error_message)[0]
        if checkbox.get_attribute('checked'):
            return True
        else:
            return None

    def get_multiselect_value_text(self, input_locator, error_message=None):
        field = self.wait.until(EC.presence_of_element_located(input_locator), error_message)
        div_parent_element = WebDriverWait(field, 5).until(EC.visibility_of_element_located((By.XPATH, '..')))
        self.driver.execute_script("return arguments[0].scrollIntoView();", div_parent_element)
        list_elements = div_parent_element.find_elements_by_tag_name('li')
        list_options_text = []
        for el in list_elements:
            list_options_text.append(el.text)
        return list_options_text

    def multiple_select_by_index_from_input(self, element_locator, index_list=None, select_name=None):
        input = self.wait.until(EC.presence_of_element_located(element_locator),
                                '"{0}" is absent'.format(str(select_name)))
        select = WebDriverWait(input, 5).until(EC.presence_of_element_located((By.XPATH, '..')),
                                               '"{0}" field is invisible'.format(str(select_name)))
        self.driver.execute_script("return arguments[0].scrollIntoView();", select)
        select.click()
        self.multiple_select_by_index(index_list, select_name)
        return self

    def clear_field(self, element_locator, error='Can not clear field in form'):
        hidden_input = self.wait.until(EC.presence_of_element_located(element_locator), 'Can not find field for clear')
        field_parent_span = WebDriverWait(hidden_input, 5).until(EC.visibility_of_element_located((By.XPATH, '../..')),
                                                                 'Can not find field for clear')
        self.driver.execute_script("return arguments[0].scrollIntoView();", field_parent_span)

        ActionChains(self.driver).move_to_element(field_parent_span).perform()

        close_icon = WebDriverWait(field_parent_span, 5).until(EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, 'span.k-icon.k-i-close')), 'There is no clear button for field')[0]
        try:
            close_icon.click()
        except:
            raise Exception(error)
        return self

