from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.BasePopUp import BasePopUp


class NotePopUp(BasePopUp):

    create_new_button = (By.CLASS_NAME, 'create-new-note-btn')
    save_button = (By.CLASS_NAME, 'save-note-btn')
    note_type_header = (By.CSS_SELECTOR, 'th[data-field="noteTypeValue"]')
    note_text_header = (By.CSS_SELECTOR, 'th[data-field="NoteTextForGrid"]')

    def __init__(self, driver):
        super(NotePopUp, self).__init__(driver, 'Note')

    def get_table_content(self):
        return self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'k-grid-content')), "'Note' table is abscent")





