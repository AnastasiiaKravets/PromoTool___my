from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SetPasswordPage:

    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

    app_name = (By.TAG_NAME, 'h1')
    password_label = (By.CSS_SELECTOR, "label[for = 'password']")
    re_password_label = (By.CSS_SELECTOR, "label[for = 'repassword']")
    password_input = (By.ID, 'password')
    re_password_input = (By.ID, 'repassword')
    change_pass_button = (By.TAG_NAME, 'button')

    back_to_login_link = (By.CLASS_NAME, 'btn')
    english_button = (By.CSS_SELECTOR, "span[lang = 'en']")
    czech_button = (By.CSS_SELECTOR, "span[lang = 'cs']")
    germany_button = (By.CSS_SELECTOR, "span[lang = 'de']")
    #notification = (By.CLASS_NAME, 'k-notification-wrap')


    def is_image_present(self):
        header = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-authentication__header_logo')),
                                 'The Logo image is not visible')
        logo_img = header.find_elements_by_tag_name('img')
        if len(logo_img) > 0:
            return True
        else:
            return False

    def get_app_name_text(self):
        app_name = self.wait.until(EC.visibility_of_element_located(self.app_name), 'Name of app is not visible')
        return app_name.text

    def enter_password(self, password=''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.password_input),
                                      'Password input field is not visible')
        input_field.send_keys(password)
        return self

    def enter_re_password(self, re_password=''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.re_password_input),
                                      'Re-password input field is not visible')
        input_field.send_keys(re_password)
        return self

    def click_change_password(self):
        change_password_button = self.wait.until(EC.element_to_be_clickable(self.change_pass_button),
                                            'Change password button is not clickable')
        change_password_button.click()
        return self

    def change_language(self, language):
        lang_button = None
        if language == 'en':
            lang_button = self.wait.until(EC.element_to_be_clickable(self.english_button),
                                          'English button is not visible')
        if language == 'cs':
            lang_button = self.wait.until(EC.element_to_be_clickable(self.czech_button),
                                          'Czech button is not visible')
        if language == 'de':
            lang_button = self.wait.until(EC.element_to_be_clickable(self.germany_button),
                                          'Germany button is not visible')
        lang_button.click()
        return self

    def click_back_to_login(self):
        back_to_login = self.wait.until(EC.visibility_of_element_located(self.back_to_login_link),
                                   'Back to login link is not visible')
        back_to_login.click()
        return self









