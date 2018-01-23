from selenium.webdriver.common.by import By

from utilities.BaseWidget import BaseWidget
from utilities.Table import Table


class FinancialInformation(BaseWidget):

    def __init__(self, driver):
        super(FinancialInformation, self).__init__(driver,
                                                  (By.XPATH, '//div[@class="b-financial-information"]/div[@class="k-grid k-widget"][1]'), # 1 - перший елемент через W3C
                                                  'Financial Information')

    def get_all_tables_labels(self):
        table = self.get_table_content('Tables content of Financial Information is missing')
        rows = Table(self.driver, table).get_all_cells_element()
        list = []
        for row in rows:
            list.append(row[0].text)
        return list

