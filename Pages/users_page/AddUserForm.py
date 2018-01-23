from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AddUserForm:
    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

    login_input = (By.CSS_SELECTOR, 'input[name="Login"]')
    username_input = (By.CSS_SELECTOR, 'input[name="UserName"]')
    email_input = (By.CSS_SELECTOR, 'input[name="Email"]')
    update_button = (By.CLASS_NAME, 'k-grid-update')

    def enter_login(self, login):
        input_field = self.wait.until(EC.visibility_of_element_located(self.login_input), 'Login input is not visible')
        input_field.send_keys(login)
        return self

    def enter_user_name(self, user_name):
        input_field = self.wait.until(EC.visibility_of_element_located(self.username_input),
                                      'UserName input is not visible')
        input_field.send_keys(user_name)
        return self

    def enter_email(self, email):
        input_field = self.wait.until(EC.visibility_of_element_located(self.email_input), 'Email input is not visible')
        input_field.send_keys(email)
        return self

    def click_update_button(self):
        update = self.wait.until(EC.element_to_be_clickable(self.update_button), 'Update button is not clicable')
        update.click()
        return self
