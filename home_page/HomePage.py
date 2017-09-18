from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import unittest


class HomePage(BasePage):

    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)



    user_name = (By.CLASS_NAME, 'b-user__name')

    user_info = (By.CLASS_NAME, 'b-user__info')
    user_action_list = (By.CLASS_NAME, 'b-user__action')
    exit_index = 0
    change_pass_index = 1
    settings_index = 2

    pop_up_labels_list = (By.CLASS_NAME, 'b-form__label')
    current_pass_label_index = 0
    new_pass_label_index = 1
    confirm_pass_label_index = 2

    old_password_field = (By.ID, 'oldUserPassword')
    new_password_field = (By.ID, 'newUserPassword')
    confirm_password_field = (By.ID, 'confirmUserPassword')

    pop_up_buttons = (By.CLASS_NAME, 'b-user__password-popup-buttons')
    pop_up_ok_button_index = 0
    pop_up_cancel_button_index = 1

    change_pass_notification = (By.CLASS_NAME, 'k-notification-wrap')
    wrong_password_notification = (By.CLASS_NAME, 'b-user__password-popup-error')




    def get_popup_ok_button(self):
        buttons = self.wait.until(EC.visibility_of_element_located(self.pop_up_buttons),
                                    'Pop up buttons are not visible')
        return buttons.find_elements_by_class_name('b-button')[self.pop_up_ok_button_index]

    def get_popup_cancel_button(self):
        buttons = self.wait.until(EC.visibility_of_element_located(self.pop_up_buttons),
                                    'Pop up buttons are not visible')
        return buttons.find_elements_by_class_name('b-button')[self.pop_up_cancel_button_index]


    def wrong_password_notification_text(self):
        notification = self.wait.until(EC.visibility_of_element_located(self.wrong_password_notification), 'Wrong password notification is not displayed')
        return notification.text




    def username_text(self):
        username = self.wait.until(EC.visibility_of_element_located(self.user_name), 'Username is not visible')
        return username.text

    def click_user_info(self):
        info = self.wait.until(EC.visibility_of_element_located(self.user_info), 'User info is not visible')
        info.click()
        return self

    def click_change_password(self):
        change_password = self.wait.until(EC.visibility_of_all_elements_located(self.user_action_list),
                                          'The Change password is not visible')[self.change_pass_index]
        change_password.click()
        return self

    def enter_old_password(self, password = ''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.old_password_field),
                                      'The Old password input is not visible')
        input_field.send_keys(password)
        return self

    def enter_new_password(self, password = ''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.new_password_field),
                                      'The New password input is not visible')
        input_field.send_keys(password)
        return self

    def enter_confirm_password(self, password = ''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.confirm_password_field),
                                      'The Confirm password input is not visible')
        input_field.send_keys(password)
        return self

    def current_pass_text(self):
        label = self.wait.until(EC.visibility_of_any_elements_located(self.pop_up_labels_list),
                                'Pop up labels is not visible')[self.current_pass_label_index]
        return label.text

    def new_pass_text(self):
        label = self.wait.until(EC.visibility_of_any_elements_located(self.pop_up_labels_list),
                                'Pop up labels is not visible')[self.new_pass_label_index]
        return label.text

    def confirm_pass_text(self):
        label = self.wait.until(EC.visibility_of_any_elements_located(self.pop_up_labels_list),
                                'Pop up labels is not visible')[self.confirm_pass_label_index]
        return label.text

    def click_pop_up_ok_button(self):
        ok_button = self.get_popup_ok_button()
        if 'disabled' in ok_button.get_attribute('class'):
            unittest.TestCase.fail(unittest.TestCase, 'The Ok button is inactive')
        else:
            ok_button.click()

    def click_pop_up_cancel_button(self):
        self.get_popup_cancel_button().click()
        return self

    def is_change_password_notification_present(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.change_pass_notification))
            return True
        except(exceptions.TimeoutException):
            return False
