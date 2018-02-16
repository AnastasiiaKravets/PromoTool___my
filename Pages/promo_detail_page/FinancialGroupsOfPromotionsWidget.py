from selenium.webdriver.common.by import By

from Pages.promo_detail_page.FinancialInformationWidget import FinancialInformation
from utilities.Table import Table


class GroupsOfPromotions(FinancialInformation):

    def __init__(self, driver):
        super(FinancialInformation, self).__init__(driver,
                                                   (By.XPATH,
                                                    '//div[@class="b-financial-information"]/div[@class="k-grid k-widget"][2]'),
                                                   # 2 - другий елемент через W3C
                                                   'Financial Information - Groups of promotions')
        self.table = self.get_table_content('Tables content of Financial Information - Group of promotions is missing')

    def are_plan_inputs_disabled(self, error='Inputs in "financial information - groups" is absent'):
        """
        :param error:
        :return: list of False/True, plan input is disabled or not
        """
        table = Table(self.driver, self.table)
        result = []
        for row in table.get_all_cells_element():
            result.append(table.is_input_disabled(row[1], error))
        return result






