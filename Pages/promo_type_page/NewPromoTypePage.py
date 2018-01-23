import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import utilities
from Pages.promo_detail_page.PromoDetailPage import PromoDetailPage
from utilities.BaseForm import BaseForm
from utilities.DataBase import DataBase
from utilities.Parser import Parser
from utilities.Table import Table


class NewPromoTypePage(BaseForm):
    browser = Parser().get_browser_name()

    """HEADER"""
    back_button = (By.CSS_SELECTOR, 'a[class*="k-button k-button-icontex"]')
    save_button = (By.ID, 'save')
    new_promo_button = (By.ID, 'new-promo')
    create_template_button = (By.ID, 'new-template')
    title = (By.TAG_NAME, 'h2')

    """PROMO TYPE INFORMATION FORM"""
    table = (By.CLASS_NAME, 'b-form__content')

    """Editable_elements"""
    """Really input"""
    name_input = (By.CSS_SELECTOR, 'input[data-bind="value: Name"]')
    key_promotion_name_input = (By.CSS_SELECTOR, 'input[data-bind="value: KeyName"]')
    key_promotion_code_input = (By.CSS_SELECTOR, 'input[data-bind="value: KeyCode"]')
    number_validy_input = (By.CSS_SELECTOR, 'input[data-bind="value: ValidityNumber"]')
    number_range_input = (By.CSS_SELECTOR, 'input[data-bind="value: RangeNumber"]')
    external_agency_input = (By.CSS_SELECTOR, 'input[data-bind="value: ExternalAgency"]')
    duration_input = (By.CSS_SELECTOR, 'input[data-bind="value: Duration"]')

    """Dropdown (getting from the parent of the input)"""
    promo_kind_input = (By.CSS_SELECTOR, 'input[data-bind="value: PromoKindId"]')
    validity_input = (By.CSS_SELECTOR, 'input[data-bind="value: Validity"]')
    start_date_validy_input = (By.CSS_SELECTOR, 'input[data-bind="value: DayOfWeek"]')
    date_validy_input = (By.CSS_SELECTOR, 'input[data-bind="value: Date"]')
    range_input = (By.CSS_SELECTOR, 'input[data-bind="value: Range"]')
    how_to_order_input = (By.CSS_SELECTOR, 'input[data-bind="value: HowToOrder"]')
    workflow_input = (By.CSS_SELECTOR, 'input[data-bind="value: Workflow"]')

    """Checkboxes"""
    setting_targets = (By.CSS_SELECTOR, 'input[data-bind="checked: IsSettingTargets"]')
    split_KPI_per_pages = (By.CSS_SELECTOR, 'input[data-bind="checked: IsSplitKPIPerPages"]')
    one_supplier = (By.CSS_SELECTOR, 'input[data-bind="checked: IsOneSupplier"]')
    only_goods = (By.CSS_SELECTOR, 'input[data-bind="checked: IsOnlyGoodsOnStock"]')
    order_planning = (By.CSS_SELECTOR, 'input[data-bind="checked: IsOrderPlanning"]')
    mutation = (By.CSS_SELECTOR, 'input[data-bind="checked: IsMutation"]')
    electronic_version = (By.CSS_SELECTOR, 'input[data-bind="checked: IsElectronicVersion"]')
    web_globus = (By.CSS_SELECTOR, 'input[data-bind="checked: IsWebGlobus"]')
    web_shop = (By.CSS_SELECTOR, 'input[data-bind="checked: IsWebShop"]')
    direct_mail = (By.CSS_SELECTOR, 'input[data-bind="checked: IsDirectMail"]')
    shelf_labels = (By.CSS_SELECTOR, 'input[data-bind="checked: IsShelfLabels"]')
    defined_direct_costs = (By.CSS_SELECTOR, 'input[data-bind="checked: IsDefinedDirectCosts"]')
    suppliers_contributions = (By.CSS_SELECTOR, 'input[data-bind="checked: IsSupplierContributions"]')

    """Multiselect dropdown"""
    parametrs_split_input = (By.CSS_SELECTOR, 'input[data-bind="value: Parameters"]')
    assortment_input = (By.CSS_SELECTOR, 'input[data-bind="value: Assortment"]')
    region_input = (By.CSS_SELECTOR, 'input[data-bind="value: Region"]')
    supermarket_input = (By.CSS_SELECTOR, 'input[data-bind="value: Supermarket"]')
    distribution_channel_input = (By.CSS_SELECTOR, 'input[data-bind="value: DistributionChannel"]')
    advertising_channel_input = (By.CSS_SELECTOR, 'input[data-bind="value: AdvertisingChannel"]')
    print_advertising_input = (By.CSS_SELECTOR, 'input[data-bind="value: PrintAdvertising"]')
    format_input = (By.CSS_SELECTOR, 'input[data-bind="value: Format"]')
    distribution_input = (By.CSS_SELECTOR, 'input[data-bind="value: Distribution"]')
    type_of_labels_input = (By.CSS_SELECTOR, 'input[data-bind="value: TypeOfLabeles"]')
    pos_support_input = (By.CSS_SELECTOR, 'input[data-bind="value: POSSupport"]')

    """Calendar"""
    validy_from_input = (By.CSS_SELECTOR, 'input[data-bind="value: ValidFrom"]')
    validy_to_input = (By.CSS_SELECTOR, 'input[data-bind="value: ValidTo"]')

    def get_form(self):
        return self.wait.until(EC.presence_of_element_located(self.table), 'Table is absent') \
            .find_element_by_tag_name('table')

    def get_title(self):
        return self.wait.until(EC.visibility_of_element_located(self.title),
                               '"New promo type" title is not visible').text

    def get_all_labels_text(self):
        labels_list = []
        form = Table(self.driver, self.get_form())
        cells = form.get_all_cells_element()
        for cell in cells:
            labels_list.append(cell[0].text)
        return labels_list

    def is_supermarket_required(self):
        field = self.wait.until(EC.presence_of_element_located(self.supermarket_input))
        div_parent_element = WebDriverWait(field, 5).until(EC.presence_of_element_located((By.XPATH, '../..')))
        if 'required' in div_parent_element.get_attribute('class'):
            return True
        else:
            return False

    def choose_promo_kind(self, state):
        state_dict = {
            'Promo kind 1': 0,
            'Promo kind 2': 1,
            'Promo kind 3': 2
        }
        dropdown = self.get_dropdown(self.promo_kind_input)
        self.click_and_select_dropdown_option(state_dict, state, '"Promo kind" is not choosable', dropdown)
        return self

    def choose_validity(self, state):
        state_dict = {
            'Day(s)': 1,
            'Month(s)': 2,
            'Quater(s)': 0
        }
        dropdown = self.get_dropdown(self.validity_input)
        self.click_and_select_dropdown_option(state_dict, state, '"Validity" is not choosable', dropdown)
        return self

    def choose_start_date(self, state):
        state_dict = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }
        dropdown = self.get_dropdown(self.start_date_validy_input)
        if self.is_dropdown_disabled(self.start_date_validy_input):
            raise Exception('"Start date (day of week)" is disabled')
        self.click_and_select_dropdown_option(state_dict, state, '"Start date (day of week)" is not choosable', dropdown)
        return self

    def choose_date(self, state):
        state_dict = {
            'First day of month': 0,
            'First day of quarter': 1
        }
        dropdown = self.get_dropdown(self.date_validy_input)
        if self.is_dropdown_disabled(self.date_validy_input):
            raise Exception('"Date" is disabled')
        self.click_and_select_dropdown_option(state_dict, state, '"Date" is not choosable', dropdown)
        return self

    def choose_range(self, state):
        state_dict = {
            'Article(s)': 0,
            'Page(s)': 1,
            'Vaucher(s)': 2
        }
        dropdown = self.get_dropdown(self.range_input)
        self.click_and_select_dropdown_option(state_dict, state, '"Range" is not choosable', dropdown)
        return self

    def choose_how_to_order(self, state):
        state_dict = {
            'Action planning': 0,
            'cross-dock': 1,
            'pre-orders': 2
        }
        dropdown = self.get_dropdown(self.how_to_order_input)
        self.click_and_select_dropdown_option(state_dict, state, '"How to order" is not choosable', dropdown)
        return self

    def choose_workflow(self, state):
        workflow_list = DataBase(utilities.DataBase.get_connection_parameters()) \
            .select_in_list("SELECT [Name] FROM [PromoToolGlobus].[PromoTool].[WorkflowTemplate]")
        state_dict = {}
        i = 0
        for element in workflow_list:
            state_dict[element[0]] = i
            i += 1
        if state not in state_dict:
            state = workflow_list[0][0]
        dropdown = self.get_dropdown(self.workflow_input)
        self.click_and_select_dropdown_option(state_dict, state, '"Workflow" is not choosable', dropdown)
        return self

    def click_back_button(self):
        self.wait.until(EC.element_to_be_clickable(self.back_button), 'Back button is not clicable').click()
        return self

    def click_save_button(self):
        button = self.wait.until(EC.visibility_of_element_located(self.save_button), 'Save button is missing')
        if self.is_button_disabled(self.save_button, 'Save'):
           raise Exception('"Save" button should be active')
        else:
            button.click()
        return self

    def choose_assortment(self):
        input = self.wait.until(EC.presence_of_element_located(self.assortment_input),
                                '"Assortment" field is absent')
        assortment = WebDriverWait(input, 5).until(EC.presence_of_element_located((By.XPATH, '..')),
                                                   '"Assortment" field is invisible')
        self.driver.execute_script("return arguments[0].scrollIntoView();", assortment)
        assortment.click()
        self.get_widget_window('"Assortment" window is invisible')
        list = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'span[class="k-in"]')),
                               'There is no option for Assortment')
        for el in list:
            el.click()
        self.close_widget_window()
        return self

    def choose_assortment_by_index(self, list_of_index):
        input = self.wait.until(EC.presence_of_element_located(self.assortment_input),
                                '"Assortment" field is absent')
        assortment = WebDriverWait(input, 5).until(EC.presence_of_element_located((By.XPATH, '..')),
                                                   '"Assortment" field is invisible')
        self.driver.execute_script("return arguments[0].scrollIntoView();", assortment)
        assortment.click()
        self.get_widget_window('"Assortment" window is invisible')
        list = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'span[class="k-in"]')),
                               'There is no option for Assortment')
        try:
            for index in list_of_index:
                list[index].click()
        except IndexError:
            print('There is no element with index ' + str(list_of_index))
        self.close_widget_window()
        return self

    def choose_supermarket(self):
        input = self.wait.until(EC.presence_of_element_located(self.supermarket_input),
                                '"Supermarket" field is absent')
        supermarket = WebDriverWait(input, 5).until(EC.presence_of_element_located((By.XPATH, '..')),
                                                    '"Supermarket" field is invisible')
        self.driver.execute_script("return arguments[0].scrollIntoView();", supermarket)
        supermarket.click()
        self.get_widget_window('"Supermarket" window is invisible')
        list = self.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'span[class="k-in"]')),
                               'There is no option for Supermarket')
        for el in list:
            el.click()
        self.close_widget_window()
        return self

    def click_create_template_button(self):
        button = self.wait.until(EC.visibility_of_element_located(self.create_template_button),
                        '"Create template" button is not visible')
        if self.is_button_disabled(self.create_template_button) is True:
            time.sleep(1)
            if self.is_button_disabled(self.create_template_button) is True:
                raise Exception('"Create template" button should be active')
        button.click()
        return PromoDetailPage(self.driver)

    def click_new_promo_button(self):
        button = self.wait.until(EC.visibility_of_element_located(self.new_promo_button),
                                 'New Promo button is invisible')
        if self.is_button_disabled(self.new_promo_button) is True:
            raise Exception('New Promo button should be active')
        button.click()
        return PromoDetailPage(self.driver)


    def click_yes_to_pop_up_dialog(self):
        toolbar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[role="toolbar"]')),
                                  'Button group is not visible in Message pop up')

        WebDriverWait(toolbar, 5).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, 'li[role="button"]')),
                                        'Buttons are not visible in Message pop up')[0].click()
        return PromoDetailPage(self.driver)

    def is_assortment_from_additional_info_disabled(self):
        field = self.wait.until(EC.presence_of_all_elements_located(self.assortment_input))
        assortment = field[len(field)-1]
        if 'true' in assortment.get_attribute('aria-disabled'):
            return True
        else:
            return False

    def get_assortment_value_from_additional_info(self):
        assortment_fields = self.wait.until(EC.presence_of_all_elements_located(self.assortment_input),
                                'Assortment field for additional info is absent')
        field = assortment_fields[len(assortment_fields)-1]
        div_parent_element = WebDriverWait(field, 5).until(EC.visibility_of_element_located((By.XPATH, '..')))
        self.driver.execute_script("return arguments[0].scrollIntoView();", div_parent_element)
        list_elements = div_parent_element.find_elements_by_tag_name('li')
        list_options_text = []
        for el in list_elements:
            list_options_text.append(el.text)
        return list_options_text
