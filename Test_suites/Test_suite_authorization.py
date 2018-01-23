import random
import string
import time
import unittest

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import utilities
from BaseTest import BaseTest
from Pages.authorization_page.AuthorizationPage import AuthorizationPage
from Pages.authorization_page.RecoveryPasswordPage import RecoveryPasswordPage
from Pages.authorization_page.SetPasswordPage import SetPasswordPage
from Pages.home_page.HomePage import HomePage
from utilities import EmailReader
from utilities.DataBase import DataBase
from utilities.Parser import Parser


class AuthorizationTest(BaseTest):
    main_mail = 'globuspromotool@gmail.com'

    def setUp(self):
        super().setUp()
        self.driver.get(self.base_url + 'authentication')

    def tearDown(self):
        self.driver.close()

    def test_auth_screen_with_language(self):
        """Maximize window. Check presence of all elements and their translation. Repeat for minimized window"""
        authorization_page = AuthorizationPage(self.driver)
        auth_values = [{
            'language': 'en',
            'user_name': 'User name:',
            'user_name_placeholder': 'User',
            'password': 'Password:',
            'password_placeholder': 'Password',
            'sign_in_button': 'Sign in',
            'forget_password_link': 'Did you forget the password?'},

            {'language': 'cs',
             'user_name': 'Přihlašovací jméno:',
             'user_name_placeholder': 'Přihlašovací jméno',
             'password': 'Heslo:',
             'password_placeholder': 'Heslo',
             'sign_in_button': 'Přihlásit',
             'forget_password_link': 'Zapomněli jste heslo?'}
        ]
        for i in range(2):
            if i == 0:
                self.driver.maximize_window()
            else:
                self.driver.set_window_size(400, 600)
            for value in auth_values:
                with self.subTest():
                    self.assertEqual(authorization_page.name_of_app(), 'Globus PromoTool',
                                     'The name of app is incorrect')
                    self.assertTrue(authorization_page.is_image_present(), 'The logo image is not visible')
                    authorization_page.change_language(value['language'])
                    self.assertEqual(authorization_page.username_label_text(), value['user_name'])
                    self.assertEqual(authorization_page.username_placeholder_text(), value['user_name_placeholder'])
                    self.assertEqual(authorization_page.password_label_text(), value['password'])
                    self.assertEqual(authorization_page.password_placeholder_text(), value['password_placeholder'])
                    self.assertEqual(authorization_page.sign_in_button_text(), value['sign_in_button'])
                    self.assertEqual(authorization_page.forget_pass_link_text(), value['forget_password_link'])

    def test_authorization_with_valid_credential(self):
        """Sign in as 'admin/admin'"""
        authorization_page = AuthorizationPage(self.driver)
        authorization_page.enter_username(self.admin_user['login']) \
            .enter_password(self.admin_user['password'])
        self.assertEqual(self.admin_user['login'], authorization_page.user_input_text(),
                         'Incorrect display of entered characters in the username field')
        self.assertEqual(self.admin_user['password'], authorization_page.password_input_text(),
                         'Incorrect display of entered characters in the password field')
        authorization_page.click_sign_in()
        WebDriverWait(self.driver, 10).until(EC.url_contains('home'), 'URL did not change')
        self.assertEqual(self.base_url + 'home', self.driver.current_url, 'URL did not change')
        home_page = HomePage(self.driver)
        self.assertEqual('admin', home_page.username_text().lower(), 'Registered with another account')

    def test_authorization_with_invalid_credential(self):
        """Enter special characters, sql injection, invalid pairs of password and login, long sequence of characters"""
        chars_80= ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(80))
        SQL_inject_A = 'admin OR 1=1'
        SQL_inject_B = 'admin; DROP TABLE Users'
        SQL_inject_C = '" or ""="'
        SQL_inject_D = "'"
        SQL_inject_E = ':'
        SQL_inject_F = '"'
        value = [
            {'username': 'wrong_username', 'password': 'admin'},  # wrong username
            {'username': 'admin', 'password': 'wrong_pass'},  # wrong password
            {'username': '@#$%^', 'password': '@#$%^'},  # wrong symbol
            {'username': ' ', 'password': ' '},  # space input
            {'username': chars_80, 'password': chars_80},  # wrong username and password 255 char
            {'username': SQL_inject_A, 'password': 'admin'},  # wrong username SQL injection A
            {'username': SQL_inject_B, 'password': 'admin'},  # wrong username SQL injection B
            {'username': SQL_inject_C, 'password': SQL_inject_C},  # wrong username SQL injection C
            {'username': SQL_inject_D, 'password': 'admin'},  # wrong username SQL injection D
            {'username': SQL_inject_E, 'password': 'admin'},  # wrong username SQL injection E
            {'username': SQL_inject_F, 'password': 'admin'},  # wrong username SQL injection F
        ]
        authorization_page = AuthorizationPage(self.driver)
        for val in value:
            with self.subTest(val):
                authorization_page.enter_username(val['username']) \
                    .enter_password(val['password']) \
                    .click_sign_in()
                time.sleep(0.2)  # Timeout for get right notification
                if val['username'] == 'admin':
                    self.assertEqual('errorBad user or password', authorization_page.notification_text())
                    continue
                self.assertEqual("errorInvalid username '{0}'".format(val['username']), authorization_page.notification_text())

    def test_pop_up_change_password_with_valid_data(self):
        """Sign in as 'For Auto Test/Test'. Choose change password option. Verify presence of all elements. Change password on the same one"""
        auth_page = AuthorizationPage(self.driver)
        auth_page.login()
        home_page = HomePage(self.driver)
        home_page.click_user_info() \
            .click_change_password()
        with self.subTest():
            self.assertEqual(home_page.current_pass_label_text(), 'Aktuální heslo:')
            self.assertEqual(home_page.current_password_placeholder(), 'Aktuální heslo')
            self.assertEqual(home_page.new_pass_label_text(), 'Nové heslo:')
            self.assertEqual(home_page.new_password_placeholder(), 'Nové heslo')
            self.assertEqual(home_page.confirm_pass_label_text(), 'Potvrďte heslo:')
            self.assertEqual(home_page.confirm_password_placeholder(), 'Potvrďte heslo')
            self.assertEqual(home_page.get_popup_ok_button().text, 'OK')
            self.assertEqual(home_page.get_popup_cancel_button().text, 'Zrušit')
        home_page.enter_current_password(self.autotest_user['password']) \
            .enter_new_password(self.autotest_user['password']) \
            .enter_confirm_password(self.autotest_user['password']) \
            .click_pop_up_ok_button()
        self.assertEqual(home_page.success_change_password_notification(), 'successHeslo bylo změněno')

    def test_change_password_invalid_data(self):
        """Sign in as 'For Auto Test/Test'. Choose change password option. Change password with non-matching passwords. Cancel changing"""
        value = [
            {'current': 'wrong_current', 'new': self.autotest_user['password'], 'confirm': self.autotest_user['password']},  # wrong current password
            {'current': self.autotest_user['password'], 'new': '1234', 'confirm': '12'},  # wrong confirm password
        ]
        auth_page = AuthorizationPage(self.driver)
        auth_page.login()
        home_page = HomePage(self.driver)
        home_page.click_user_info() \
            .click_change_password()
        for val in value:
            home_page.enter_current_password(val['current']) \
                .enter_new_password(val['new']) \
                .enter_confirm_password(val['confirm']) \
                .click_pop_up_ok_button()
            if val['current'] == 'wrong_current':
                self.assertEqual('Chybně zadané současné heslo', home_page.wrong_password_notification_text(),
                                 'Wrong notification text')
                continue
            self.assertEqual('Hesla se neshodují', home_page.wrong_password_notification_text(),
                             'Wrong notification text')
        home_page.click_pop_up_cancel_button()

    def test_forgotten_password_default_view_and_navigation(self):
        """Navigate to forget password page. Verify presence of all elements and their translation. Return to authorization page"""
        authorization_page = AuthorizationPage(self.driver)
        recover_pass = RecoveryPasswordPage(self.driver)
        authorization_page.click_forget_password()
        WebDriverWait(self.driver, 10).until(EC.url_contains('recovery-password'),
                                             'Did you forget the password has wrong link')
        with self.subTest():
            self.assertEqual(recover_pass.get_app_name_text(), 'Globus PromoTool', 'The name of app is incorrect')
            self.assertTrue(recover_pass.is_image_present(), 'The logo image is not visible')
            """For English"""
            recover_pass.change_language('en')
            self.assertEqual(recover_pass.message_text(), 'The requirement for password recovery:')
            self.assertEqual(recover_pass.email_label_text(), 'User name / Email:')
            self.assertEqual(recover_pass.email_placeholder_text(), 'User name / Email')
            self.assertEqual(recover_pass.send_request_button_text(), 'Send request')
            self.assertEqual(recover_pass.back_to_login_text(), 'Back to login')
            """For Czech"""
            recover_pass.change_language('cs')
            self.assertEqual(recover_pass.message_text(), 'Požadavek na obnovu hesla:')
            self.assertEqual(recover_pass.email_label_text(), 'Přihlašovací jméno / E-mail:')
            self.assertEqual(recover_pass.email_placeholder_text(), 'Přihlašovací jméno / E-mail')
            self.assertEqual(recover_pass.send_request_button_text(), 'Zaslat požadavek')
            self.assertEqual(recover_pass.back_to_login_text(), 'Zpět na přihlášení')

        recover_pass.click_back_to_login()
        WebDriverWait(self.driver, 10).until(EC.url_contains('authentication'),
                                             'Back to login has wrong link')

    def test_forgotten_password_with_invalid_data(self):
        """Navigate to forget password page. Enter non-existent email. Send request"""
        self. driver.get(self.base_url+'recovery-password')
        recover_pass = RecoveryPasswordPage(self.driver)
        recover_pass.enter_email('an') \
            .click_send_request()
        self.assertEqual(recover_pass.get_notification(), 'errorUser not found')


    def test_forgotten_password_with_valid_data(self):
        """Navigate to forget password page. Enter existed email. Send request. Get link in email. Change password"""
        self.driver.get(self.base_url + 'recovery-password')
        recover_pass = RecoveryPasswordPage(self.driver)
        recover_pass.enter_email(self.main_mail) \
            .click_send_request()
        time.sleep(0.5)
        self.assertEqual(recover_pass.get_notification(), 'successE-mail notification was send to Users !')
        self.driver.get(EmailReader.get_link_from_mail())
        WebDriverWait(self.driver, 10).until(EC.url_contains('set-password'), 'Wrong link for setting password')
        set_pass_page = SetPasswordPage(self.driver)
        set_pass_page.enter_password(self.autotest_user['password']) \
            .enter_re_password(self.autotest_user['password']) \
            .click_change_password()
        if set_pass_page.get_notification() in 'errorLink to set password action expired !':
            self.fail('Recived email with expired set password link')
        self.assertEqual(set_pass_page.get_notification(), 'successPassword successfully changed !')

    def test_password_expired_message(self):
        """In database change UpdatePassDate to 2017-04-22 for Test1111. Verify warning message. Set new password"""
        data_base = DataBase(utilities.DataBase.get_connection_parameters())
        data_base.execute(
            "UPDATE [PromoToolGlobus].[PromoTool].[Users] SET[UpdatePassDate] = '2017-04-22 00:00:00.000' WHERE[UserID] = 96;")
        authorization_page = AuthorizationPage(self.driver)
        authorization_page.login()

        """"Default view of warning message"""
        with self.subTest():
            self.assertEqual(authorization_page.pass_expiration_title_text(), 'Varování')
            self.assertEqual(authorization_page.pass_expiration_message_text(), 'Vaše heslo vypršelo')
            self.assertEqual(authorization_page.get_pass_expiration_ok_button().text, 'OK')
            self.assertEqual(authorization_page.get_pass_expiration_cancel_button().text, 'Zrušit')
        authorization_page.click_pass_expiration_ok_button()
        WebDriverWait(self.driver, 10).until(EC.url_contains('set-password'),
                                             'This is not Set Password Page')
        set_pass_page = SetPasswordPage(self.driver)

        """Default view of set password form"""
        with self.subTest():
            time.sleep(3)
            self.assertEqual(set_pass_page.password_label_text(), 'Heslo:')
            self.assertEqual(set_pass_page.password_placeholder(), 'Heslo')
            self.assertEqual(set_pass_page.re_password_label_text(), 'Zadejte znovu heslo:')
            self.assertEqual(set_pass_page.re_password_placeholder(), 'Zadejte znovu heslo')
            self.assertEqual(set_pass_page.change_password_text(), 'Změnit heslo')
            self.assertEqual(set_pass_page.back_to_login_text(), 'Zpět na přihlášení')
        set_pass_page.enter_password(self.autotest_user['password']) \
            .enter_re_password(self.autotest_user['password']) \
            .click_change_password()
        self.assertEqual(set_pass_page.get_notification(), 'successPassword successfully changed !')
        WebDriverWait(self.driver, 10).until(EC.url_contains('authentication'),
                                             "Changing the password don't return to authentication page")
