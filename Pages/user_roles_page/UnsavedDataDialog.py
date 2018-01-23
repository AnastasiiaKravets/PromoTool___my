from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BasePage import BasePage
from utilities.Parser import Parser

class UnsavedDataDialog(BasePage):
    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

    dialog_window_unsaved_changes_full = (By.CSS_SELECTOR, "div.k-widget.k-dialog.k-window.k-dialog-centered")
    dialog_window_unsaved_changes_title = (By.CSS_SELECTOR, "div.k-widget.k-dialog.k-window.k-dialog-centered span.k-dialog-title")
    dialog_window_unsaved_message = (By.CSS_SELECTOR, "div.k-widget.k-dialog.k-window.k-dialog-centered div.k-content")
    dialog_window_unsaved_ok = (By.CSS_SELECTOR, "div.k-widget.k-dialog.k-window.k-dialog-centered li:nth-child(1)")
    dialog_window_unsaved_cancel = (By.CSS_SELECTOR, "div.k-widget.k-dialog.k-window.k-dialog-centered li:nth-child(2)")

    def unsave_changes_dialog_window_test(self):
        """Verify elements of the dialog window, which appears when check privilege checkbox"""
        dialog_window_unsaved_changes_full_element = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_unsaved_changes_full), 'The full dialog window about unsaved changes is not visible')

        dialog_window_unsaved_changes_title_element = self.wait.until(EC.visibility_of_element_located(
                    self.dialog_window_unsaved_changes_title), 'The title "Unsaved data" of dialog window is not visible')

        dialog_window_unsaved_message_element = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_unsaved_message), '"All unsaved data will be lost" is not visible')

        dialog_window_unsaved_ok_element = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_unsaved_ok), 'The "OK" button is not visible')

        dialog_window_unsaved_cancel_element = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_unsaved_cancel), 'The "Cancel" button is not visible')

        return dialog_window_unsaved_changes_full_element.is_displayed() and \
               dialog_window_unsaved_changes_title_element.is_displayed() and \
               dialog_window_unsaved_message_element.is_displayed() and \
               dialog_window_unsaved_ok_element.is_displayed() and \
               dialog_window_unsaved_cancel_element.is_displayed()

    def save_changes_click_ok(self):
        dialog_window_unsaved_ok_element = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_unsaved_ok), 'The "OK" button is not visible')

        # Click on the "OK" button
        if dialog_window_unsaved_ok_element.is_enabled():
            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", dialog_window_unsaved_ok_element)
            else:
                dialog_window_unsaved_ok_element.click()

    def save_changes_click_cancel(self):
        dialog_window_unsaved_cancel_element = self.wait.until(EC.visibility_of_element_located(
                            self.dialog_window_unsaved_cancel), 'The "Cancel" button is not visible')

        # Click on the "Cancel" button
        if dialog_window_unsaved_cancel_element.is_enabled():
            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", dialog_window_unsaved_cancel_element)
            else:
                dialog_window_unsaved_cancel_element.click()
