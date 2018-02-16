from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utilities.BaseWidget import BaseWidget
from utilities.Table import Table


class FinancialInformation(BaseWidget):

    def __init__(self, driver):
        super(FinancialInformation, self).__init__(driver,
                                                   (By.XPATH,
                                                    '//div[@class="b-financial-information"]/div[@class="k-grid k-widget"][1]'),
                                                   # 1 - перший елемент через W3C
                                                   'Financial Information')
        self.table = self.get_table_content('Tables content of Financial Information is missing')

    turnover_row = 0
    title_page_row = 1
    margin_row = 2
    gross_profit_row = 3
    suppliers_contribution_row = 4
    total_gross_profit_row = 5

    def get_all_tables_labels(self):
        rows = Table(self.driver, self.table).get_all_cells_element()
        list = []
        for row in rows:
            list.append(row[0].text)
        return list

    def enter_plan_value(self, row, value, error_message='Input in financial information is absent'):
        current_row = Table(self.driver, self.table).get_row(row)
        input = WebDriverWait(current_row[1], 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')),
                                                       error_message)
        input.clear()
        input.send_keys(value)
        return self

    def get_plan_value(self, row, error_message='Input in financial information is absent'):
        table = Table(self.driver, self.table)
        current_row = table.get_row(row)
        return table.get_value_from_input(current_row[1], error_message)

    def is_plan_input_disabled(self, row, error='Input in financial information is absent'):
        table = Table(self.driver, self.table)
        current_row = table.get_row(row)
        return table.is_input_disabled(current_row[1], error)

    def get_estimation_value(self, row):
        table = Table(self.driver, self.table)
        current_row = table.get_row(row)
        return current_row[2].text

    def get_estimation_vs_plan_value(self, row):
        table = Table(self.driver, self.table)
        current_row = table.get_row(row)
        return current_row[3].text

    def get_reality_value(self, row):
        table = Table(self.driver, self.table)
        current_row = table.get_row(row)
        return current_row[4].text

    def get_reality_vs_estimation_value(self, row):
        table = Table(self.driver, self.table)
        current_row = table.get_row(row)
        return current_row[5].text

    def get_last_year_value(self, row):
        table = Table(self.driver, self.table)
        current_row = table.get_row(row)
        return current_row[6].text

    def get_estimation_vs_last_year_abs_value(self, row):
        table = Table(self.driver, self.table)
        current_row = table.get_row(row)
        return current_row[7].text

    def get_estimation_vs_last_year_percent_value(self, row):
        table = Table(self.driver, self.table)
        current_row = table.get_row(row)
        return current_row[8].text
