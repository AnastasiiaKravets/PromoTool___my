from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Pages.promo_detail_page.NotePopUp import NotePopUp
from Pages.promo_detail_page.TagPopUp import TagPopUp
from utilities.BaseForm import BaseForm


class BasicInformation(BaseForm):

    title = (By.CLASS_NAME, 'b-form__title-text')

    code_input = (By.CSS_SELECTOR, 'input[data-bind="value: Code"]')
    name_input = (By.CSS_SELECTOR, 'input[data-bind="value: Name"]')
    promo_type_input = (By.CSS_SELECTOR, 'input[data-bind="value: PromoActionTypeName"]')
    validity_from_input = (By.CSS_SELECTOR, 'input[data-bind="value: ActiveFrom"]')
    validity_to_input = (By.CSS_SELECTOR, 'input[data-bind="value: ActiveTo"]')
    description_input = (By.CSS_SELECTOR, 'input[data-bind="value: Description"]')
    status_input = (By.CSS_SELECTOR, 'input[data-bind="value: StateName"]')
    note_input = (By.CLASS_NAME, 'b-custom-notes__buttons')
    external_code_input = (By.CSS_SELECTOR, 'input[data-bind="value: ExtCode"]')
    promo_kind_input = (By.CSS_SELECTOR, 'input[data-bind="value: PromoKindId"]')
    confirm_checkbox = (By.CSS_SELECTOR, 'input[data-bind="checked: IsConfirmed"]')
    deadline_input = (By.CSS_SELECTOR, 'input[data-bind="value: Deadline"]')
    tag_input = (By.CLASS_NAME, 'b-custom-tags__buttons')


    def __init__(self, driver):
        self.driver = driver
        self.form = WebDriverWait(self.driver, 10)\
            .until(EC.presence_of_element_located((By.CLASS_NAME, 'b-promo-detail__basic-info')),
                   '"Basic information" form is absent')
        self.wait = WebDriverWait(self.form, 10)

    def get_title_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.title), '"Basic information" title is absent').text

    def get_all_labels_text(self):
        list = []
        labels = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'label.b-form__label')),
                                 'There are no labels')
        for el in labels:
            list.append(el.text)
        return list

    def is_note_existed(self):
        notes = self.wait.until(EC.presence_of_element_located(self.note_input), '"Notes" input is absent')
        field = WebDriverWait(notes, 5).until(EC.presence_of_element_located((By.XPATH, './/div')))
        if 'field-empty' in field.get_attribute('class'):
            return False
        else:
            return True

    def is_tag_existed(self):
        tag = self.wait.until(EC.presence_of_element_located(self.tag_input), '"Tag" input is absent')
        field = WebDriverWait(tag, 5).until(EC.presence_of_element_located((By.XPATH, './/div')))
        if 'field-empty' in field.get_attribute('class'):
            return False
        else:
            return True

    def click_notes(self):
        notes = self.wait.until(EC.presence_of_element_located(self.note_input), '"Notes" input is absent')
        field = WebDriverWait(notes, 5).until(EC.presence_of_element_located((By.XPATH, './/div')))
        field.click()
        return NotePopUp(self.driver)

    def click_tag(self):
        tag = self.wait.until(EC.presence_of_element_located(self.tag_input), '"Tag" input is absent')
        field = WebDriverWait(tag, 5).until(EC.presence_of_element_located((By.XPATH, './/div')))
        field.click()
        return TagPopUp(self.driver)











