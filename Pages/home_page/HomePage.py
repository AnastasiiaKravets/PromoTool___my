from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import unittest


class HomePage(BasePage):
    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

    """HEADER"""
    search = (By.CLASS_NAME, 'b-search__open')
    user_name = (By.CLASS_NAME, 'b-user__name')
    user_info = (By.CLASS_NAME, 'b-user__info')
    user_actions_info = (By.CLASS_NAME, 'b-user-actions__info')

    """Header subelements USER ACTION LIST"""
    user_action_list = (By.CLASS_NAME, 'b-user__action')
    exit_index = 0
    change_pass_index = 1
    settings_index = 2

    """Profile selection"""
    profile_selection_list = (By.CLASS_NAME, 'k-input')
    profile_list_not_selected = (By.CSS_SELECTOR, "li:nth-child(1)")
    store_profile_button = (By.XPATH, "//li[@tabindex='-1'][@data-offset-index='0']")
    office_profile_button = (By.XPATH,
                             "(//div[@class='k-animation-container']/div/div[2]/ul/li[2])[2]")

    """Header subelements USER ACTIONS INFO"""
    # Не описане

    """MENUBAR"""  # Remember about scroll into view
    home_menuitem = (By.CSS_SELECTOR, "a[href = '/home']")
    promo_action_menuitem = (By.CSS_SELECTOR, "a[href = '/promo-actions']")
    promo_order_menuitem = (By.CSS_SELECTOR, "a[href = '/promo-order']")
    event_calendar_menuitem = (By.CSS_SELECTOR, "a[href = '/event-calendar']")
    evaluatiion_menuitem = (By.CSS_SELECTOR, "a[href = '/evaluation']")
    # suppliers_menuitem = (By.CSS_SELECTOR, "a[href = '/promo-order']")
    collisions_menuitem = (By.CSS_SELECTOR, "a[href = '/collisions-list']")
    # promo_management_menuitem = (By.CSS_SELECTOR, "a[href = '/promo-order']")
    product_database_menuitem = (By.CSS_SELECTOR, "a[href = '/product-database']")
    # internal_reports_menuitem = (By.CSS_SELECTOR, "a[href = '/promo-order']")
    users_menuitem = (By.CSS_SELECTOR, "a[href = '/admin/users']")
    roles_menuitem = (By.CSS_SELECTOR, "a[href = '/admin/roles']")
    operations_menuitem = (By.CSS_SELECTOR, "a[href = '/admin/operations']")
    parametrs_management_menuitem = (By.CSS_SELECTOR, "a[href = '/admin/dictionaries']")
    promo_type_menuitem = (By.CSS_SELECTOR, "a[href = '/promo-type']")
    localization_management_menuitem = (By.CSS_SELECTOR, "a[href = '/admin/locale']")
    reports_menuitem = (By.CSS_SELECTOR, "a[href = '/reports-list']")

    pop_up_labels_list = (By.CLASS_NAME, 'b-form__label')
    current_pass_label_index = 0
    new_pass_label_index = 1
    confirm_pass_label_index = 2

    old_password_field = (By.ID, 'oldUserPassword')
    new_password_field = (By.ID, 'newUserPassword')
    confirm_password_field = (By.ID, 'confirmUserPassword')

    pop_up_buttons = (By.CLASS_NAME, 'b-user__password-popup-buttons')
    pop_up_ok_button_index = 0
    pop_up_cancel_button_index = 1

    change_pass_notification = (By.CLASS_NAME, 'k-notification-wrap')
    wrong_password_notification = (By.CLASS_NAME, 'b-user__password-popup-error')

    def get_popup_ok_button(self):
        buttons = self.wait.until(EC.visibility_of_element_located(self.pop_up_buttons),
                                  'Pop up buttons are not visible')
        return buttons.find_elements_by_class_name('b-button')[self.pop_up_ok_button_index]

    def get_popup_cancel_button(self):
        buttons = self.wait.until(EC.visibility_of_element_located(self.pop_up_buttons),
                                  'Pop up buttons are not visible')
        return buttons.find_elements_by_class_name('b-button')[self.pop_up_cancel_button_index]

    def wrong_password_notification_text(self):
        notification = self.wait.until(EC.visibility_of_all_elements_located(self.wrong_password_notification),
                                       'Wrong password notification is not displayed')
        return notification[len(notification) - 1].text

    def username_text(self):
        username = self.wait.until(EC.visibility_of_element_located(self.user_name), 'Username is not visible')
        return username.text

    def click_user_info(self):
        info = self.wait.until(EC.visibility_of_element_located(self.user_info), 'User info is not visible')
        info.click()
        return self

    def click_change_password(self):
        change_password = self.wait.until(EC.visibility_of_all_elements_located(self.user_action_list),
                                          'The Change password is not visible')[self.change_pass_index]
        change_password.click()
        return self

    def enter_current_password(self, password=''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.old_password_field),
                                      'The Old password input is not visible')
        input_field.send_keys(password)
        return self

    def enter_new_password(self, password=''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.new_password_field),
                                      'The New password input is not visible')
        input_field.send_keys(password)
        return self

    def enter_confirm_password(self, password=''):
        input_field = self.wait.until(EC.visibility_of_element_located(self.confirm_password_field),
                                      'The Confirm password input is not visible')
        input_field.send_keys(password)
        return self

    def current_pass_label_text(self):
        label = self.wait.until(EC.visibility_of_any_elements_located(self.pop_up_labels_list),
                                'Pop up labels is not visible')[self.current_pass_label_index]
        return label.text

    def new_pass_label_text(self):
        label = self.wait.until(EC.visibility_of_any_elements_located(self.pop_up_labels_list),
                                'Pop up labels is not visible')[self.new_pass_label_index]
        return label.text

    def confirm_pass_label_text(self):
        label = self.wait.until(EC.visibility_of_any_elements_located(self.pop_up_labels_list),
                                'Pop up labels is not visible')[self.confirm_pass_label_index]
        return label.text

    def current_password_placeholder(self):
        input_field = self.wait.until(EC.visibility_of_element_located(self.old_password_field),
                                      'The Old password input is not visible')
        return input_field.get_attribute('placeholder')

    def new_password_placeholder(self):
        input_field = self.wait.until(EC.visibility_of_element_located(self.new_password_field),
                                      'The New password input is not visible')
        return input_field.get_attribute('placeholder')

    def confirm_password_placeholder(self):
        input_field = self.wait.until(EC.visibility_of_element_located(self.confirm_password_field),
                                      'The Confirm password input is not visible')
        return input_field.get_attribute('placeholder')

    def click_exit(self):
        click_exit_var = self.wait.until(EC.visibility_of_all_elements_located(self.user_action_list),
                                         'The Exit is not visible')[self.exit_index]
        click_exit_var.click()
        return self

    def click_pop_up_ok_button(self):
        ok_button = self.get_popup_ok_button()
        if 'disabled' in ok_button.get_attribute('class'):
            unittest.TestCase.fail(unittest.TestCase, 'The Ok button is inactive')
        else:
            ok_button.click()

    def click_pop_up_cancel_button(self):
        self.get_popup_cancel_button().click()
        return self

    def success_change_password_notification(self):
        try:
            el = self.wait.until(EC.visibility_of_element_located(self.change_pass_notification))
            return el.text
        except exceptions.TimeoutException:
            return "Change password notification is abscent"

    def click_users_menuitem(self):
        users = self.wait.until(EC.element_to_be_clickable(self.users_menuitem), 'Users menuitem is not clickable')
        self.driver.execute_script("return arguments[0].scrollIntoView();", users)
        users.click()

    def click_roles_menuitem(self):
        roles = self.wait.until(EC.element_to_be_clickable(self.roles_menuitem), 'Roles menu is not clickable')
        self.driver.execute_script("return arguments[0].scrollIntoView();", roles)
        roles.click()

    def click_evaluation_menuitem(self):
        menuitem = self.wait.until(EC.element_to_be_clickable(self.evaluatiion_menuitem),
                                   'Evaluation menuitem is not clickable')
        self.driver.execute_script("return arguments[0].scrollIntoView();", menuitem)
        menuitem.click()

    def click_promo_type_menuitem(self):
        promo_type = self.wait.until(EC.element_to_be_clickable(self.promo_type_menuitem), 'Promo type menu is not clickable')
        self.driver.execute_script("return arguments[0].scrollIntoView();", promo_type)
        promo_type.click()
        return self

    def list_store_profile_select(self):
        # Locate profile selection list
        try:
            profile_menu = self.wait.until(EC.visibility_of_element_located(self.profile_selection_list),
                                           'Profile selection list is not visible')
        except Exception as error:
            print('An error occurred: %s' % error)
        profile_menu.click()
        # locate Store Profile
        found_list_A = self.wait.until(EC.visibility_of_element_located(self.store_profile_button),
                                       'Store profile list is not visible')
        # Choose/click on the Store profile 
        found_list_A.click()

        return self

    def list_office_profile_select(self):
        # Locate profile selection list
        try:
            profile_menu = self.wait.until(EC.visibility_of_element_located(self.profile_selection_list),
                                           'Profile selection list is not visible')
        except Exception as error:
            print('An error occurred: %s' % error)

        profile_menu.click()
        # locate Office Profile
        try:
            found_list_B = self.wait.until(EC.visibility_of_element_located(self.office_profile_button),
                                           'Office profile list is not visible')
        except Exception as error:
            print('An error occurred: %s' % error)
        # Choose/click on the Office profile 
        found_list_B.click()

        return self



