import unittest
from authorization_page.Utilities_for_authorization import AuthorizationPage
from BasePage import BasePage
from home_page.HomePage import HomePage
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class AuthorizationTest(unittest.TestCase, BasePage):
    base_url = 'https://qa05.promotool.temabit.com/'

    def setUp(self):
        #base_page = BasePage.get_instance()
        #self.driver = BasePage().get_driver()

        self.driver = webdriver.Chrome('c:\Program Files (x86)\ChromeDriver\chromedriver.exe')
        #self.driver = webdriver.Ie('c:\Program Files (x86)\ChromeDriver\IEDriverServer_32.exe')

        self.driver.get(self.base_url + 'authentication')

    def tearDown(self):
        self.driver.close()


    def test_auth_screen(self):
        wait = WebDriverWait(self.driver, 10)
        authorization_page = AuthorizationPage(self.driver)
        self.assertEqual(authorization_page.name_of_app(), 'Globus PromoTool', 'The name of app is incorrect')
        self.assertTrue(authorization_page.is_image_present(), 'The logo image is not visible')

        #@TODO може буде якась ідея краща
        username = wait.until(EC.visibility_of_element_located(authorization_page.username_label),
                              "Username label is not visible")
        password = wait.until(EC.visibility_of_element_located(authorization_page.password_label),
                              "Password label is not visible")
        placeholder_user = wait.until(EC.visibility_of_element_located(authorization_page.username_input),
                                      'Username input field is not visible')
        placeholder_pass = wait.until(EC.visibility_of_element_located(authorization_page.password_input),
                                      'Password input field is not visible')
        input_field_user = wait.until(EC.visibility_of_element_located(authorization_page.username_input),
                                      'Username input field is not visible')
        input_field_pass = wait.until(EC.visibility_of_element_located(authorization_page.password_input),
                                      'Password input field is not visible')
        sign_button = wait.until(EC.visibility_of_element_located(authorization_page.sign_in_button),
                                 'Sign in button is not visible')
        forgot_link = wait.until(EC.visibility_of_element_located(authorization_page.forgot_password_link),
                                 'Forgot password link is not visible')
        en_button = wait.until(EC.element_to_be_clickable(authorization_page.english_button),
                               'English button is not visible')
        cz_button = wait.until(EC.element_to_be_clickable(authorization_page.czech_button),
                               'Czech button is not visible')
        de_button = wait.until(EC.element_to_be_clickable(authorization_page.germany_button),
                               'Germany button is not visible')

    def test_authorization_with_valid_data(self):
        authorization_page = AuthorizationPage(self.driver)

        authorization_page.enter_username('admin')\
                          .enter_password('admin')

        self.assertEqual('admin', authorization_page.user_input_text(),
                         'Incorrect display of entered characters in the username field')
        self.assertEqual('admin', authorization_page.password_input_text(),
                         'Incorrect display of entered characters in the password field')

        authorization_page.click_sign_in()

        WebDriverWait(self.driver, 10).until(EC.url_contains('home'), 'URL did not change')
        self.assertEqual(self.base_url+'home', self.driver.current_url)

        home_page = HomePage(self.driver)
        self.assertEqual('Admin', home_page.username_text(), 'Registered with another account')


    def test_authorization_with_invalid_data(self):
        authorization_page = AuthorizationPage(self.driver)

        authorization_page.enter_username('admin')\
                          .enter_password('12345')\
                          .click_sign_in()

        self.assertEqual('errorBad user or password', authorization_page.notification_text())


    def test_pop_up_change_password_view(self):
        # @ TODO test without authorization
        wait = WebDriverWait(self.driver, 10)
        auth_page = AuthorizationPage(self.driver)
        auth_page.login()

        home_page = HomePage(self.driver)
        home_page.click_user_info()\
                 .click_change_password()

        current_pass_label = wait.until(EC.visibility_of_any_elements_located(home_page.pop_up_labels_list),
                                        'Pop up labels is not visible')[home_page.current_pass_label_index]
        new_pass_label = wait.until(EC.visibility_of_any_elements_located(home_page.pop_up_labels_list),
                                        'Pop up labels is not visible')[home_page.new_pass_label_index]
        confirm_pass_label = wait.until(EC.visibility_of_any_elements_located(home_page.pop_up_labels_list),
                                'Pop up labels is not visible')[home_page.confirm_pass_label_index]
        ok_button = home_page.get_popup_ok_button()
        cancel_button = home_page.get_popup_cancel_button()


    def test_change_password_valid_data(self):
        auth_page = AuthorizationPage(self.driver)
        auth_page.login()

        home_page = HomePage(self.driver)
        home_page.click_user_info() \
                 .click_change_password().enter_old_password('admin')\
                 .enter_new_password('admin')\
                 .enter_confirm_password('admin')\
                 .click_pop_up_ok_button()
        self.assertTrue(home_page.is_change_password_notification_present(), 'Change Password Notification is absent')


    def test_change_password_invalid_data(self):
        # @TODO test notification for invalid data      check the language
        auth_page = AuthorizationPage(self.driver)
        auth_page.login()

        home_page = HomePage(self.driver)
        home_page.click_user_info() \
            .click_change_password()\
            .enter_old_password('123') \
            .enter_new_password('1234') \
            .enter_confirm_password('1234') \
            .click_pop_up_ok_button()
        self.assertEqual('Špatné aktuální heslo', home_page.wrong_password_notification_text(),
                         'Wrong notification text')
        home_page.enter_old_password('admin') \
            .enter_new_password('administrator') \
            .enter_confirm_password('admin') \
            .click_pop_up_ok_button()
        self.assertEqual('Hesla se neshodují', home_page.wrong_password_notification_text(),
                         'Wrong notification text')

    def test_change_password_cancel(self):
        # @ TODO check if pop up is closed
        auth_page = AuthorizationPage(self.driver)
        auth_page.login()

        home_page = HomePage(self.driver)
        home_page.click_user_info() \
            .click_change_password()\
            .click_pop_up_cancel_button()


    def test_forgotten_password(self):
        pass

    def test_setting_password_for_a_user(self):
        pass




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AuthorizationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
