from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utilities.BaseWidget import BaseWidget


class WorkflowWidget(BaseWidget):

    def __init__(self, driver):
        super(WorkflowWidget, self).__init__(driver,
                                                  (By.CSS_SELECTOR, 'div[class="b-promo-action-workflow"]'),
                                                  'Workflow')





