from selenium.webdriver.common.by import By

from utilities.BaseWidget import BaseWidget


class GroupsOfPromotions(BaseWidget):

    def __init__(self, driver):
        super(GroupsOfPromotions, self).__init__(driver,
                                                  (By.XPATH, '//div[@class="b-financial-information"]/div[@class="k-grid k-widget"][2]'), # 2 - другий елемент через W3C
                                                  'Financial Information - Groups of promotions')
