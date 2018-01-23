from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BasePage import BasePage


class RecoveryPasswordPage(BasePage):


    app_name = (By.TAG_NAME, 'h1')
    text_label = (By.CLASS_NAME, "text-danger")
    email_label = (By.CSS_SELECTOR, "label[for = 'login']")
    email_input = (By.ID, 'login')
    send_request_button = (By.CLASS_NAME, 'k-button')

    back_to_login_link = (By.CSS_SELECTOR, "a[href = '/authentication']")
    english_button = (By.CSS_SELECTOR, "span[lang = 'en']")
    czech_button = (By.CSS_SELECTOR, "span[lang = 'cs']")
    germany_button = (By.CSS_SELECTOR, "span[lang = 'de']")
    notification = (By.CLASS_NAME, 'k-notification-wrap')

    def is_image_present(self):
        header = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-recovery-password__header_logo')),
                                 'The Logo image is not visible')
        logo_img = header.find_elements_by_tag_name('img')
        if len(logo_img) > 0:
            return True
        else:
            return False

    def get_app_name_text(self):
        app_name = self.wait.until(EC.visibility_of_element_located(self.app_name), 'Name of app is not visible')
        return app_name.text

    def message_text(self):
        message = self.wait.until(EC.visibility_of_element_located(self.text_label),
                                  'Requirement for password text is not visible')
        return message.text

    def email_label_text(self):
        email = self.wait.until(EC.visibility_of_element_located(self.email_label), 'Email Label is not visible')
        return email.text

    def email_placeholder_text(self):
        input_field = self.wait.until(EC.visibility_of_element_located(self.email_input),
                                      'Email input field is not visible')
        return input_field.get_attribute('placeholder')

    def send_request_button_text(self):
        send_request = self.wait.until(EC.visibility_of_element_located(self.send_request_button),
                                       'Send Request button is not visible')
        return send_request.text

    def back_to_login_text(self):
        back_to_login = self.wait.until(EC.visibility_of_element_located(self.back_to_login_link),
                                        'Back to login link is not visible')
        return back_to_login.text

    def enter_email(self, email):
        input_field = self.wait.until(EC.visibility_of_element_located(self.email_input),
                                      'Email input field is not visible')
        input_field.clear()
        input_field.send_keys(email)
        return self

    def click_send_request(self):
        send_request = self.wait.until(EC.element_to_be_clickable(self.send_request_button),
                                       'Send Request button is not clickable')
        send_request.click()
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

    def get_notification(self):
        notification = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.notification),
                                                           'Notification is not visible')
        return notification.text
