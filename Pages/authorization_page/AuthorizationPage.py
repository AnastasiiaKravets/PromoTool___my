from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from BasePage import BasePage
from BaseTest import BaseTest


class AuthorizationPage(BasePage):

    # @ TODO initialize singletone instance of webdriver
    # base_page = BasePage.get_instance()
    # driver = base_page.get_driver()

    app_name = (By.TAG_NAME, 'h1')
    username_label = (By.CSS_SELECTOR, "label[for = 'username']")
    password_label = (By.CSS_SELECTOR, "label[for = 'password']")
    username_input = (By.ID, 'username')
    password_input = (By.ID, 'password')
    sign_in_button = (By.TAG_NAME, 'button')
    forget_password_link = (By.CSS_SELECTOR, "a[href = '/recovery-password']")
    english_button = (By.CLASS_NAME, 'b-authentication__flag_en')
    czech_button = (By.CLASS_NAME, 'b-authentication__flag_cs')
    germany_button = (By.CLASS_NAME, 'b-authentication__flag_de')
    notification = (By.CLASS_NAME, 'k-notification-wrap')

    """Password expiration message"""
    pass_expiration_title = (By.CLASS_NAME, 'k-dialog-title')
    pass_expiration_message = (By.ID, 'b-authentication__message-window')
    pass_expiration_buttons = (By.CLASS_NAME, 'k-dialog-buttongroup')
    pass_expiration_ok_index = 0
    pass_expiration_cancel_index = 1

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
        input_field.clear()
        input_field.send_keys(username)
        return self

    def enter_password(self, password=''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.password_input),
                                      'Password input field is not visible')
        input_field.clear()
        input_field.send_keys(password)
        return self

    def click_sign_in(self):
        sign_button = self.wait.until(EC.element_to_be_clickable(self.sign_in_button), 'Sign in button is not active')
        sign_button.click()
        return self

    def click_forget_password(self):
        forget_link = self.wait.until(EC.visibility_of_element_located(self.forget_password_link),
                                      'Forgot password link is not visible')
        forget_link.click()
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

    def user_input_text(self):
        input_field = self.wait.until(EC.visibility_of_element_located(self.username_input),
                                      'Username input field is not visible')
        return input_field.get_attribute('value')

    def password_input_text(self):
        input_field = self.wait.until(EC.visibility_of_element_located(self.password_input),
                                      'Password input field is not visible')
        return input_field.get_attribute('value')

    def notification_text(self):
        el = WebDriverWait(self.driver, 3).until(EC.visibility_of_all_elements_located(self.notification),
                                                 'Notification is not visible')
        return el[len(el) - 1].text

    def sign_in_button_text(self):
        sign_button = self.wait.until(EC.visibility_of_element_located(self.sign_in_button),
                                      'Sign in button is not visible')
        return sign_button.text

    def forget_pass_link_text(self):
        forget_link = self.wait.until(EC.visibility_of_element_located(self.forget_password_link),
                                      'Forgot password link is not visible')
        return forget_link.text

    def pass_expiration_title_text(self):
        pass_expiration_title_text = self.wait.until(EC.visibility_of_element_located(self.pass_expiration_title))
        return pass_expiration_title_text.text

    def pass_expiration_message_text(self):
        pass_expiration_message = self.wait.until(EC.visibility_of_element_located(self.pass_expiration_message))
        return pass_expiration_message.text

    def get_pass_expiration_ok_button(self):
        buttons = self.wait.until(EC.visibility_of_element_located(self.pass_expiration_buttons),
                                  'Pop up buttons are not visible')
        return buttons.find_elements_by_class_name('k-button')[self.pass_expiration_ok_index]

    def get_pass_expiration_cancel_button(self):
        buttons = self.wait.until(EC.visibility_of_element_located(self.pass_expiration_buttons),
                                  'Pop up buttons are not visible')
        return buttons.find_elements_by_class_name('k-button')[self.pass_expiration_cancel_index]

    def click_pass_expiration_ok_button(self):
        self.get_pass_expiration_ok_button().click()
        return self

    def click_pass_expiration_cancel_button(self):
        self.get_pass_expiration_cancel_button().click()
        return self

    def login(self, username=BaseTest().autotest_user['login'], password=BaseTest().autotest_user['password']):
        """Only with Czech"""
        self.change_language('cs')
        self.enter_username(username)
        self.enter_password(password)
        self.click_sign_in()
