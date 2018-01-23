from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
from utilities.Parser import Parser
from selenium.webdriver.common.keys import Keys

class AddRolePopUp(BasePage):
    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

   #add_role_button = (By.CSS_SELECTOR, "section#l-content a.k-button.k-button-icontext.button-success.k-grid-add")
    add_role_button = (By.CSS_SELECTOR, "a.k-button.k-button-icontext.button-success.k-grid-add")
    new_role_pop_up_window = (By.CSS_SELECTOR, "div.k-widget.k-window[style*='block']")
    new_role_pop_up_edit_title = (By.CSS_SELECTOR, "div.k-widget.k-window[style*='block'] span.k-window-title")
    new_role_pop_up_close_button = (By.CSS_SELECTOR, "div.k-widget.k-window[style*='block'] span.k-icon.k-i-close")
    new_role_pop_up_role_id = (By.CSS_SELECTOR, "div.k-widget.k-window[style*='block'] label[for='RoleID']")
    new_role_pop_up_role_name = (By.CSS_SELECTOR, "div.k-widget.k-window[style*='block'] label[for='RoleName']")
    new_role_pop_up_role_is_active = (By.CSS_SELECTOR, "div.k-widget.k-window[style*='block'] label[for='IsActive']")
    new_role_pop_up_name_text_box = (By.CSS_SELECTOR, "div.k-widget.k-window[style*='block'] input[type='text']")
    new_role_pop_up_is_active_checkbox = (By.CSS_SELECTOR,
                                          "div.k-widget.k-window[style*='block'] input[type='checkbox']")
    new_role_pop_up_update_button = (By.CSS_SELECTOR,
                    "div.k-widget.k-window[style*='block'] a.k-button.k-button-icontext.k-primary.k-grid-update")
    new_role_pop_up_cancel_button = (By.CSS_SELECTOR,
                    "div.k-widget.k-window[style*='block'] a.k-button.k-button-icontext.k-grid-cancel")

    new_role_pop_up_active_checkbox = (By.CSS_SELECTOR, "div.k-widget.k-window[style*='block'] input[type='checkbox']")

    pop_up_role_name_message = (By.CSS_SELECTOR, "div.k-notification-wrap")


    def press_add_new_role_pop_up_window(self):
        add_role_pop_up_window = self.wait.until(EC.visibility_of_element_located(self.add_role_button))

        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", add_role_pop_up_window)
        else:
            add_role_pop_up_window.click()

        # locate the pop-up window which appears after pressing the Add new role button
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(self.new_role_pop_up_window),
                                "Add new role dialog window is not visible. The button Add new role was not pressed")
        except TimeoutException:
            return False
        return True

    def add_new_role_edit_title(self):
        new_role_pop_up_edit = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_edit_title))
        return new_role_pop_up_edit.text

    def add_new_role_close_button(self):
        new_role_close_button = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_close_button))
        return new_role_close_button.is_enabled()

    def add_new_role_id(self):
        new_role_id = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_role_id))
        return new_role_id.is_displayed()

    def add_new_role_name(self):
        new_role_name = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_role_name))
        return new_role_name.is_displayed()

    def add_new_role_is_active(self):
        new_role_is_active = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_role_is_active))
        return new_role_is_active.is_displayed()

    def add_new_role_name_text_box(self):
        new_role_name_text_box = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_name_text_box))
        return new_role_name_text_box.is_enabled()

    def add_new_role_checkbox(self):
        new_role_checkbox = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_is_active_checkbox))
        return new_role_checkbox.is_enabled()

    def add_new_role_update_button(self):
        new_role_update_button = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_update_button))
        return new_role_update_button.is_enabled()

    def add_new_role_cancel_button(self):
        new_role_cancel_button = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_cancel_button))
        return new_role_cancel_button.is_enabled()

    def press_cancel_new_role_pop_up_window(self):
        new_role_cancel_button = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_cancel_button))
        new_role_cancel_button.click()

    def add_new_role_and_read_error_message(self, new_role):

        new_role_name_text_box = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_name_text_box))

        if new_role_name_text_box.is_enabled():
            # click on the text field
            new_role_name_text_box.click()
            time.sleep(1)
            # write the new role name
            new_role_name_text_box.send_keys(new_role)

            # Check visibility of "Update" button and press "Update" button
            pop_up_update_button_loc = self.wait.until(EC.visibility_of_element_located(
                                                                                self.new_role_pop_up_update_button))
            if pop_up_update_button_loc.is_enabled():
                self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_update_button)).click()

        # find the locator of popup error message and return its text
        role_name_message_loc = self.wait.until(EC.visibility_of_element_located(self.pop_up_role_name_message))
        return role_name_message_loc.text

    def add_new_role_active(self, new_role):
        new_role_name_text_box = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_name_text_box))
        new_role_is_active_checkbox = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_active_checkbox))

        if new_role_name_text_box.is_enabled() and new_role_is_active_checkbox.is_enabled():
            new_role_name_text_box.click()
            time.sleep(1)
            new_role_name_text_box.send_keys(new_role)
            new_role_is_active_checkbox.click()
            self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_update_button)).click()

    def add_new_role_not_active(self, new_role):
        new_role_name_text_box = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_name_text_box))

        if new_role_name_text_box.is_enabled():
            new_role_name_text_box.click()
            time.sleep(1)
            new_role_name_text_box.send_keys(new_role)
            self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_update_button)).click()

    def edit_role(self, new_role_name, save='no'):
        old_role_name_text_box = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_name_text_box))
        old_role_is_active_checkbox = self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_active_checkbox))

        if old_role_name_text_box.is_enabled() and old_role_is_active_checkbox.is_enabled():
            old_role_name_text_box.click()
            time.sleep(1)
            old_role_name_text_box.send_keys(Keys.CONTROL, 'a')
            old_role_name_text_box.send_keys(new_role_name)
            old_role_is_active_checkbox.click()
            if save == 'yes':
                self.wait.until(EC.visibility_of_element_located(self.new_role_pop_up_update_button)).click()


