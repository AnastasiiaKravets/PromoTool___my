from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.BasePopUp import BasePopUp


class ComparedActionPopUp(BasePopUp):


    def __init__(self, driver):
        super(ComparedActionPopUp, self).__init__(driver, 'Select compared promo action')

