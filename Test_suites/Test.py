import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import utilities
from BaseTest import BaseTest
from Pages.authorization_page.RecoveryPasswordPage import RecoveryPasswordPage
from Pages.authorization_page.SetPasswordPage import SetPasswordPage
from Pages.home_page.HomePage import HomePage
from Pages.users_page.AddUserForm import AddUserForm
from Pages.users_page.UsersPage import UsersPage
from utilities import user_info, EmailReader
from utilities.DataBase import DataBase
from utilities.PromoRequest import PromoRequest


class Test(BaseTest):
    main_mail = 'globuspromotool@gmail.com'
    def setUp(self):
        super().setUp()
        self.driver.get(self.base_url + '404')
        PromoRequest(self.driver).authorization_by_request(login=self.autotest_user['login'], password=self.autotest_user['password'])
        self.driver.get(self.base_url +'home')

    def test_add_user(self):
        home_page = HomePage(self.driver)

        home_page.click_users_menuitem()
        time.sleep(1)

        user_page = UsersPage(self.driver)
        user_page.click_add_user()

        add_user = AddUserForm(self.driver)
        user_data = user_info.get_new_user_name()
        add_user.enter_login(user_data) \
            .enter_user_name(user_data) \
            .enter_email(EmailReader.new_user_email()) \
            .click_update_button()
        connection_param = utilities.DataBase.get_connection_parameters()
        data_base = DataBase(connection_param)
        data_base.execute("DELETE FROM [PromoToolGlobus].[PromoTool].[Users] WHERE [UserName] LIKE 'autotest%'")


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
