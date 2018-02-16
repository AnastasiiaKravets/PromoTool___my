import unittest
from selenium import webdriver
from BasePage import BasePage
from utilities.Parser import Parser


class BaseTest(unittest.TestCase):
    base_url = Parser().get_base_url()
    browser = Parser().get_browser_name()
    download_directory = 'c:\\Users\\an.kravets\Downloads\PromoTool'

    admin_user = {
        'login': 'admin',
        'password': 'admin'
    }

    autotest_user = {
        'login': 'For Auto Test',
        'password': 'Test'
    }

    pilot_user = {
        'login': 'an.kravets',
        'password': '1111'
    }

    pilot_admin_user = {
        'login': 'admin',
        'password': 'admin'
    }

    def setUp(self):
        if self.browser == 'Chrome':
            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {"download.default_directory": self.download_directory})
            options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome(executable_path=("../WebDrivers/chromedriver.exe"),
                                           chrome_options=options)
            self.driver.set_page_load_timeout(10)


        if self.browser == "IE":
            self.driver = webdriver.Ie(executable_path=("../WebDrivers/IEDriverServer_32.exe"))


        self.driver.maximize_window()
        # self.driver.desired_capabilities['pageLoadStrategy'] = 'eager'
        try:
            self.driver.get(self.base_url + '404')
        except:
            self.driver.close()
            raise Exception('Can not load {}')

    def tearDown(self):
        self.driver.close()

    def open_url(self, part_url: str):
        full_url = str(self.base_url) + str(part_url)
        self.driver.get(full_url)
        BasePage(self.driver).wait_for_url_contain(full_url).wait_spiner_loading()
