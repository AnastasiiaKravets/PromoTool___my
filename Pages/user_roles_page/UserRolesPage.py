from selenium.common.exceptions import TimeoutException
from BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utilities
from utilities.DataBase import DataBase
from utilities import XpathFindText
import time
from utilities.Parser import Parser
from utilities.Table import Table

class UserRolesPage(BasePage):
    def __init__(self, driver_instance):
        self.driver = driver_instance
        self.wait = WebDriverWait(self.driver, 10)

    # Roles title on the upper-right corner, under user menu
    roles_title = (By.CSS_SELECTOR, "a#dashboard")

    # Add Roles button on the upper-left side
    add_role_button_css = (By.CSS_SELECTOR, "section#l-content a.k-button.k-button-icontext.button-success.k-grid-add")
    # Roles table full (left table)
    roles_table_left_css = (By.CSS_SELECTOR, "div.b-admin-roles-grid-wrapper.k-grid.k-widget.k-reorderable.k-editable")

    # roles_table_left_content = (By.CSS_SELECTOR, "k-grid-content.k-auto-scrollable")

    roles_table_element_locator = (By.CSS_SELECTOR, "table.k-selectable")

    # Roles table elements (left table for adding roles) - 4 columns,
    # and their filter button in the shape of triangle (triangle without one side)
    roles_table_first_column_css = (By.CSS_SELECTOR,
        "div.b-admin-roles-grid-wrapper.k-grid.k-widget.k-reorderable.k-editable th[scope='col'][data-index='0']")
    privileges_table_first_column_css = (By.CSS_SELECTOR,
                                "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='0']")
    roles_table_id_column_arrow = (By.CSS_SELECTOR,
        "div.b-admin-roles-grid-wrapper.k-grid.k-widget.k-reorderable.k-editable th[scope='col'][data-index='0'] \
                                                                                        span.k-icon.k-i-arrowhead-s")
    roles_table_second_column_css = (By.CSS_SELECTOR,
        "div.b-admin-roles-grid-wrapper.k-grid.k-widget.k-reorderable.k-editable th[scope='col'][data-index='1']")
    privileges_table_second_column_css = (By.CSS_SELECTOR,
                                "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='1']")
    roles_table_name_column_arrow = (By.CSS_SELECTOR,
        "div.b-admin-roles-grid-wrapper.k-grid.k-widget.k-reorderable.k-editable th[scope='col'][data-index='1'] \
                                                                                        span.k-icon.k-i-arrowhead-s")
    roles_table_third_column_css = (By.CSS_SELECTOR,
        "div.b-admin-roles-grid-wrapper.k-grid.k-widget.k-reorderable.k-editable th[scope='col'][data-index='2']")
    privileges_table_third_column_css = (By.CSS_SELECTOR,
                                "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='2']")
    roles_table_isactive_column_arrow = (By.CSS_SELECTOR,
        "div.b-admin-roles-grid-wrapper.k-grid.k-widget.k-reorderable.k-editable th[scope='col'][data-index='2'] \
                                                                                        span.k-icon.k-i-arrowhead-s")
    roles_table_fourth_column_css = (By.CSS_SELECTOR,
        "div.b-admin-roles-grid-wrapper.k-grid.k-widget.k-reorderable.k-editable  th[scope='col'][data-index='3']")
    privileges_table_fourth_column_css = (By.CSS_SELECTOR,
                                "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='3']")

    privileges_table_fifth_column_css = (By.CSS_SELECTOR,
                                "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='4']")

    # Save changes button on the upper-right side
    save_changes_button_css = (By.CSS_SELECTOR,
                           "a.k-button.k-button-icontext.button-success.k-grid-saveOperations")

    save_changes_button_locator = (By.CSS_SELECTOR, "a[class $='saveOperations']")

    save_changes_button_icon_css = (By.CSS_SELECTOR,
                "a.k-button.k-button-icontext.button-success.k-grid-saveOperations  span.k-sprite.fa.fa-save")
    # Whole privileges table (right table)
    privileges_table_css = (By.CSS_SELECTOR,
                                            "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable")
    # Privileges table, without any additional elements
    privileges_table_element_locator = (By.XPATH, "(//div[@class='k-grid-content k-auto-scrollable']/*)[2]")

    # Privileges table elements (right table for adding privileges) - 4 columns,
    # and their filter button in the shape of triangle (triangle without one side)
    privileges_table_checkbox_column_css = (By.CSS_SELECTOR,
                            "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='0']")
    privileges_table_id_column_css = (By.CSS_SELECTOR,
                            "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='1']")
    privileges_table_id_column_menu_css = (By.CSS_SELECTOR,
                        "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='1'] \
                                                                                    span.k-icon.k-i-arrowhead-s")
    privileges_table_operation_name_column_css = (By.CSS_SELECTOR,
                    "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='2']")
    privileges_table_operation_name_column_menu_css = (By.CSS_SELECTOR,
                        "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='2'] \
                                                                                    span.k-icon.k-i-arrowhead-s")
    privileges_table_operation_url_column_css = (By.CSS_SELECTOR,
                        "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='3']")
    privileges_table_operation_url_column_menu_css = (By.CSS_SELECTOR,
                        "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='3'] \
                                                                                    span.k-icon.k-i-arrowhead-s")
    privileges_table_is_active_column_css = (By.CSS_SELECTOR,
                        "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='4']")
    privileges_table_is_active_column_arrow = (By.CSS_SELECTOR,
                        "div.b-admin-operations-grid-wrapper.k-grid.k-widget.k-reorderable [data-index='4'] \
                                                                                    span.k-icon.k-i-arrowhead-s")

    dialog_window_remove_role_element = (By.CSS_SELECTOR, "div.k-widget.k-dialog.k-window.k-dialog-centered")

    privileges_checkboxes = (By.CSS_SELECTOR, "div.b-admin-operations-grid-wrapper.k-grid.k-widget."
                                                                        "k-reorderable input[type='checkbox']")

    # get locator for all checkboxes of privileges table
    all_tr_nodes_checkboxes = (By.CSS_SELECTOR, "div.b-admin-operations-grid-wrapper.k-grid."
                                                "k-widget.k-reorderable tr")
    # locator for drop-down menu - columns checkboxes - role table - ID column
    id_column_checkboxes_drop_down = (By.CSS_SELECTOR, "ul[role='menu'] li[role='menuitem']:nth-child(1)")
    role_name_checkboxes_drop_down = (By.CSS_SELECTOR, "ul[role='menu'] li[role='menuitem']:nth-child(2)")
    is_active_checkboxes_drop_down = (By.CSS_SELECTOR, "ul[role='menu'] li[role='menuitem']:nth-child(3)")
    operations_checkboxes_drop_down = (By.CSS_SELECTOR, "ul[role='menu'] li[role='menuitem']:nth-child(4)")
    # locator for drop-down menu - columns checkboxes - privilege table
    id_column_checkboxes_drop_down_privilege = (By.CSS_SELECTOR, "ul[role='menu'] li[role='menuitem']:nth-child(1)")
    operation_name_checkboxes_drop_down_privilege = (By.CSS_SELECTOR, "ul[role='menu'] li[role='menuitem']:nth-child(2)")
    operation_url_checkboxes_drop_down_privilege = (By.CSS_SELECTOR, "ul[role='menu'] li[role='menuitem']:nth-child(3)")
    is_active_checkboxes_drop_down_privilege = (By.CSS_SELECTOR, "ul[role='menu'] li[role='menuitem']:nth-child(4)")

    def locator_id_column(self):
        return self.roles_table_first_column_css

    def locator_id_column_privilege(self):
        return self.privileges_table_second_column_css

    def locator_role_name_column(self):
        return self.roles_table_second_column_css

    def locator_operation_name_column_privilege(self):
        return self.privileges_table_third_column_css

    def locator_is_active_column(self):
        return self.roles_table_third_column_css

    def locator_operation_url_column_privilege(self):
        return self.privileges_table_fourth_column_css

    def locator_operations_column(self):
        return self.roles_table_fourth_column_css

    def locator_is_active_column_privilege(self):
        return self.privileges_table_fifth_column_css

    def locators_all_checkboxes_except_id(self):
        checkbox_list = [self.role_name_checkboxes_drop_down, self.is_active_checkboxes_drop_down,
                         self.operations_checkboxes_drop_down]
        return checkbox_list

    def locators_all_checkboxes_except_id_priv(self):
        checkbox_list = [self.operation_name_checkboxes_drop_down_privilege,
                         self.operation_url_checkboxes_drop_down_privilege,
                         self.is_active_checkboxes_drop_down_privilege]
        return checkbox_list

    def locators_all_checkboxes_except_role_name(self):
        checkbox_list = [self.id_column_checkboxes_drop_down, self.is_active_checkboxes_drop_down,
                         self.operations_checkboxes_drop_down]
        return checkbox_list

    def locators_all_checkboxes_except_operation_name_priv(self):
        checkbox_list = [self.id_column_checkboxes_drop_down_privilege,
                         self.operation_url_checkboxes_drop_down_privilege,
                         self.is_active_checkboxes_drop_down_privilege]
        return checkbox_list

    def locators_all_checkboxes_except_is_active(self):
        checkbox_list = [self.id_column_checkboxes_drop_down, self.role_name_checkboxes_drop_down,
                         self.operations_checkboxes_drop_down]
        return checkbox_list

    def locators_all_checkboxes_except_operation_url_priv(self):
        checkbox_list = [self.id_column_checkboxes_drop_down_privilege,
                         self.operation_name_checkboxes_drop_down_privilege,
                         self.is_active_checkboxes_drop_down_privilege]
        return checkbox_list

    def locators_all_checkboxes_except_operations(self):
        checkbox_list = [self.id_column_checkboxes_drop_down, self.role_name_checkboxes_drop_down,
                         self.is_active_checkboxes_drop_down]
        return checkbox_list

    def locators_all_checkboxes_except_is_active_priv(self):
        checkbox_list = [self.id_column_checkboxes_drop_down_privilege,
                         self.operation_name_checkboxes_drop_down_privilege,
                         self.operation_url_checkboxes_drop_down_privilege]
        return checkbox_list

    def role_title(self):
        roles_id = self.wait.until(EC.visibility_of_element_located(self.roles_title),
                                      'Roles module is not visible')
        role_bool = roles_id.is_displayed()
        return role_bool

    def add_role_button_bool(self):
        role_add_button = self.wait.until(EC.visibility_of_element_located(self.add_role_button_css),
                                      'Add Role button is not visible')
        # role_add_button_bool = role_add_button.is_displayed()
        role_add_button_bool = role_add_button.is_enabled()
        return role_add_button_bool

    def roles_table_bool(self):
        roles_table_webelement = self.wait.until(EC.visibility_of_element_located(self.roles_table_left_css),
                                      'Roles table is not visible')
        roles_table_bool = roles_table_webelement.is_displayed()
        return roles_table_bool

    def roles_table_id_column_bool(self):
        roles_table_id_column_elem = self.wait.until(EC.visibility_of_element_located(self.roles_table_first_column_css),
                                                 'Column "ID" is not visible')
        id_column_bool = roles_table_id_column_elem.is_displayed()

        roles_table_id_column_menu_elem = self.wait.until(EC.visibility_of_element_located(
                                        self.roles_table_id_column_arrow), 'Column "ID" arrow menu is not enabled')
        id_column_menu_bool = roles_table_id_column_menu_elem.is_enabled()

        return id_column_bool and id_column_menu_bool

    def roles_table_role_name_column_bool(self):
        roles_table_role_name_column_elem = self.wait.until(EC.visibility_of_element_located(
                                        self.roles_table_second_column_css), 'Column "Role name" is not visible')
        role_name_column_bool = roles_table_role_name_column_elem.is_displayed()

        roles_table_name_column_menu_elem = self.wait.until(EC.visibility_of_element_located(
                                self.roles_table_name_column_arrow), 'Column "Role name" arrow menu is not enabled')
        role_name_column_menu_bool = roles_table_name_column_menu_elem.is_enabled()

        return role_name_column_bool and role_name_column_menu_bool

    def roles_table_isActive_column_bool(self):
        roles_table_isactive_column_elem = self.wait.until(EC.visibility_of_element_located(
                                        self.roles_table_third_column_css), 'Column "isActive" is not visible')
        isactive_column_bool = roles_table_isactive_column_elem.is_displayed()

        roles_table_isactive_column_menu_elem = self.wait.until(EC.visibility_of_element_located(
                        self.roles_table_isactive_column_arrow), 'Column "isActive" arrow menu is not enabled')
        isactive_column_menu_bool = roles_table_isactive_column_menu_elem.is_enabled()

        return isactive_column_bool and isactive_column_menu_bool

    def roles_table_operations_column_bool(self):
        roles_table_operations_column_elem = self.wait.until(EC.visibility_of_element_located(
                                        self.roles_table_fourth_column_css), 'Column "Operations" is not visible')
        operations_column_bool = roles_table_operations_column_elem.is_displayed()

        return operations_column_bool

    # -- Right table with privileges begins here -- #
    def save_changes_button_bool(self):
        save_changes_button = self.wait.until(EC.visibility_of_element_located(self.save_changes_button_css),
                                      'Save changes button is not visible')
        save_changes_button_bool = save_changes_button.is_displayed()

        save_changes_button_icon = self.wait.until(EC.visibility_of_element_located(self.save_changes_button_icon_css),
                                              'Save changes icon is not visible')
        save_changes_button_icon_bool = save_changes_button_icon.is_displayed()

        return save_changes_button_bool and save_changes_button_icon_bool

    def privileges_table_bool(self):
        privileges_table_elem = self.wait.until(EC.visibility_of_element_located(
                                                self.privileges_table_css), 'Privileges table is not visible')
        privileges_table_bool = privileges_table_elem.is_displayed()

        return privileges_table_bool

    def privileges_table_checkbox_column_bool(self):
        privileges_table_checkbox_column_elem = self.wait.until(EC.visibility_of_element_located(
                                self.privileges_table_checkbox_column_css), 'Column with checkboxes is not visible')
        privileges_table_checkbox_column_bool = privileges_table_checkbox_column_elem.is_displayed()

        return privileges_table_checkbox_column_bool

    def privileges_table_id_column_bool(self):
        privileges_table_id_column_elem = self.wait.until(EC.visibility_of_element_located(
                                                self.privileges_table_id_column_css), 'Column "ID" is not visible')
        privileges_id_column_bool = privileges_table_id_column_elem.is_displayed()

        privileges_table_id_column_menu_elem = self.wait.until(EC.visibility_of_element_located(
                                self.privileges_table_id_column_menu_css), 'Column "ID" arrow menu is not enabled')
        privileges_table_id_column_menu_bool = privileges_table_id_column_menu_elem.is_enabled()

        return privileges_id_column_bool and privileges_table_id_column_menu_bool

    def privileges_table_operation_name_column_bool(self):
        privileges_table_operation_name_column_elem = self.wait.until(EC.visibility_of_element_located(
                        self.privileges_table_operation_name_column_css), 'Column "Operation name" is not visible')
        privileges_table_operation_name_column_bool = privileges_table_operation_name_column_elem.is_displayed()

        privileges_table_operation_name_column_menu = self.wait.until(EC.visibility_of_element_located(
            self.privileges_table_operation_name_column_menu_css), 'Column "Operation name" arrow menu is not enabled')
        privileges_table_id_column_menu_bool = privileges_table_operation_name_column_menu.is_enabled()

        return privileges_table_operation_name_column_bool and privileges_table_id_column_menu_bool

    def privileges_table_operation_url_column_bool(self):
        privileges_table_operation_url_column_elem = self.wait.until(EC.visibility_of_element_located(
                        self.privileges_table_operation_url_column_css), 'Column "Operation URL" is not visible')
        privileges_table_operation_url_column_bool = privileges_table_operation_url_column_elem.is_displayed()

        privileges_table_operation_url_column_menu = self.wait.until(EC.visibility_of_element_located(
            self.privileges_table_operation_url_column_menu_css), 'Column "Operation URL" arrow menu is not enabled')
        privileges_table_operation_url_menu_bool = privileges_table_operation_url_column_menu.is_enabled()

        return privileges_table_operation_url_column_bool and privileges_table_operation_url_menu_bool

    def privileges_table_is_active_column_bool(self):
        privileges_table_is_active_column_elem = self.wait.until(EC.visibility_of_element_located(
                        self.privileges_table_is_active_column_css), 'Column "is Active" is not visible')
        privileges_table_is_active_column_bool = privileges_table_is_active_column_elem.is_displayed()

        privileges_table_is_active_column_menu = self.wait.until(EC.visibility_of_element_located(
                    self.privileges_table_is_active_column_arrow), 'Column "is Active" arrow menu is not enabled')
        privileges_table_is_active_menu_bool = privileges_table_is_active_column_menu.is_enabled()

        return privileges_table_is_active_column_bool and privileges_table_is_active_menu_bool

    def add_new_role_button_visible_bool(self):
        """Press 'Add Role' button and test that pop up window appears, if window appeared return True"""
        role_add_button = self.wait.until(EC.visibility_of_element_located(self.add_role_button_css),
                                          'Add Role button is not visible')

        return role_add_button.is_displayed()

    def webelement_of_id_column_in_roles_table(self):
        """Returns webelement of the ID column of the Role's (left) table"""
        role_id_menu_button = self.wait.until(EC.visibility_of_element_located(self.roles_table_first_column_css),
                                          'ID column on Roles table is not visible')

        if role_id_menu_button.is_displayed():
            return role_id_menu_button

    def webelement_of_id_column_in_privilege_table(self):
        """Returns webelement of the ID column of the Privileges (right) table"""
        role_id = self.wait.until(EC.visibility_of_element_located(self.privileges_table_second_column_css),
                                          'ID column in Privileges table is not visible')

        return role_id

    def webelement_of_name_column_in_roles_table(self):
        """Returns webelement of the Role name column of the Role's (left) table"""
        role_name_menu_button = self.wait.until(EC.visibility_of_element_located(self.roles_table_second_column_css),
                                          'Name column in Roles table is not visible')

        if role_name_menu_button.is_displayed():
            return role_name_menu_button

    def webelement_of_operation_name_column_in_privilege_table(self):
        """Returns webelement of the Operation name column of the Privileges (right) table"""
        operation_name = self.wait.until(EC.visibility_of_element_located(self.privileges_table_third_column_css),
                                          'Operation name column in Privileges table is not visible')

        return operation_name

    def webelement_of_isactive_column_in_roles_table(self):
        """Returns webelement of the isActive column of the Role's (left) table"""
        role_isactive_= self.wait.until(EC.visibility_of_element_located(
                            self.roles_table_third_column_css), 'IsActive column in Roles table is not visible')
        return role_isactive_

    def webelement_of_operation_url_column_in_privilege_table(self):
        """Returns webelement of the Operation Url column of the Privileges (right) table"""
        operation_url = self.wait.until(EC.visibility_of_element_located(self.privileges_table_fourth_column_css),
                                          'Operation Url column in Privileges table is not visible')
        return operation_url

    def webelement_of_operations_column_in_roles_table(self):
        """Returns webelement of the Operations column of the Role's (left) table"""
        role_operations_menu_button = self.wait.until(EC.visibility_of_element_located(
                            self.roles_table_fourth_column_css), 'Name column in Operations table is not visible')

        if role_operations_menu_button.is_displayed():
            return role_operations_menu_button

    def webelement_of_operation_is_active_column_in_privilege_table(self):
        """Returns webelement of the Is Active column of the Privileges (right) table"""
        is_active = self.wait.until(EC.visibility_of_element_located(self.privileges_table_fifth_column_css),
                                          'Is Active column in Privileges table is not visible')
        return is_active

    def names_of_all_columns_in_roles_table(self, column_names_from_table_headers):
        """Returns a list of the columns of the Role name table, according to their relative index in the DOM"""
        role_names_list = []

        role_name_inx_0 = self.wait.until(EC.visibility_of_element_located(self.roles_table_first_column_css),
                                                                        '1st column in Roles table is not visible')
        if role_name_inx_0.is_displayed():

            if role_name_inx_0.text.find("\n") < 0:
                splited_string = role_name_inx_0.text
            else:
                splited_string = (role_name_inx_0.text).split("\n", 1)[1]

            role_names_list.append(splited_string)

        role_name_inx_1 = self.wait.until(EC.visibility_of_element_located(self.roles_table_second_column_css),
                                                                        '2nd column in Roles table is not visible')
        if role_name_inx_1.is_displayed():

            if role_name_inx_1.text.find("\n") < 0:
                splited_string = role_name_inx_1.text
            else:
                splited_string = (role_name_inx_1.text).split("\n", 1)[1]

            role_names_list.append(splited_string)

        role_name_inx_2 = self.wait.until(EC.visibility_of_element_located(self.roles_table_third_column_css),
                                                                        '3rd column in Roles table is not visible')
        if role_name_inx_2.is_displayed():

            if role_name_inx_2.text.find("\n") < 0:
                splited_string = role_name_inx_2.text
            else:
                splited_string = (role_name_inx_2.text).split("\n", 1)[1]

            role_names_list.append(splited_string)

        role_name_inx_3 = self.wait.until(EC.visibility_of_element_located(self.roles_table_fourth_column_css),
                                                                        '4th column in Roles table is not visible')
        if role_name_inx_3.is_displayed():

            if role_name_inx_3.text.find("\n") < 0:
                splited_string = role_name_inx_3.text
            else:
                splited_string = (role_name_inx_3.text).split("\n", 1)[1]

            role_names_list.append(splited_string)

        default_column_state = True
        for idx, val in enumerate(column_names_from_table_headers):
            if role_names_list[idx] != column_names_from_table_headers[idx]:
                default_column_state = False

        return default_column_state

    def names_of_all_columns_in_privilege_table(self, column_names_from_table_headers):
        """Returns a list of the columns of the Privilege table, according to their relative index in the DOM"""
        priv_names_list = []
        ### Column 1
        role_name_inx_1 = self.wait.until(EC.visibility_of_element_located(self.privileges_table_first_column_css),
                                                                        '1st column in Privilege table is not visible')
        if role_name_inx_1.text.find("\n") < 0:
            splited_string = role_name_inx_1.text
        else:
            splited_string = (role_name_inx_1.text).split("\n", 1)[1]

        priv_names_list.append(splited_string)
        ### Column 2
        role_name_inx_2 = self.wait.until(EC.visibility_of_element_located(self.privileges_table_second_column_css),
                                                                        '2nd column in Privilege table is not visible')
        if role_name_inx_2.text.find("\n") < 0:
            splited_string = role_name_inx_2.text
        else:
            splited_string = (role_name_inx_2.text).split("\n", 1)[1]

        priv_names_list.append(splited_string)
        ### Column 3
        role_name_inx_3 = self.wait.until(EC.visibility_of_element_located(self.privileges_table_third_column_css),
                                                                        '3rd column in Privilege table is not visible')
        if role_name_inx_3.text.find("\n") < 0:
            splited_string = role_name_inx_3.text
        else:
            splited_string = (role_name_inx_3.text).split("\n", 1)[1]

        priv_names_list.append(splited_string)
        ### Column 4
        role_name_inx_4 = self.wait.until(EC.visibility_of_element_located(self.privileges_table_fourth_column_css),
                                                                        '4th column in Privilege table is not visible')
        if role_name_inx_4.text.find("\n") < 0:
            splited_string = role_name_inx_4.text
        else:
            splited_string = (role_name_inx_4.text).split("\n", 1)[1]

        priv_names_list.append(splited_string)
        ### Column 5
        role_name_inx_5 = self.wait.until(EC.visibility_of_element_located(self.privileges_table_fifth_column_css),
                                                                        '5th column in Privilege table is not visible')
        if role_name_inx_5.text.find("\n") < 0:
            splited_string = role_name_inx_5.text
        else:
            splited_string = (role_name_inx_5.text).split("\n", 1)[1]

        priv_names_list.append(splited_string)

        default_column_state = True
        for idx, val in enumerate(column_names_from_table_headers):
            if priv_names_list[idx] != column_names_from_table_headers[idx]:
                default_column_state = False

        return default_column_state

    def name_of_1st_column_in_roles_table(self):
        """Returns column name of the 1st column in the Role name table"""
        role_name_webelement = self.wait.until(EC.visibility_of_element_located(self.roles_table_first_column_css),
                                                                        '1st column in Roles table is not visible')
        if role_name_webelement.is_displayed():
            if role_name_webelement.text.find("\n") < 0:
                splited_string = role_name_webelement.text
            else:
                splited_string = (role_name_webelement.text).split("\n", 1)[1]

        return splited_string

    def name_of_2nd_column_in_roles_table(self):
        """Returns column name of the 2nd column in the Role name table"""
        role_name_webelement = self.wait.until(EC.visibility_of_element_located(self.roles_table_second_column_css),
                                                                        '2nd column in Roles table is not visible')
        if role_name_webelement.is_displayed():
            if role_name_webelement.text.find("\n") < 0:
                splited_string = role_name_webelement.text
            else:
                splited_string = (role_name_webelement.text).split("\n", 1)[1]

        return splited_string

    def name_of_3rd_column_in_roles_table(self):
        """Returns column name of the 3rd column in the Role name table"""
        role_name_webelement = self.wait.until(EC.visibility_of_element_located(self.roles_table_third_column_css),
                                                                        '3rd column in Roles table is not visible')
        if role_name_webelement.is_displayed():
            if role_name_webelement.text.find("\n") < 0:
                splited_string = role_name_webelement.text
            else:
                splited_string = (role_name_webelement.text).split("\n", 1)[1]

        return splited_string

    def name_of_4th_column_in_roles_table(self):
        """Returns column name of the 4th column in the Role name table"""
        role_name_webelement = self.wait.until(EC.visibility_of_element_located(self.roles_table_fourth_column_css),
                                                                        '4th column in Roles table is not visible')
        if role_name_webelement.is_displayed():
            if role_name_webelement.text.find("\n") < 0:
                splited_string = role_name_webelement.text
            else:
                splited_string = (role_name_webelement.text).split("\n", 1)[1]

        return splited_string

    def webelement_of_1st_column_in_roles_table(self):
        """Returns webelement of the 1st column in the Role name table"""
        role_name_webelement = self.wait.until(EC.visibility_of_element_located(self.roles_table_first_column_css),
                                                                        '1st column in Roles table is not visible')
        if role_name_webelement.is_displayed():
            return role_name_webelement

    def webelement_of_1st_column_in_privilege_table(self):
        """Returns webelement of the 1st column in the Privilege table"""
        priv_column_webelement = self.wait.until(EC.visibility_of_element_located(self.privileges_table_first_column_css),
                                                                        '1st column in Roles table is not visible')
        return priv_column_webelement

    def webelement_of_2nd_column_in_privilege_table(self):
        """Returns webelement of the 2nd column in the Privilege table"""
        priv_column_webelement = self.wait.until(EC.visibility_of_element_located(self.privileges_table_second_column_css),
                                                                        '2nd column in Privilege table is not visible')
        return priv_column_webelement

    def webelement_of_2nd_column_in_roles_table(self):
        """Returns webelementof the 2nd column in the Role name table"""
        role_name_webelement = self.wait.until(EC.visibility_of_element_located(self.roles_table_second_column_css),
                                                                        '2nd column in Roles table is not visible')
        if role_name_webelement.is_displayed():
            return role_name_webelement

    def webelement_of_3rd_column_in_roles_table(self):
        """Returns webelement of the 3rd column in the Role name table"""
        role_name_webelement = self.wait.until(EC.visibility_of_element_located(self.roles_table_third_column_css),
                                                                        '3rd column in Roles table is not visible')
        if role_name_webelement.is_displayed():
            return role_name_webelement

    def webelement_of_3rd_column_in_privilege_table(self):
        """Returns webelement of the 3rd column in the Privilege table"""
        priv_column_webelement = self.wait.until(EC.visibility_of_element_located(self.privileges_table_third_column_css),
                                                                        '3rd column in Privilege table is not visible')
        return priv_column_webelement

    def webelement_of_4th_column_in_roles_table(self):
        """Returns webelement of the 4th column in the Role name table"""
        role_name_webelement = self.wait.until(EC.visibility_of_element_located(self.roles_table_fourth_column_css),
                                                                        '4th column in Roles table is not visible')
        if role_name_webelement.is_displayed():
            return role_name_webelement

    def webelement_of_4th_column_in_privilege_table(self):
        """Returns webelement of the 4th column in the Privilege name table"""
        priv_column_webelement = self.wait.until(EC.visibility_of_element_located(self.privileges_table_fourth_column_css),
                                                                        '4th column in Privileges table is not visible')
        return priv_column_webelement

    def webelement_of_5th_column_in_privilege_table(self):
        """Returns webelement of the 5th column in the Privilege name table"""
        priv_column_webelement = self.wait.until(EC.visibility_of_element_located(self.privileges_table_fifth_column_css),
                                                                        '5th column in Privileges table is not visible')
        return priv_column_webelement

    def user_page_elements_test(self):
        """Verify basic Webelements of the user page window"""
        return \
            self.role_title() and self.add_role_button_bool() and self.roles_table_bool() and self.roles_table_id_column_bool() and \
            self.roles_table_role_name_column_bool() and self.roles_table_isActive_column_bool() and \
            self.roles_table_operations_column_bool() and self.save_changes_button_bool() and self.privileges_table_bool() and \
            self.privileges_table_checkbox_column_bool() and self.privileges_table_id_column_bool() and \
            self.privileges_table_operation_name_column_bool() and self.privileges_table_operation_url_column_bool() and \
            self.privileges_table_is_active_column_bool() and self.add_new_role_button_visible_bool()

    def verify_new_role_grid_vs_db(self, role_name):
        """Extract role's parameters from web grid and from DB and compare them"""
        # Check if the input was string
        if not isinstance(role_name, str):
            role_name = str(role_name)

        # Instantiate User Role page
        roles_page_instance = UserRolesPage(self.driver)
        # get the webelement of the Role page without headers
        roles_table_web = roles_page_instance.get_the_table_element_roles_without_headers()
        # initialize the Table class instance
        role_table_instance = Table(self.driver, roles_table_web)

        # Connect to DB
        data_base = DataBase(utilities.DataBase.get_connection_parameters())
        if role_name.find("'"):
            data_base_var_without_apostrophe = utilities.DataBase.escape_apostrophes_for_sql_query(role_name)

        # save result of the query to the dictionary, 1 row in dictionary correspond to 1 row in DB;
        # one row in dictionary contains tuple of different datatypes which correspond to cell values in DB
        db_res = data_base.select("DECLARE @SQL NVARCHAR(255);"
                        "SET @SQL = 'SELECT * FROM [PromoToolGlobus].[PromoTool].[Roles] WHERE RoleName = @Field1';"
                        "EXECUTE sp_executesql @SQL, N'@Field1 VARCHAR(255)', '"+data_base_var_without_apostrophe+"'")
        # Save data from DB in the corresponding variables
        if len(db_res) > 0 and len(db_res[0]) > 0:
            id_db = db_res[0][0]
            role_name_db = db_res[0][1]
            is_active_db = db_res[0][2]
        elif len(db_res) <= 0:
            return False

        # id number of role from DB coverted to string
        id_db = str(id_db)
        # isactive value of role from DB coverted to string
        is_active_db = (str(is_active_db)).lower()

        # get the list of webelements corresponding to the values from the found row
        row_web_elements = role_table_instance.get_row_by_id(id_db)
        webelement_len = len(row_web_elements)
        # 4 columns in Roles table : ID, Role name, IsActive, Operations
        if webelement_len > 0:
            id_web = str(row_web_elements[0].text)
            role_name_web = str(row_web_elements[1].get_attribute("textContent"))
            is_active_web = (str(row_web_elements[2].text)).lower()

        # compare values of RoleId, RoleName and isActive status with the corresponding values extracted from DB
        if id_db == id_web and role_name_db == role_name_web and is_active_db == is_active_web:
                return True
        return False

    def verify_role_parameters(self, role_name):
        roles_page_instance = UserRolesPage(self.driver)
        # get the webelement of the Role page without headers
        roles_table_web = roles_page_instance.get_the_table_element_roles_without_headers()
        # initialize the Table class instance
        role_table_instance = Table(self.driver, roles_table_web)

        all_rows = role_table_instance.get_all_cells_element()
        id_list = []
        for row in all_rows:
            id_list.append(int(row[0].get_attribute("textContent")))

        id_list.sort()
        id = id_list[-1]
        row_webelement = role_table_instance.get_row_by_id(id)
        role_name_from_grid = row_webelement[1].get_attribute("textContent")

        if role_name == role_name_from_grid:
            return True
        return False

    def remove_role_by_name(self, role_name):
        """Find new role by its name and then remove it"""
        # Check if the input was string
        if not isinstance(role_name, str):
            role_name = str(role_name)

        # Instantiate User Role page
        roles_page_instance = UserRolesPage(self.driver)
        # get the webelement of the Role page without headers
        roles_table_web = roles_page_instance.get_the_table_element_roles_without_headers()
        # initialize the Table class instance
        role_table_instance = Table(self.driver, roles_table_web)

        # Connect to DB
        data_base = DataBase(utilities.DataBase.get_connection_parameters())
        if role_name.find("'"):
            data_base_var_without_apostrophe = utilities.DataBase.escape_apostrophes_for_sql_query(role_name)

        # save result of the query to the dictionary, 1 row in dictionary correspond to 1 row in DB;
        # one row in dictionary contains tuple of different datatypes which correspond to cell values in DB
        db_res = data_base.select("DECLARE @SQL NVARCHAR(255);"
                        "SET @SQL = 'SELECT * FROM [PromoToolGlobus].[PromoTool].[Roles] WHERE RoleName = @Field1';"
                        "EXECUTE sp_executesql @SQL, N'@Field1 VARCHAR(255)', '"+data_base_var_without_apostrophe+"'")
        # Save data from DB in the corresponding variables
        if len(db_res) > 0 and len(db_res[0]) > 0:
            id_db = db_res[0][0]
            role_name_db = db_res[0][1]
            is_active_db = db_res[0][2]
        elif len(db_res) <= 0:
            return

        # id number of role from DB coverted to string
        id_db = str(id_db)

        # get the list of webelements corresponding to the values from the found row
        row_web_elements = role_table_instance.get_row_by_id(id_db)
        webelement_len = len(row_web_elements)
        # 4 columns in Roles table : ID, Role name, IsActive, Operations
        if webelement_len > 0:
            buttons_web_element = row_web_elements[3]
        else:
            return

        # get the webelement of 2 buttons
        buttons_web_elements = buttons_web_element.find_elements_by_tag_name('a')

        # get the webelement of Delete button, and verify validity common webelement
        if len(buttons_web_elements) >= 2:
            delete_button_element = buttons_web_elements[1]
        else:
            return

        # Click on the "Delete" button
        if delete_button_element.is_enabled():
            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", delete_button_element)
            else:
                delete_button_element.click()
        else:
            return

    def edit_role_by_id(self, role_id):
        # Instantiate User Role page
        roles_page_instance = UserRolesPage(self.driver)
        # get the webelement of the Role page without headers
        roles_table_web = roles_page_instance.get_the_table_element_roles_without_headers()
        # initialize the Table class instance
        role_table_instance = Table(self.driver, roles_table_web)

        # get the list of webelements corresponding to the values from the found row
        row_web_elements = role_table_instance.get_row_by_id(role_id)
        webelement_len = len(row_web_elements)
        # 4 columns in Roles table : ID, Role name, IsActive, Operations
        if webelement_len > 0:
            buttons_web_element = row_web_elements[3]
        else:
            return

        # get the webelement of 2 buttons
        buttons_web_elements = buttons_web_element.find_elements_by_tag_name('a')

        # get the webelement of Delete button, and verify validity common webelement
        if len(buttons_web_elements) >= 2:
            eidt_button_element = buttons_web_elements[0]
        else:
            return

        # Click on the "Edit" button
        if eidt_button_element.is_enabled():
            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", eidt_button_element)
            else:
                eidt_button_element.click()
        else:
            return

    def verify_role_was_deleted_from_grid_and_db(self, role_name):
        """Extract role's parameters from web grid and from DB and compare them"""
        db_removed = False
        grid_removed = False
        # Check if the input was string
        if not isinstance(role_name, str):
            role_name = str(role_name)
        # Connect to DB
        data_base = DataBase(utilities.DataBase.get_connection_parameters())
        if role_name.find("'"):
            data_base_var_without_apostrophe = utilities.DataBase.escape_apostrophes_for_sql_query(role_name)

        # save result of the query to the dictionary, 1 row in dictionary correspond to 1 row in DB;
        # one row in dictionary contains tuple of different datatypes which correspond to cell values in DB
        db_res = data_base.select("DECLARE @SQL NVARCHAR(255);"
                        "SET @SQL = 'SELECT * FROM [PromoToolGlobus].[PromoTool].[Roles] WHERE RoleName = @Field1';"
                        "EXECUTE sp_executesql @SQL, N'@Field1 VARCHAR(100)', '"+data_base_var_without_apostrophe+"'")
        # Save data from DB in the corresponding variables
        if len(db_res) == 0:
             db_removed = True

        # Take the Role name which is the input parameter and create XPATH with its name
        full_xpath_name = XpathFindText.xpath_of_text(role_name)

        # create XPATH object for the Role's name from input parameter
        name_for_comparison = (By.XPATH, full_xpath_name)

        # locate the Role's row location by its name, normally the Webelement should not be found, so the Timeout
        # exception will be thrown by the wait , we catch it and retrun True if the element was not found
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(name_for_comparison),
                                                            "Role with the name " + role_name + " was not found")
        except TimeoutException:
            grid_removed = True

        # if the role name was not found in the DB and in the Webgrid then return True
        if db_removed and grid_removed:
                return True
        return False

    def click_on_the_role(self, role_name):
        """Click/highlight the Role by its name"""
        # Check if the input was string
        if not isinstance(role_name, str):
            role_name = str(role_name)

        # Take the Role name which is the input parameter and create XPATH with its name
        row_to_remove = XpathFindText.xpath_of_text(role_name)

        # get the location of  XPATH object for the Role's name from input parameter
        role_to_remove_loc = (By.XPATH, row_to_remove)

        # get the webelement of the role based on XPATH locator
        row_with_role_name = self.wait.until(EC.visibility_of_element_located(role_to_remove_loc),
                                             "Row with the role name '" + role_name + "' is not visible")

        if row_with_role_name.is_enabled():
            if Parser().get_browser_name() is 'IE':
                self.driver.execute_script("arguments[0].click();", row_with_role_name)
            else:
                row_with_role_name.click()

        return row_with_role_name

    def get_the_role_id_from_db(self, role_name):
        """Return the role's ID by its name"""
        # Check if the input was string
        if not isinstance(role_name, str):
            role_name = str(role_name)

        # Connect to DB
        data_base = DataBase(utilities.DataBase.get_connection_parameters())
        if role_name.find("'"):
            data_base_var_without_apostrophe = utilities.DataBase.escape_apostrophes_for_sql_query(role_name)

        # save result of the query to the dictionary, 1 row in dictionary correspond to 1 row in DB;
        # one row in dictionary contains tuple of different datatypes which correspond to cell values in DB
        db_res = data_base.select("DECLARE @SQL NVARCHAR(255);"
                        "SET @SQL = 'SELECT * FROM [PromoToolGlobus].[PromoTool].[Roles] WHERE RoleName = @Field1';"
                        "EXECUTE sp_executesql @SQL, N'@Field1 VARCHAR(255)', '"+data_base_var_without_apostrophe+"'")
        # Save data from DB in the corresponding variables
        if len(db_res) > 0 and len(db_res[0]) > 0:
            id_db = db_res[0][0]
        elif len(db_res) <= 0:
            return "error reading DB"

        # id number of role from DB coverted to string
        id_db = str(id_db)

        return id_db

    def get_the_role_is_active_from_db(self, role_name):
        """Return the role's IsActive by its name"""
        # Check if the input was string
        if not isinstance(role_name, str):
            role_name = str(role_name)

        # Connect to DB
        data_base = DataBase(utilities.DataBase.get_connection_parameters())
        if role_name.find("'"):
            data_base_var_without_apostrophe = utilities.DataBase.escape_apostrophes_for_sql_query(role_name)

        # save result of the query to the dictionary, 1 row in dictionary correspond to 1 row in DB;
        # one row in dictionary contains tuple of different datatypes which correspond to cell values in DB
        db_res = data_base.select("DECLARE @SQL NVARCHAR(255);"
                        "SET @SQL = 'SELECT * FROM [PromoToolGlobus].[PromoTool].[Roles] WHERE RoleName = @Field1';"
                        "EXECUTE sp_executesql @SQL, N'@Field1 VARCHAR(255)', '"+data_base_var_without_apostrophe+"'")
        # Save data from DB in the corresponding variables
        if len(db_res) > 0 and len(db_res[0]) > 0:
            id_db = db_res[0][0]
            is_active_db = db_res[0][2]
        elif len(db_res) <= 0:
            return "error reading DB"

        # id number of role from DB coverted to string
        is_active = str(is_active_db)

        return is_active

    def role_found_by_name(self, role_name):
        """If role found by name return True"""
        # Check if the input was string
        if not isinstance(role_name, str):
            role_name = str(role_name)

        # Take the Role name which is the input parameter and create XPATH with its name
        row_location = XpathFindText.xpath_of_text(role_name)

        # get the location of  XPATH object for the Role's name from input parameter
        role_webelement_location = (By.XPATH, row_location)

        # get the webelement of the role based on XPATH locator
        try:
            WebDriverWait(self.driver, 0.5).until(EC.visibility_of_element_located(role_webelement_location),
                                                    "Row with the role name '" + role_name + "' is not visible")
        except TimeoutException:
            return False

        return True

    def get_the_table_element_roles_without_headers(self):
        """Return the table's webelement without headers and other elements, in our case Role's table"""
        table_webelement_roles = self.wait.until(EC.visibility_of_element_located(self.roles_table_element_locator))
        return table_webelement_roles

    def get_the_table_element_privileges_without_headers(self):
        """Return the table's webelement without headers and other elements, in our case Privileges' table"""
        table_webelement_roles = self.wait.until(EC.visibility_of_element_located(self.privileges_table_element_locator))
        return table_webelement_roles

    def get_the_table_element_roles_full(self):
        """Return the table's webelement, in our case Role's table"""
        table_webelement_roles = self.wait.until(EC.visibility_of_element_located(self.roles_table_left_css))
        return table_webelement_roles

    def get_the_table_element_privileges_full(self):
        """Return the table's webelement, in our case Privileges table"""
        table_webelement_privileges = self.wait.until(EC.visibility_of_element_located(self.privileges_table_css))
        return table_webelement_privileges

    def click_on_the_privilege_and_save_one_by_one(self):
        """Click/check each privilege on the Role page after each checking press Save button"""
        # Instantiate User Role page
        roles_page_instance = UserRolesPage(self.driver)
        # get the webelement of the Privilege table without headers
        privileges_table_web = roles_page_instance.get_the_table_element_privileges_without_headers()
        # initialize the Table class instance
        privileges_table_instance = Table(self.driver, privileges_table_web)

        # check if Privileges (right) table is loaded
        privileges_table_instance.wait_table_to_load()
        # get the size of privilege table
        priv_table_size = privileges_table_instance.count_rows()

        i = 1 # checkbox serial number
        while i < priv_table_size:

            loc_of_nth_privilege_checkbox = (By.XPATH, "(//div[@class='k-grid-content k-auto-scrollable']/*)[2]//tr["+str(i)+"]//td[1]")

            try:
                webelement_of_nth_checkbox = WebDriverWait(privileges_table_web, 30).until(EC.visibility_of_element_located(
                                        loc_of_nth_privilege_checkbox), "Checkbox "+str(i)+" is not clickable")

                self.driver.execute_script("return arguments[0].scrollIntoView(true);", webelement_of_nth_checkbox)

                if Parser().get_browser_name() is 'IE':
                    self.driver.execute_script("arguments[0].click();", webelement_of_nth_checkbox)
                else:
                    webelement_of_nth_checkbox.click()
            except:
                continue

            try:
                webelement_of_save_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                                            self.save_changes_button_locator), "Save changes button is not visible")

                save_button_attribute = webelement_of_save_button.get_attribute("class")

                if "success" not in save_button_attribute:
                    continue

                if Parser().get_browser_name() is 'IE':
                    self.driver.execute_script("arguments[0].click();", webelement_of_save_button)
                else:
                    webelement_of_save_button.click()
            except:
                continue

            i = i + 1

        return self

    def click_on_the_privilege_and_save_one_time(self):
        """Click/check each privilege on the Role page with pressing Save button at the end"""
        # Instantiate User Role page
        roles_page_instance = UserRolesPage(self.driver)
        # get the webelement of the Privilege table without headers
        privileges_table_web = roles_page_instance.get_the_table_element_privileges_without_headers()
        # initialize the Table class instance
        privileges_table_instance = Table(self.driver, privileges_table_web)

        # check if Privileges (right) table is loaded
        privileges_table_instance.wait_table_to_load()
        # get the size of privilege table
        priv_table_size = privileges_table_instance.count_rows()

        i = 1 # checkbox serial number
        while i < priv_table_size:

            loc_of_nth_privilege_checkbox = (By.XPATH, "(//div[@class='k-grid-content k-auto-scrollable']/*)[2]//tr["+str(i)+"]//td[1]")

            try:
                webelement_of_nth_checkbox = WebDriverWait(privileges_table_web, 30).until(EC.visibility_of_element_located(
                                        loc_of_nth_privilege_checkbox), "Checkbox "+str(i)+" is not clickable")

                self.driver.execute_script("return arguments[0].scrollIntoView(true);", webelement_of_nth_checkbox)

                if Parser().get_browser_name() is 'IE':
                    self.driver.execute_script("arguments[0].click();", webelement_of_nth_checkbox)
                else:
                    webelement_of_nth_checkbox.click()
            except:
                continue

            i = i + 1


        webelement_of_save_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                                    self.save_changes_button_locator), "Save changes button is not visible")

        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", webelement_of_save_button)
        else:
            webelement_of_save_button.click()

        return self

    def click_on_the_privilege_by_ids(self, privelege_ids):
        """Click/check particular privilege in the Role page by its ID"""
        # Instantiate User Role page
        roles_page_instance = UserRolesPage(self.driver)
        # get the webelement of the Privilege table without headers
        privileges_table_web = roles_page_instance.get_the_table_element_privileges_without_headers()
        # initialize the Table class instance
        privileges_table_instance = Table(self.driver, privileges_table_web)

        # check if Privileges (right) table is loaded
        privileges_table_instance.wait_table_to_load()

        for id_inx in privelege_ids:
            try:
                webelement_of_row_with_id = privileges_table_instance.get_row_by_id(id_inx, 1)

                self.driver.execute_script("return arguments[0].scrollIntoView(true);", webelement_of_row_with_id[0])

                if Parser().get_browser_name() is 'IE':
                    self.driver.execute_script("arguments[0].click();", webelement_of_row_with_id[0])
                else:
                    webelement_of_row_with_id[0].click()
            except:
                return
        return

    def verify_privilege_checkboxes_state(self, privelege_ids):
        """Click/check particular privilege in the Role page by its ID"""
        # Instantiate User Role page
        roles_page_instance = UserRolesPage(self.driver)
        # get the webelement of the Privilege table without headers
        privileges_table_web = roles_page_instance.get_the_table_element_privileges_without_headers()
        # initialize the Table class instance
        privileges_table_instance = Table(self.driver, privileges_table_web)

        # check if Privileges (right) table is loaded
        # privileges_table_instance.wait_table_to_load()

        bool_res_list = []

        for id_inx in privelege_ids:
            try:
                webelement_of_row_with_id = privileges_table_instance.get_row_by_id(id_inx, 1)

                self.driver.execute_script("return arguments[0].scrollIntoView(true);", webelement_of_row_with_id[0])

                webelement_of_checkbox = webelement_of_row_with_id[0].find_elements_by_tag_name("input")

                checkbox_attr_value = webelement_of_checkbox[0].get_attribute('checked')

                if checkbox_attr_value:
                    bool_res_list.append(True)
                else:
                    bool_res_list.append(False)
            except:
                return

        return bool_res_list