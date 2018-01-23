from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities import XpathFindText
from utilities.Parser import Parser

class UsersPage:
    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

    add_user_button = (By.CLASS_NAME, 'k-grid-add')
    user_table_locator_without_controls = (By.CSS_SELECTOR, 'table.k-selectable')
    user_page_roles_table = (By.XPATH, "(//div[@class='k-grid-content k-auto-scrollable']/*)[2]")
    save_changes_button = (By.CSS_SELECTOR, "a.k-button.k-button-icontext.button-success.k-grid-saveRoles")

    def click_add_user(self):
        button = self.wait.until(EC.element_to_be_clickable(self.add_user_button))
        button.click()
        return self

    def get_webelement_user_table(self):
        user_table_web = self.wait.until(EC.visibility_of_element_located(self.user_table_locator_without_controls),
                                 "Table with users is not visible")
        return user_table_web

    def get_webelement_role_table_in_user_page(self):
        roles_table_web = self.wait.until(EC.visibility_of_element_located(self.user_page_roles_table),
                                                            "Table with roles inside the User page is not visible")
        return roles_table_web

    def get_save_changes_button_user_page(self):
        save_changes_btn = self.wait.until(EC.visibility_of_element_located(self.save_changes_button),
                                                            "Save changes button in User page is not visible")
        return save_changes_btn

    def click_on_the_user_by_name(self, user_name):
        """Click/highlight the Role by its name"""
        # Check if the input was string
        if not isinstance(user_name, str):
            user_name = str(user_name)

        # Take the Role name which is the input parameter and create XPATH with its name
        row_xpath = XpathFindText.xpath_of_text(user_name)

        # get the location of  XPATH object for the Role's name from input parameter
        user_loc = (By.XPATH, row_xpath)

        # get the webelement of the user based on XPATH locator
        try:
            row_with_user_name = WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(user_loc),
                                             "Row with the user name '" + user_name + "' is not visible")
        except:
            return "role not found"

        if row_with_user_name.is_enabled():
            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", row_with_user_name)
            else:
                row_with_user_name.click()

        return row_with_user_name
