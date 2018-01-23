from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BasePage import BasePage
from utilities.Parser import Parser

class RemoveRoleDialog(BasePage):
    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

    dialog_window_remove_role_element = (By.CSS_SELECTOR,
                                         "div.k-widget.k-dialog.k-window.k-dialog-centered:not([aria-hidden='true'])")
    dialog_window_remove_role_title_loc = (By.CSS_SELECTOR,
                "div.k-widget.k-dialog.k-window.k-dialog-centered:not([aria-hidden='true']) span.k-dialog-title")

    dialog_window_question_elem = (By.CSS_SELECTOR,
                "div.k-widget.k-dialog.k-window.k-dialog-centered:not([aria-hidden='true']) div.k-content")
    dialog_window_buttons = (By.CSS_SELECTOR,
                             "div.k-widget.k-dialog.k-window.k-dialog-centered:not([aria-hidden='true']) \
                                                            ul.k-dialog-buttongroup.k-dialog-button-layout-stretched")

    dialog_window_yes_button = (By.CSS_SELECTOR,
                    "div.k-widget.k-dialog.k-window.k-dialog-centered:not([aria-hidden='true']) li:nth-of-type(1)")

    dialog_window_no_button = (By.CSS_SELECTOR,
                    "div.k-widget.k-dialog.k-window.k-dialog-centered:not([aria-hidden='true']) li:nth-of-type(2)")

    def remove_role_dialog_window_test(self):
        """Verify elements of the dialog window, which appears when Remove role button pressed"""
        dialog_window_remove_role_element = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_remove_role_element), 'The dialog window delete role is not visible')

        dialog_window_remove_role_title = self.wait.until(EC.visibility_of_element_located(
                    self.dialog_window_remove_role_title_loc), 'The title "Message" of dialog window is not visible')

        dialog_window_dialog_content = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_question_elem), 'The question of dialog window is not visible')

        dialog_window_buttons_visibility = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_buttons), 'The "Yes" , "No" buttons are not visible')

        dialog_window_yes_button_loc = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_yes_button), 'The "Yes" button is not visible')

        dialog_window_no_button_loc = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_no_button), 'The "No" button is not visible')


        return dialog_window_remove_role_element.is_displayed() and dialog_window_remove_role_title.is_displayed() \
                and dialog_window_dialog_content.is_displayed() and dialog_window_buttons_visibility.is_displayed() \
                and dialog_window_yes_button_loc.is_displayed() and dialog_window_no_button_loc.is_displayed()


    def delete_role_click_yes(self):
        dialog_window_yes_button_loc = self.wait.until(EC.visibility_of_element_located(
                                    self.dialog_window_yes_button), 'The "Yes" button is not visible')

        # Click on the "Delete" button
        if dialog_window_yes_button_loc.is_enabled():
            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", dialog_window_yes_button_loc)
            else:
                dialog_window_yes_button_loc.click()

    def delete_role_click_no(self):
        dialog_window_no_button_loc = self.wait.until(EC.visibility_of_element_located(
                                    self.dialog_window_no_button), 'The "No" button is not visible')

        if dialog_window_no_button_loc.is_enabled():
            dialog_window_no_button_loc.click()

