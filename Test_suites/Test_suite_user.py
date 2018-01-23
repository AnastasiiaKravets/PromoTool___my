import time

import utilities
from BaseTest import BaseTest
from Pages.home_page.HomePage import HomePage
from Pages.users_page.AddUserForm import AddUserForm
from Pages.users_page.UsersPage import UsersPage
from utilities import EmailReader
from utilities import user_info
from utilities.DataBase import DataBase
from utilities.PromoRequest import PromoRequest


class UserPageTest(BaseTest):
    main_mail = 'globuspromotool@gmail.com'


    def setUp(self):
        super().setUp()
        self.driver.get(self.base_url + '404')
        PromoRequest(self.driver).authorization_by_request(login=self.autotest_user['login'], password=self.autotest_user['password'])
        self.driver.get(self.base_url +'home')

    def tearDown(self):
        self.driver.close()




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


