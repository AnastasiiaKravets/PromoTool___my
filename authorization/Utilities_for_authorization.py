from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from BasePage import BasePage
from selenium import webdriver


class AuthorizationPage(BasePage):


    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)


    #@ TODO initialize singletone instance of webdriver
    #base_page = BasePage.get_instance()
    #driver = base_page.get_driver()

    app_name = (By.TAG_NAME, 'h1')
    username_label = (By.CSS_SELECTOR, "label[for = 'username']")
    password_label = (By.CSS_SELECTOR, "label[for = 'password']")
    username_input = (By.ID, 'username')
    password_input = (By.ID, 'password')
    sign_in_button = (By.TAG_NAME, 'button')
    forgot_password_link = (By.CLASS_NAME, 'b-authentication__footer')
    english_button = (By.CLASS_NAME, 'b-authentication__flag_en')
    czech_button = (By.CLASS_NAME, 'b-authentication__flag_cs')
    germany_button = (By.CLASS_NAME, 'b-authentication__flag_de')
    notification = (By.CLASS_NAME, 'k-notification-wrap')

    def name_of_app(self):
        app_name = self.wait.until(EC.visibility_of_element_located(self.app_name), 'Name of app is not visible')
        return app_name.text

    def is_image_present(self):
        header = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-authentication__header_logo')),
                                 'The Logo image is not visible')
        logo_img = header.find_elements_by_tag_name('img')
        if len(logo_img) > 0:
            return True
        else:
            return False

    def username_label_text(self):
        username = self.wait.until(EC.visibility_of_element_located(self.username_label),
                                   "Username label is not visible")
        return username.text

    def password_label_text(self):
        password = self.wait.until(EC.visibility_of_element_located(self.password_label),
                                   "Password label is not visible")
        return password.text

    def username_placeholder_text(self):
        placeholder = self.wait.until(EC.visibility_of_element_located(self.username_input),
                                      'Username input field is not visible')
        return placeholder.get_attribute('placeholder')

    def password_placeholder_text(self):
        placeholder = self.wait.until(EC.visibility_of_element_located(self.password_input),
                                      'Password input field is not visible')
        return placeholder.get_attribute('placeholder')

    def enter_username(self, username=''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.username_input),
                                      'Username input field is not visible')
        input_field.send_keys(username)
        return self

    def enter_password(self, password=''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.password_input),
                                      'Password input field is not visible')
        input_field.send_keys(password)
        return self

    def click_sign_in(self):
        sign_button = self.wait.until(EC.element_to_be_clickable(self.sign_in_button), 'Sign in button is not active')
        sign_button.click()
        return self

    def click_forget_password(self):
        forgot_link = self.wait.until(EC.visibility_of_element_located(self.forgot_password_link),
                                      'Forgot password link is not visible')
        forgot_link.click()
        return self

    def change_language(self, language):
        if language == 'en':
            lang_button = self.wait.until(EC.element_to_be_clickable(self.english_button),
                                          'English button is not visible')
            lang_button.click()
        if language == 'cs':
            lang_button = self.wait.until(EC.element_to_be_clickable(self.czech_button),
                                          'Czech button is not visible')
            lang_button.click()
        if language == 'de':
            lang_button = self.wait.until(EC.element_to_be_clickable(self.germany_button),
                                          'Germany button is not visible')
            lang_button.click()
        return self

    def user_input_text(self):
        input_field = self.wait.until(EC.visibility_of_element_located(self.username_input),
                                      'Username input field is not visible')
        return input_field.get_attribute('value')

    def password_input_text(self):
        input_field = self.wait.until(EC.visibility_of_element_located(self.password_input),
                                      'Password input field is not visible')
        return input_field.get_attribute('value')

    def notification_text(self):
        el = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.notification),
                                                 'Notification is not visible')
        return el.text







    def login(self, username = 'admin', password = 'admin'):
        self.enter_username(username)
        self.enter_password(password)
        self.click_sign_in()

