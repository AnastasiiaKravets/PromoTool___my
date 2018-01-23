import unittest

from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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




    def setUp(self):
        if self.browser == 'Chrome':
            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {"download.default_directory": self.download_directory})
            options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome(executable_path='c:\Program Files (x86)\SeleniumDriver\chromedriver.exe',
                                           chrome_options=options)
            self.driver.set_page_load_timeout(10)
        if self.browser == "IE":
            self.driver = webdriver.Ie('c:\Program Files (x86)\SeleniumDriver\IEDriverServer_32.exe')
        self.driver.maximize_window()
        #self.driver.desired_capabilities['pageLoadStrategy'] = 'eager'
        # TODO load timeout for IE
        #self.driver.set_page_load_timeout(10)

    def tearDown(self):
        self.driver.close()
