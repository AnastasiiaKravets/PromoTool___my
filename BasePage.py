from selenium import webdriver

class BasePage:
    class __Base:
        def __init__(self):
            self.driver = webdriver.Chrome('c:\Program Files (x86)\ChromeDriver\chromedriver.exe')

        def get_driver(self):
            return self.driver

    instance = None

    @staticmethod
    def get_instance():
        if not BasePage.instance:
            BasePage.instance = BasePage.__Base()
        return BasePage.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)