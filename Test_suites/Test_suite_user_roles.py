import time
import unittest

from BaseTest import BaseTest
from utilities.Parser import Parser

from Pages.user_roles_page.RemoveRoleDialog import RemoveRoleDialog
from Pages.user_roles_page.UserRolesPage import UserRolesPage

from Pages.user_roles_page.UnsavedDataDialog import UnsavedDataDialog
from Pages.user_roles_page.AddRolePopUp import AddRolePopUp
from utilities.KendoSortingChecker import KendoSorting

from utilities.Table import Table
from utilities.Table import TableFilter
from utilities.PromoRequest import PromoRequest

from Pages.users_page.UsersPage import UsersPage
from Pages.home_page.HomePage import HomePage

class UserRolesTest(BaseTest):
    """Add roles and privileges to user, delete roles, sort, and filter columns, attach roles to users."""

    role_name_empty = "  "
    role_name_special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    role_name_with_all_priv = "uP}p,'qe6NKH=Y.%F&6uS}hp[X}[6;[bq),SrB6cPs8tJt_vcXL^d"
    role_name_very_long = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget " \
                          "dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, " \
                          "nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium !@#:"
    role_name_cancel = "jUHQb-j'-:pP,6f*"
    role_name_yes = "MAS&U<f>89VKS2/V5s)eG9z2"
    double_role_name = "z\"%QE^+GPNPftA^3jtL&e*YshMd4hq5&#EfanwM}m3Q&bzd]bxXwCD"
    role_name_too_long = "{kU\"]$~p,/pH5v%D:9\" < M @ fc3\)}-\"5B-Du&g[jJ?;\;Yj:?uSzx#S(6mC(Zm:TFpv[M$<@v#!Vf8\\3+" \
                         "Abm*-#Pcus*}S:r;]ZA%;-_>\"kPbdsDvDy`r2uN\^WqWQ5jYycL(4`ruh*g$z829LG~=\:EUkk?g>&T!yb\Z6En" \
                         "T$J`$tJA*Bz}??5Rap~N#)$Xy+_\\2YZE7&8%ard'g\\nQ4hm5~6z}s{p$h{C}8Xk/>A4[T$Xv2_!WDpfEh}=.aGeqW3"
    role3 = "}=qt[e7x+b6;?/@a9P]dn9BU$5(kX}Z9"
    role2 = "aBYwbb:E;(XjV3,>d[Q8-d_=2Ehs"
    role1 = "ABcYwbb:E;(XjV3,>d[Q8-d_=2Ehs\""
    role4 = "x2~x*RRr{M9SRC~"
    role5 = "-UM@myKt8B&pMT97MV#T"
    role6 = "9z4XzxtyPGwn"
    role7 = "  k3SVt5deXMzxQkLK5B7b"
    all_roles_name = [role_name_special_characters, role_name_with_all_priv,role_name_very_long,role_name_cancel,
                      role_name_yes,double_role_name,role_name_too_long,role3,role2,role1,role4,role5,role6,role7]

    user_id = ""
    login = "login_test"
    email = "globuspromotool3@gmail.com"
    auth_type = "0"
    domain = ""
    is_active = "true"
    user_name = "Test user"

    def setUp(self):
        """set up before test case: open the webpage and load cache and login with the "For Auto Test" user, czech language"""
        super().setUp()
        self.driver.get(self.base_url + '404')
        PromoRequest(self.driver).authorization_by_request(login=self.autotest_user['login'],
                                                           password=self.autotest_user['password'], language='cs')
        self.driver.get(self.base_url +'admin/roles')

    def tearDown(self):
        """Remove added roles if the test fails, in order to add it again in the next run"""
        roles_menu = UserRolesPage(self.driver)

        for role_name in self.all_roles_name:
            if roles_menu.role_found_by_name(role_name):
                role_id_grid = roles_menu.get_the_role_id_from_db(role_name)
                role_isactive_grid = roles_menu.get_the_role_is_active_from_db(role_name)

                # if there is no such entry in the DB , meaning role was not added, then no need to send POST request for deletion to the server
                if role_id_grid == "error reading DB" or role_isactive_grid == "error reading DB":
                    pass
                elif len(role_id_grid) > 0 and len(role_isactive_grid) > 0:
                    PromoRequest(self.driver).delete_role_request(role_id_grid, role_isactive_grid, role_name)
        self.driver.close()

    # ============ Adding roles =============== #
    def test_add_roles_page_elements(self):
        """Verify active elements, menus, titles, buttons, column names on the roles page"""

        # Clean grid if any roles left from previous steps
        roles_menu = UserRolesPage(self.driver)

        for role_name in self.all_roles_name:
            if roles_menu.role_found_by_name(role_name):
                role_id_grid = roles_menu.get_the_role_id_from_db(role_name)
                role_isactive_grid = roles_menu.get_the_role_is_active_from_db(role_name)

                # if there is no such entry in the DB , meaning role was not added, then no need to send POST request for deletion to the server
                if role_id_grid == "error reading DB" or role_isactive_grid == "error reading DB":
                    None
                elif len(role_id_grid) > 0 and len(role_isactive_grid) > 0:
                    PromoRequest(self.driver).delete_role_request(role_id_grid, role_isactive_grid, role_name)

        self.assertTrue(roles_menu.role_title(), "Role page title is not visible")
        self.assertTrue(roles_menu.add_role_button_bool(), "Add role button is not visible")
        self.assertTrue(roles_menu.roles_table_bool(), "Role's table is not visible")
        self.assertTrue(roles_menu.roles_table_id_column_bool(), "Role ID column is not visible")
        self.assertTrue(roles_menu.roles_table_role_name_column_bool(), "Role name column is not visible")
        self.assertTrue(roles_menu.roles_table_isActive_column_bool(), "isActive column is not visible")
        self.assertTrue(roles_menu.roles_table_operations_column_bool(), "Operations column is not visible")
        self.assertTrue(roles_menu.save_changes_button_bool(), "Save changes button is not visible")
        self.assertTrue(roles_menu.privileges_table_bool(), "Privilege's table is not visible")
        self.assertTrue(roles_menu.privileges_table_checkbox_column_bool(), "Checkboxes column is not visible")
        self.assertTrue(roles_menu.privileges_table_id_column_bool(), "Privileges ID column is not visible")
        self.assertTrue(roles_menu.privileges_table_operation_name_column_bool(), "Operation name column is not visible")
        self.assertTrue(roles_menu.privileges_table_operation_url_column_bool(), "Operation URL column is not visible")
        self.assertTrue(roles_menu.privileges_table_is_active_column_bool(), "isActive column is not visible")
        self.assertTrue(roles_menu.add_new_role_button_visible_bool(), "Add new role button is not visible")

    def test_adding_role_with_very_long_name(self):
        """Add role with very_long_name , with maximum length 254 characters"""
        # Instantiate Add Role popup window
        add_roles_pop_up = AddRolePopUp(self.driver)

        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Press add role button
        self.assertTrue(add_roles_pop_up.press_add_new_role_pop_up_window(), "Add Role button is not available")

        # Add role with a lot of special characters
        add_roles_pop_up.add_new_role_active(self.role_name_very_long)
        time.sleep(0.5)
        # # Verify that the new role appears in the DB and in the grid, and that the roles' parameters match
        # self.assertTrue(roles_menu.verify_new_role_grid_vs_db(self.role_name_very_long),
        #                                                         "The grid data doesn't correpond to the DB data")

        role_name_comparison_result = roles_menu.verify_role_parameters(self.role_name_very_long)

        # Click with the mouse on the Roles row in the Roles table
        roles_menu.click_on_the_role(self.role_name_very_long)

        # test compare role name from the grid and from the GUI dialog
        self.assertTrue(role_name_comparison_result, "The name of the new role is wrong")

        # test visibility of all web elements on Roles page , after the dialog window was closed
        self.assertTrue(roles_menu.user_page_elements_test(), "Some elements of Role page are not visible")

    def test_adding_role_with_special_characters(self):
        """Add all set of special characters based on python's function set(punctuation)"""
        # role_name_special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

        # Instantiate Add Role popup window
        add_roles_pop_up = AddRolePopUp(self.driver)

        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Press add role button
        self.assertTrue(add_roles_pop_up.press_add_new_role_pop_up_window(), "Add Role button is not available")

        # Add role with a lot of special characters
        add_roles_pop_up.add_new_role_active(self.role_name_special_characters)

        # # Verify that the new role appears in the DB and in the grid, and that the roles' parameters match
        # self.assertTrue(roles_menu.verify_new_role_grid_vs_db(self.role_name_special_characters),
        #                                                         "The grid data doesn't correpond to the DB data")
        time.sleep(0.5)
        role_name_comparison_result = roles_menu.verify_role_parameters(self.role_name_special_characters)
        # test compare role name from the grid and from the GUI dialog
        self.assertTrue(role_name_comparison_result, "The name of the new role is wrong")
        # Click with the mouse on the Roles row in the Roles table
        roles_menu.click_on_the_role(self.role_name_special_characters)

        # test visibility of all web elements on Roles page , after the dialog window was closed
        self.assertTrue(roles_menu.user_page_elements_test(), "Some elements of Role page are not visible")

    def test_adding_role_with_empty_name(self):
        """Add role with 3 spaces name"""
        # Instantiate Add Role popup window
        add_roles_pop_up = AddRolePopUp(self.driver)

        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Press add role button
        self.assertTrue(add_roles_pop_up.press_add_new_role_pop_up_window(), "Add Role button is not available")

        # Add role with 3 spaces
        self.assertEqual(add_roles_pop_up.add_new_role_and_read_error_message(self.role_name_empty),
                                                                                            'errorRole name is empty')

        # Verify that the new role appears in the DB and in the grid, and that the roles' parameters match
        roles_menu.verify_role_was_deleted_from_grid_and_db(self.role_name_empty)

        # test visibility of all web elements on Roles page , after the dialog window was closed
        self.assertTrue(roles_menu.user_page_elements_test(), "Some elements of Role page are not visible")

    def test_adding_roles_with_the_same_name(self):
        """Add 2 roles with the same name twice one-by-one"""
        # Instantiate Add Role popup window
        add_roles_pop_up = AddRolePopUp(self.driver)

        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Press add role button
        self.assertTrue(add_roles_pop_up.press_add_new_role_pop_up_window(), "Add Role button is not available")

        # Add new role 1st time
        add_roles_pop_up.add_new_role_active(self.double_role_name)

        # # Verify that the new role appears in the DB and in the grid, and that the roles' parameters match
        # self.assertTrue(roles_menu.verify_new_role_grid_vs_db(self.double_role_name),
        #                                                             "The grid data doesn't correpond to the DB data")

        # Click with the mouse on the Roles row in the Roles table
        # roles_menu.click_on_the_role(self.double_role_name)
        time.sleep(0.5)
        # Press add role button
        self.assertTrue(add_roles_pop_up.press_add_new_role_pop_up_window(), "Add Role button is not available")
        #
        # add_roles_pop_up.add_new_role_active(self.double_role_name)

        # Add new role 2nd time
        self.assertEqual(add_roles_pop_up.add_new_role_and_read_error_message(self.double_role_name),
                         "errorNo message for code=RoleNameAlreadyExists")

        add_roles_pop_up.press_cancel_new_role_pop_up_window()

        # test visibility of all web elements on Roles page , after the dialog window was closed
        self.assertTrue(roles_menu.user_page_elements_test(), "Some elements of Role page are not visible")

    @unittest.expectedFailure
    def test_adding_role_with_long_name_exceeding_limit(self):
        """Add role with the name exceeding allowed length 254 characters"""
        # Instantiate Add Role popup window
        add_roles_pop_up = AddRolePopUp(self.driver)

        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Press add role button
        self.assertTrue(add_roles_pop_up.press_add_new_role_pop_up_window(), "Add Role button is not available")

        # Check the error message, at this moment the proper error message is not known and the error message below
        # was created based on the error message from the empty name.
        # In this particular test case we have a bug with wrong error message, this assert will produce error.

        self.assertEqual(add_roles_pop_up.add_new_role_and_read_error_message(self.role_name_too_long),
                                                           "errorNo message for code=RoleNameLengthExceeded")

        # press Cancel button after the adding of new role name was rejected
        self.assertTrue(add_roles_pop_up.press_cancel_new_role_pop_up_window(), "Cancel button is not available")

        # test visibility of all web elements on Roles page , after the dialog window was closed
        self.assertTrue(roles_menu.user_page_elements_test(), "Some elements of Role page are not visible")

    # ============ Checking privileges =============== #
    def check_all_privileges_one_by_one_save_after_each_click(self):
        """Add role and check all privileges one-by-one. After each step press button 'Save changes' """
        # role_name_with_all_priv = "uP}p,'qe6NKH=Y.%F&6uS}hp[X}[6;[bq),SrB6cPs8tJt_vcXL^d"
        # Instantiate Add Role popup window
        # add_roles_pop_up = AddRolePopUp(self.driver)

        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)
        role_name_with_all_priv_parameters = []
        role_name_with_all_priv_parameters = PromoRequest(self.driver).add_role_request("true", self.role_name_with_all_priv)
        self.driver.refresh()

        # Click with the mouse on the Roles row in the Roles table
        roles_menu.click_on_the_role(self.role_name_with_all_priv)
        # sometimes the button "Save changes" remains gray for long time
        time.sleep(0.5)

        roles_menu.click_on_the_privilege_and_save_one_by_one()

        # test visibility of all web elements on Roles page , after the dialog window was closed
        self.assertTrue(roles_menu.user_page_elements_test(), "Some elements of Role page are not visible")

    def check_all_privileges_one_by_one_and_save_one_time(self):
        """Add role and check all privileges one-by-one. After all checkboxes are checked press button 'Save changes' """

        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)
        role_name_with_all_priv_parameters = []
        role_name_with_all_priv_parameters = PromoRequest(self.driver).add_role_request("true", self.role_name_with_all_priv)
        self.driver.refresh()

        # Click with the mouse on the Roles row in the Roles table
        roles_menu.click_on_the_role(self.role_name_with_all_priv)
        # sometimes the button "Save changes" remains gray for long time
        time.sleep(0.5)

        roles_menu.click_on_the_privilege_and_save_one_time()

        # test visibility of all web elements on Roles page , after the dialog window was closed
        self.assertTrue(roles_menu.user_page_elements_test(), "Some elements of Role page are not visible")

    # ============ Deleting roles =============== #
    def test_delete_roles_yes(self):
        """Create role, press remove the role, in removing dialog window press Yes"""
        # role_name_yes = "MAS&U<f>89VKS2/V5s)eG9z2"
        # Instantiate Add Role popup window
        add_roles_pop_up = AddRolePopUp(self.driver)
        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Press add role button
        self.assertTrue(add_roles_pop_up.press_add_new_role_pop_up_window(), "Add Role button is not available")

        # Add new role , make it active
        add_roles_pop_up.add_new_role_active(self.role_name_yes)

        # Verify that the new role appears in the DB and in the grid, and that the roles' parameters match
        self.assertTrue(roles_menu.verify_new_role_grid_vs_db(self.role_name_yes),
                                                                "The grid data doesn't correpond to the DB data")

        # test visibility of all web elements on Roles page , after the dialog window was closed
        self.assertTrue(roles_menu.user_page_elements_test(), "Some elements of Role page are not visible")

        # -- Removing the role, because we want to keep the grid clean --- #
        # Instantiate Remove Role dialog page
        remove_dialog = RemoveRoleDialog(self.driver)

        # If role was found in the grid and in DB , then remove the role:
        # press Delete button , remove dialog , Yes button
        roles_menu.remove_role_by_name(self.role_name_yes)
        remove_dialog.remove_role_dialog_window_test()
        remove_dialog.delete_role_click_yes()

        # test if the role was deleted from DB and from webpage
        self.assertTrue(roles_menu.verify_role_was_deleted_from_grid_and_db(self.role_name_yes),
                    "The role was not deleted from the DB or the grid doesn't show proper results after deletion")

    def test_delete_roles_cancel(self):
        """Create role, press remove the role, in removing dialog window press No"""
        # role_name_cancel = "jUHQb-j'-:pP,6f*"
        # Instantiate Add Role popup window
        add_roles_pop_up = AddRolePopUp(self.driver)
        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Press add role button
        self.assertTrue(add_roles_pop_up.press_add_new_role_pop_up_window(), "Add Role button is not available")

        # Add role with long role name for all privileges test case
        add_roles_pop_up.add_new_role_active(self.role_name_cancel)

        # Verify that the new role appears in the DB and in the grid, and that the roles' parameters match
        self.assertTrue(roles_menu.verify_new_role_grid_vs_db(self.role_name_cancel),
                                                                "The grid data doesn't correpond to the DB data")

        # test visibility of all web elements on Roles page , after the dialog window was closed
        self.assertTrue(roles_menu.user_page_elements_test(), "Some elements of Role page are not visible")

    # ------- Column manipulations via Kendo UI (from drop-down menu) ------- #
    # ============ Sorting from drop-down menu and by double-mouse click =============== #
    def test_sort_columns_privileges_table(self):
        """Sort ascending, descending the ID, OperationName, OperationUrl, IsActive columns from the dropdown menu in privileges table"""
        self.driver.maximize_window()
        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Instance of TableFilter class for accessing column filter capabilities
        drop_menu = TableFilter(self.driver)

        # Instance of Table for accessing Privileges table parameters
        table_parameters = Table(self.driver, roles_menu.get_the_table_element_privileges_without_headers())

        # # ====================== "ID" column , Privileges table ====================== #
        column_index = 1
        # if we want to sort integers, then isInt is True
        isInt = True

        # Get the ID column webelement from User roles page
        header_element = roles_menu.webelement_of_id_column_in_privilege_table()

        # === Sort ascending "ID" column from GUI with dropdown filters === #
        drop_menu.sort_ascending(header_element)

        # Get the list of all rows/webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "ID" column from GUI with dropdown filters === #
        drop_menu.sort_descending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending,
                        "Sorting ascending of 'ID' column has failed in Privileges table")
        self.assertTrue(kendo_sorted_descending,
                        "Sorting descending of 'ID' column has failed in Privileges table")
        # reset previous sorting/cancel sorting of one column in order to sort another one
        drop_menu.sort_descending(header_element)
        # ====================== "OperationName" column , Privileges table ====================== #
        column_index = 2
        # if we want to sort integers, then isInt is True
        isInt = False

        # Get the "OperationName" column webelement from User roles page
        header_element = roles_menu.webelement_of_operation_name_column_in_privilege_table()

        # === Sort ascending "OperationName" column from GUI with dropdown filters === #
        drop_menu.sort_ascending(header_element)

        # Get the list of all rows/webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # create instance of KendoSorting class and pass list of sorted rows from GUI, and column index
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take the sorted data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "OperationName" column from GUI with dropdown filters === #
        drop_menu.sort_descending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # create instance of KendoSorting class and pass list of sorted rows from GUI, and column index
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take the sorted data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending,
                        "Sorting ascending of 'OperationName' column has failed in Privileges table")
        self.assertTrue(kendo_sorted_descending,
                        "Sorting descending of 'OperationName' column has failed in Privileges table")

        drop_menu.sort_descending(header_element)
        # ====================== "OperationUrl" column , Privileges table ====================== #
        column_index = 3
        # if we want to sort integers, then isInt is True
        isInt = False

        # Get the "OperationUrl" column webelement from User roles page
        header_element = roles_menu.webelement_of_operation_url_column_in_privilege_table()

        # === Sort ascending "OperationUrl" column from GUI with dropdown filters === #
        drop_menu.sort_ascending(header_element)

        # Get the list of all rows/webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # create instance of KendoSorting class and pass list of sorted rows from GUI, and column index
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take the sorted data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "OperationUrl" column from GUI with dropdown filters === #
        drop_menu.sort_descending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # create instance of KendoSorting class and pass list of sorted rows from GUI, and column index
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take the sorted data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending,
                        "Sorting ascending of 'OperationUrl' column has failed in Privileges table")
        self.assertTrue(kendo_sorted_descending,
                        "Sorting descending of 'OperationUrl' column has failed in Privileges table")

        drop_menu.sort_descending(header_element)
        # ====================== "IsActive" column , Privileges table ====================== #
        column_index = 4
        # if we want to sort integers, then isInt is True
        isInt = False

        # Get the "IsActive" column webelement from User roles page
        header_element = roles_menu.webelement_of_operation_is_active_column_in_privilege_table()

        # === Sort ascending "IsActive" column from GUI with dropdown filters === #
        drop_menu.sort_ascending(header_element)

        # Get the list of all rows/webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # create instance of KendoSorting class and pass list of sorted rows from GUI, and column index
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take the sorted data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "IsActive" column from GUI with dropdown filters === #
        drop_menu.sort_descending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # create instance of KendoSorting class and pass list of sorted rows from GUI, and column index
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take the sorted data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending,
                        "Sorting ascending of 'IsActive' column has failed in Privileges table")
        self.assertTrue(kendo_sorted_descending,
                        "Sorting descending of 'IsActive' column has failed in Privileges table")

        drop_menu.sort_descending(header_element)

        # ---------------------------- Sorting with double-mouse click ------------------------ #
        # ====================== "ID" column , Privileges table ====================== #
        column_index = 1
        # if we want to sort integers, then isInt is True
        isInt = True

        # Get the ID column webelement from User roles page
        header_element = roles_menu.webelement_of_id_column_in_privilege_table()

        # === Sort ascending "ID" column from GUI with mouse === #
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)
        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "ID" column from GUI with mouse  === #

        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)
        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending, "Sorting ascending of ID column has failed in Privilege table")
        self.assertTrue(kendo_sorted_descending, "Sorting descending of ID column has failed in Privilege table")
        # reset previous sorting/cancel sorting of one column in order to sort another one
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)
        # ====================== "Operation name" column , Privileges table ====================== #
        # column_index = 2
        # # if we want to sort integers, then isInt is True
        # isInt = False
        #
        # # Get the "Operation name" column webelement from User roles page
        # header_element = roles_menu.webelement_of_operation_name_column_in_privilege_table()
        #
        # # === Sort ascending "Operation name" column from GUI with dropdown filters === #
        #
        # if Parser().get_browser_name() is 'IE':
        #     self.driver.execute_script("arguments[0].click();", header_element)
        # else:
        #     drop_menu.sort_with_mouse(header_element)
        # # Get the list of webelements from the table
        # list_of_rows = table_parameters.get_all_cells_element()
        #
        # # take the sorted data from the grid and index of the sorted column
        # kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)
        #
        # # take data from the grid and sort it according to Kendo algorithm, then
        # # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        # kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)
        #
        # # === Sort descending "Operation name" column from GUI with dropdown filters === #
        #
        # if Parser().get_browser_name() is 'IE':
        #     self.driver.execute_script("arguments[0].click();", header_element)
        # else:
        #     drop_menu.sort_with_mouse(header_element)
        #
        # # Get the list of webelements from the table
        # list_of_rows = table_parameters.get_all_cells_element()
        #
        # # take the sorted data from the grid and index of the sorted column
        # kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)
        #
        # # take data from the grid and sort it according to Kendo algorithm, then
        # # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        # kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)
        #
        # self.assertTrue(kendo_sorted_ascending, "Sorting ascending of 'Operation name' column has failed in Privilege table")
        # self.assertTrue(kendo_sorted_descending, "Sorting descending of 'Operation name' column has failed in Privilege table")
        # # reset previous sorting/cancel sorting of one column in order to sort another one
        # if Parser().get_browser_name() is 'IE':
        #     self.driver.execute_script("arguments[0].click();", header_element)
        # else:
        #     drop_menu.sort_with_mouse(header_element)

        # ====================== "Operation URL" column , Privileges table ====================== #
        column_index = 3
        # if we want to sort integers, then isInt is True
        isInt = False

        # Get the "IsActive" column webelement from User roles page
        header_element = roles_menu.webelement_of_operation_url_column_in_privilege_table()

        # === Sort ascending "OperationUrl" column from GUI with mouse === #
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "IsActive" column from GUI with mouse === #
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending, "Sorting ascending of 'OperationUrl' column has failed in Privilege table")
        self.assertTrue(kendo_sorted_descending, "Sorting descending of 'OperationUrl' column has failed in Privilege table")
        # reset previous sorting/cancel sorting of one column in order to sort another one
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)

        # ====================== "IsActive" column , Privileges table ====================== #
        column_index = 4
        # if we want to sort integers, then isInt is True
        isInt = False

        # Get the "IsActive" column webelement from User roles page
        header_element = roles_menu.webelement_of_operation_is_active_column_in_privilege_table()

        # === Sort ascending "IsActive" column from GUI with mouse === #
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "IsActive" column from GUI with mouse === #
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending, "Sorting ascending of 'IsActive' column has failed in Privilege table")
        self.assertTrue(kendo_sorted_descending, "Sorting descending of 'IsActive' column has failed in Privilege table")
        # reset previous sorting/cancel sorting of one column in order to sort another one
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)

    def test_sort_columns_roles_table(self):
        """Sort ascending, descending the ID, Role name, IsActive columns from the dropdown menu in roles table"""
       # self.driver.maximize_window()
        # =============================== Add some Roles which we can sort ======================== #

        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # == Add 1st role : "}=qt[e7x+b6;?/@a9P]dn9BU$5(kX}Z9"
        PromoRequest(self.driver).add_role_request("true", self.role1)

        # == Add 2nd role : "aBYwbb:E;(XjV3,>d[Q8-d_=2Ehs"
        PromoRequest(self.driver).add_role_request("true", self.role2)

        # == Add 3rd role : "ABcYwbb:E;(XjV3,>d[Q8-d_=2Ehs\""
        PromoRequest(self.driver).add_role_request("true", self.role3)

        self.driver.refresh()

        # =============================== Start sorting procedure ======================== #
        # Instance of TableFilter class for accessing column filter capabilities
        drop_menu = TableFilter(self.driver)

        # Instance of Table for accessing Roles table parameters
        table_parameters = Table(self.driver, roles_menu.get_the_table_element_roles_without_headers())

        # ====================== "ID" column , Roles table ====================== #
        column_index = 0
        # if we want to sort integers, then isInt is True
        isInt = True

        # Get the ID column webelement from User roles page
        header_element = roles_menu.webelement_of_id_column_in_roles_table()

        # === Sort ascending "ID" column from GUI with dropdown filters === #
        drop_menu.sort_ascending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "ID" column from GUI with dropdown filters === #
        drop_menu.sort_descending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending, "Sorting ascending of ID column has failed in Roles table")
        self.assertTrue(kendo_sorted_descending, "Sorting descending of ID column has failed in Roles table")
        # reset previous sorting/cancel sorting of one column in order to sort another one
        drop_menu.sort_descending(header_element)

        # ====================== "Role name" column , Roles table ====================== #
        column_index = 1
        # if we want to sort integers, then isInt is True
        isInt = False

        # Get the "Role name" column webelement from User roles page
        header_element = roles_menu.webelement_of_name_column_in_roles_table()

        # === Sort ascending "Role name" column from GUI with dropdown filters === #
        drop_menu.sort_ascending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "Role name" column from GUI with dropdown filters === #
        drop_menu.sort_descending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending, "Sorting ascending of 'Role name' column has failed in Roles table")
        self.assertTrue(kendo_sorted_descending, "Sorting descending of 'Role name' column has failed in Roles table")
        # reset previous sorting/cancel sorting of one column in order to sort another one
        drop_menu.sort_descending(header_element)

        # ====================== "IsActive" column , Roles table ====================== #
        column_index = 2
        # if we want to sort integers, then isInt is True
        isInt = False

        # Get the "IsActive" column webelement from User roles page
        header_element = roles_menu.webelement_of_isactive_column_in_roles_table()

        # === Sort ascending "IsActive" column from GUI with dropdown filters === #
        drop_menu.sort_ascending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "IsActive" column from GUI with dropdown filters === #
        drop_menu.sort_descending(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending, "Sorting ascending of 'IsActive' column has failed in Roles table")
        self.assertTrue(kendo_sorted_descending, "Sorting descending of 'IsActive' column has failed in Roles table")
        # reset previous sorting/cancel sorting of one column in order to sort another one
        drop_menu.sort_with_mouse(header_element)
        drop_menu.sort_with_mouse(header_element)

        # ---------------------------- Sorting with double-mouse click ------------------------ #
        # ====================== "ID" column , Roles table ====================== #
        column_index = 0
        # if we want to sort integers, then isInt is True
        isInt = True

        # Get the ID column webelement from User roles page
        header_element = roles_menu.webelement_of_id_column_in_roles_table()

        # === Sort ascending "ID" column from GUI with mouse === #
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)
        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)

        # === Sort descending "ID" column from GUI with mouse  === #
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)

        # Get the list of webelements from the table
        list_of_rows = table_parameters.get_all_cells_element()

        # take the sorted data from the grid and index of the sorted column
        kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)

        # take data from the grid and sort it according to Kendo algorithm, then
        # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)

        self.assertTrue(kendo_sorted_ascending, "Sorting ascending of ID column has failed in Roles table")
        self.assertTrue(kendo_sorted_descending, "Sorting descending of ID column has failed in Roles table")
        # reset previous sorting/cancel sorting of one column in order to sort another one
        if Parser().get_browser_name() is 'IE':
            self.driver.execute_script("arguments[0].click();", header_element)
            self.driver.execute_script("arguments[0].click();", header_element)
        else:
            drop_menu.sort_with_mouse(header_element)
            drop_menu.sort_with_mouse(header_element)
        # ====================== "Role name" column , Roles table ====================== #
        # column_index = 1
        # # if we want to sort integers, then isInt is True
        # isInt = False
        #
        # # Get the "Role name" column webelement from User roles page
        # header_element = roles_menu.webelement_of_name_column_in_roles_table()
        #
        # # === Sort ascending "Role name" column from GUI with dropdown filters === #
        #
        # if Parser().get_browser_name() is 'IE':
        #     self.driver.execute_script("arguments[0].click();", header_element)
        # else:
        #     drop_menu.sort_with_mouse(header_element)
        #
        # # Get the list of webelements from the table
        # list_of_rows = table_parameters.get_all_cells_element()
        #
        # # take the sorted data from the grid and index of the sorted column
        # kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)
        #
        # # take data from the grid and sort it according to Kendo algorithm, then
        # # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        # kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)
        #
        # # === Sort descending "Role name" column from GUI with dropdown filters === #
        # if Parser().get_browser_name() is 'IE':
        #     self.driver.execute_script("arguments[0].click();", header_element)
        # else:
        #     drop_menu.sort_with_mouse(header_element)
        #
        # # Get the list of webelements from the table
        # list_of_rows = table_parameters.get_all_cells_element()
        #
        # # take the sorted data from the grid and index of the sorted column
        # kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)
        #
        # # take data from the grid and sort it according to Kendo algorithm, then
        # # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        # kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)
        #
        # self.assertTrue(kendo_sorted_ascending, "Sorting ascending of 'Role name' column has failed in Roles table")
        # self.assertTrue(kendo_sorted_descending, "Sorting descending of 'Role name' column has failed in Roles table")
        # # reset previous sorting/cancel sorting of one column in order to sort another one
        # if Parser().get_browser_name() is 'IE':
        #     self.driver.execute_script("arguments[0].click();", header_element)
        # else:
        #     drop_menu.sort_with_mouse(header_element)

        # # ====================== "IsActive" column , Roles table ====================== #
        # column_index = 2
        # # if we want to sort integers, then isInt is True
        # isInt = False
        #
        # # Get the "IsActive" column webelement from User roles page
        # header_element = roles_menu.webelement_of_isactive_column_in_roles_table()
        #
        # # === Sort ascending "IsActive" column from GUI with mouse === #
        # if Parser().get_browser_name() is 'IE':
        #     self.driver.execute_script("arguments[0].click();", header_element)
        # else:
        #     drop_menu.sort_with_mouse(header_element)
        #
        # # Get the list of webelements from the table
        # list_of_rows = table_parameters.get_all_cells_element()
        #
        # # take the sorted data from the grid and index of the sorted column
        # kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)
        #
        # # take data from the grid and sort it according to Kendo algorithm, then
        # # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        # kendo_sorted_ascending = kendo_sort_instance.sort_strings_ascending(isInt)
        #
        # # === Sort descending "IsActive" column from GUI with mouse === #
        # if Parser().get_browser_name() is 'IE':
        #     self.driver.execute_script("arguments[0].click();", header_element)
        # else:
        #     drop_menu.sort_with_mouse(header_element)
        #
        # # Get the list of webelements from the table
        # list_of_rows = table_parameters.get_all_cells_element()
        #
        # # take the sorted data from the grid and index of the sorted column
        # kendo_sort_instance = KendoSorting(self.driver, list_of_rows, column_index)
        #
        # # take data from the grid and sort it according to Kendo algorithm, then
        # # take the same/sorted data from  the grid, and compare both results , if match then sorting was successful
        # kendo_sorted_descending = kendo_sort_instance.sort_strings_descending(isInt)
        #
        # self.assertTrue(kendo_sorted_ascending, "Sorting ascending of 'IsActive' column has failed in Roles table")
        # self.assertTrue(kendo_sorted_descending, "Sorting descending of 'IsActive' column has failed in Roles table")
        # # reset previous sorting/cancel sorting of one column in order to sort another one
        # if Parser().get_browser_name() is 'IE':
        #     self.driver.execute_script("arguments[0].click();", header_element)
        # else:
        #     drop_menu.sort_with_mouse(header_element)

    # ============ Make columns visible or invisible =============== #
    def test_columns_check_uncheck_drop_down_roles_table(self):
        """Check/uncheck column names in drop-down menu - when unchecked, column disappears from the Role name table"""
        # Instantiate User Role page
        roles_page = UserRolesPage(self.driver)
        table_instance = TableFilter(self.driver)

        column_id_test = False
        column_role_name_test = False
        column_is_active_test = False
        column_operations_test = False

        # ================ "ID" column checked , others unchecked / Role names table ================ #
        # Check if all columns are visible before checking/unchecking them
        if table_instance.is_column_displayed(roles_page.locator_id_column()) and \
            table_instance.is_column_displayed(roles_page.locator_role_name_column()) and \
            table_instance.is_column_displayed(roles_page.locator_is_active_column()) and \
            table_instance.is_column_displayed(roles_page.locator_operations_column()):

            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_id_column()),
                            "The ID checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_role_name_column()),
                            "The Role name checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_is_active_column()),
                            "The IsActive checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operations_column()),
                            "The Operations checkbox is not enabled")

            # get the webelement of ID column in the Role names table
            webelem_id = roles_page.webelement_of_id_column_in_roles_table()
            # get the locators of 3 checkboxes except id checkbox
            checkbox_elements = roles_page.locators_all_checkboxes_except_id()
            # uncheck 3 checkboxes: Role name, IsActive, Operations in the drop-down columns filter
            table_instance.columns_settings(webelem_id, checkbox_elements)

            column_id_test = table_instance.is_column_displayed(roles_page.locator_id_column())
            column_role_name_test = table_instance.is_column_displayed(roles_page.locator_role_name_column())
            column_is_active_test = table_instance.is_column_displayed(roles_page.locator_is_active_column())
            column_operations_test = table_instance.is_column_displayed(roles_page.locator_operations_column())
            time.sleep(0.5)
            # check back 3 checkboxes: Role name, IsActive, Operations in the drop-down columns filter
            # we need to start next test with all columns enabled
            table_instance.columns_settings(webelem_id, checkbox_elements)

        self.assertTrue(column_id_test, "The ID is disabled, but should be enabled")
        self.assertFalse(column_role_name_test, "The Role name column is enabled, but should be disabled")
        self.assertFalse(column_is_active_test, "The IaActives column is enabled, but should be disabled")
        self.assertFalse(column_operations_test, "The Operations column is enabled, but should be disabled")

        # ================ "Role name" column checked , others unchecked / Role names table ================ #
        # Check if all columns are visible before checking/unchecking them
        if table_instance.is_column_displayed(roles_page.locator_id_column()) and \
            table_instance.is_column_displayed(roles_page.locator_role_name_column()) and \
            table_instance.is_column_displayed(roles_page.locator_is_active_column()) and \
            table_instance.is_column_displayed(roles_page.locator_operations_column()):

            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_id_column()),
                            "The ID checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_role_name_column()),
                            "The Role name checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_is_active_column()),
                            "The IsActive checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operations_column()),
                            "The Operations checkbox is not enabled")

            # get the webelement of "Role name" column in the Role names table
            webelem_role_name = roles_page.webelement_of_name_column_in_roles_table()
            # get the locators of 3 checkboxes except role name checkbox
            checkbox_elements = roles_page.locators_all_checkboxes_except_role_name()
            # uncheck 3 checkboxes: Role name, IsActive, Operations in the drop-down columns filter
            table_instance.columns_settings(webelem_role_name, checkbox_elements)

            column_id_test = table_instance.is_column_displayed(roles_page.locator_id_column())
            column_role_name_test = table_instance.is_column_displayed(roles_page.locator_role_name_column())
            column_is_active_test = table_instance.is_column_displayed(roles_page.locator_is_active_column())
            column_operations_test = table_instance.is_column_displayed(roles_page.locator_operations_column())
            time.sleep(0.5)
            # check back 3 checkboxes: Role name, IsActive, Operations in the drop-down columns filter
            # we need to start next test with all columns enabled
            table_instance.columns_settings(webelem_role_name, checkbox_elements)

        self.assertFalse(column_id_test, "The ID column is enabled, but should be disabled")
        self.assertTrue(column_role_name_test, "The Role name column is disabled, but should be enabled")
        self.assertFalse(column_is_active_test, "The IaActives column is enabled, but should be disabled")
        self.assertFalse(column_operations_test, "The Operations column is enabled, but should be disabled")

        # ================ "IsActive" column checked , others unchecked / Role names table ================ #
        # Check if all columns are visible before checking/unchecking them
        if table_instance.is_column_displayed(roles_page.locator_id_column()) and \
                table_instance.is_column_displayed(roles_page.locator_role_name_column()) and \
                table_instance.is_column_displayed(roles_page.locator_is_active_column()) and \
                table_instance.is_column_displayed(roles_page.locator_operations_column()):

            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_id_column()),
                            "The ID checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_role_name_column()),
                            "The Role name checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_is_active_column()),
                            "The IsActive checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operations_column()),
                            "The Operations checkbox is not enabled")

            # get the webelement of "IsActive" column in the Role names table
            webelem_is_active = roles_page.webelement_of_isactive_column_in_roles_table()
            # get the locators of 3 checkboxes except Is Active checkbox
            checkbox_elements = roles_page.locators_all_checkboxes_except_is_active()
            # uncheck 3 checkboxes: Role name, IsActive, Operations in the drop-down columns filter
            table_instance.columns_settings(webelem_is_active, checkbox_elements)

            column_id_test = table_instance.is_column_displayed(roles_page.locator_id_column())
            column_role_name_test = table_instance.is_column_displayed(roles_page.locator_role_name_column())
            column_is_active_test = table_instance.is_column_displayed(roles_page.locator_is_active_column())
            column_operations_test = table_instance.is_column_displayed(roles_page.locator_operations_column())
            time.sleep(0.5)
            # check back 3 checkboxes: Role name, IsActive, Operations in the drop-down columns filter
            # we need to start next test with all columns enabled
            table_instance.columns_settings(webelem_is_active, checkbox_elements)

        self.assertFalse(column_id_test, "The ID column is enabled, but should be disabled")
        self.assertFalse(column_role_name_test, "The Role name column is enabled, but should be disabled")
        self.assertTrue(column_is_active_test, "The IsActive column is disabled, but should be enabled")
        self.assertFalse(column_operations_test, "The Operations column is enabled, but should be disabled")

    def test_columns_check_uncheck_drop_down_privileges_table(self):
        """Check/uncheck column names in drop-down menu - when unchecked, column disappears from the Privileges table"""
        # Instantiate User Role page
        roles_page = UserRolesPage(self.driver)
        table_instance = TableFilter(self.driver)

        column_id_test = False
        column_operation_name_test = False
        column_operation_url_test = False
        column_is_active_test = False

        # ================ "ID" column checked , others unchecked / Privilege names table ================ #
        # Check if all columns are visible before checking/unchecking them
        if table_instance.is_column_displayed(roles_page.locator_id_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_operation_name_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_operation_url_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_is_active_column_privilege()):
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_id_column_privilege()),
                            "The ID checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operation_name_column_privilege()),
                            "The Operation name checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operation_url_column_privilege()),
                            "The Operation Url checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_is_active_column_privilege()),
                            "The Is Active checkbox is not enabled")

            # get the webelement of ID column in the Privileges table
            webelem_id = roles_page.webelement_of_id_column_in_privilege_table()
            # get the locators of 3 checkboxes except id checkbox
            checkbox_elements = roles_page.locators_all_checkboxes_except_id_priv()
            # uncheck 3 checkboxes
            table_instance.columns_settings(webelem_id, checkbox_elements)

            column_id_test = table_instance.is_column_displayed(roles_page.locator_id_column_privilege())
            column_operation_name_test = table_instance.is_column_displayed(roles_page.locator_operation_name_column_privilege())
            column_operation_url_test = table_instance.is_column_displayed(roles_page.locator_operation_url_column_privilege())
            column_is_active_test = table_instance.is_column_displayed(roles_page.locator_is_active_column_privilege())
            time.sleep(0.5)
            # check back 3 checkboxes
            table_instance.columns_settings(webelem_id, checkbox_elements)

        self.assertTrue(column_id_test, "The ID is disabled, but should be enabled")
        self.assertFalse(column_operation_name_test, "The Operation name column is enabled, but should be disabled")
        self.assertFalse(column_operation_url_test, "The Operation Url column is enabled, but should be disabled")
        self.assertFalse(column_is_active_test, "The Is Active column is enabled, but should be disabled")

        # ================ "Operation name" column checked , others unchecked / Privilege names table ================ #
        # Check if all columns are visible before checking/unchecking them
        if table_instance.is_column_displayed(roles_page.locator_id_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_operation_name_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_operation_url_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_is_active_column_privilege()):
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_id_column_privilege()),
                            "The ID checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operation_name_column_privilege()),
                            "The Operation name checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operation_url_column_privilege()),
                            "The Operation Url checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_is_active_column_privilege()),
                            "The Is Active checkbox is not enabled")

            # get the webelement of "Operation name" column in the Privilege names table
            webelem_operation_name = roles_page.webelement_of_operation_name_column_in_privilege_table()
            # get the locators of 3 checkboxes except Operation name checkbox
            checkbox_elements = roles_page.locators_all_checkboxes_except_operation_name_priv()
            # uncheck 3 checkboxes
            table_instance.columns_settings(webelem_operation_name, checkbox_elements)

            column_id_test = table_instance.is_column_displayed(roles_page.locator_id_column_privilege())
            column_operation_name_test = table_instance.is_column_displayed(roles_page.locator_operation_name_column_privilege())
            column_operation_url_test = table_instance.is_column_displayed(roles_page.locator_operation_url_column_privilege())
            column_is_active_test = table_instance.is_column_displayed(roles_page.locator_is_active_column_privilege())
            time.sleep(0.5)

            # check back 3 checkboxes
            table_instance.columns_settings(webelem_operation_name, checkbox_elements)

        self.assertFalse(column_id_test, "The ID column is enabled, but should be disabled")
        self.assertTrue(column_operation_name_test, "The Operation name column is disabled, but should be enabled")
        self.assertFalse(column_operation_url_test, "The Operation Url column is enabled, but should be disabled")
        self.assertFalse(column_is_active_test, "The Is Active column is enabled, but should be disabled")

        # ================ "Operation Url" column checked , others unchecked / Privilege names table ================ #
        # Check if all columns are visible before checking/unchecking them
        if table_instance.is_column_displayed(roles_page.locator_id_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_operation_name_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_operation_url_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_is_active_column_privilege()):
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_id_column_privilege()),
                            "The ID checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operation_name_column_privilege()),
                            "The Operation name checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operation_url_column_privilege()),
                            "The Operation Url checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_is_active_column_privilege()),
                            "The Is Active checkbox is not enabled")

            # get the webelement of "Operation Url" column in the Role names table
            webelem_operation_url = roles_page.webelement_of_operation_url_column_in_privilege_table()
            # get the locators of 3 checkboxes except Operation Url checkbox
            checkbox_elements = roles_page.locators_all_checkboxes_except_operation_url_priv()
            # uncheck 3 checkboxes
            table_instance.columns_settings(webelem_operation_url, checkbox_elements)

            column_id_test = table_instance.is_column_displayed(roles_page.locator_id_column_privilege())
            column_operation_name_test = table_instance.is_column_displayed(roles_page.locator_operation_name_column_privilege())
            column_operation_url_test = table_instance.is_column_displayed(roles_page.locator_operation_url_column_privilege())
            column_is_active_test = table_instance.is_column_displayed(roles_page.locator_is_active_column_privilege())
            time.sleep(0.5)
            # check back 3 checkboxes
            table_instance.columns_settings(webelem_operation_url, checkbox_elements)

        self.assertFalse(column_id_test, "The ID column is enabled, but should be disabled")
        self.assertFalse(column_operation_name_test, "The Operation name column is enabled, but should be disabled")
        self.assertTrue(column_operation_url_test, "The Operation Url column is disabled, but should be enabled")
        self.assertFalse(column_is_active_test, "The Is Active column is enabled, but should be disabled")

        # ================ "Is Active" column checked , others unchecked / Privilege names table ================ #
        # Check if all columns are visible before checking/unchecking them
        if table_instance.is_column_displayed(roles_page.locator_id_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_operation_name_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_operation_url_column_privilege()) and \
                table_instance.is_column_displayed(roles_page.locator_is_active_column_privilege()):
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_id_column_privilege()),
                            "The ID checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operation_name_column_privilege()),
                            "The Operation name checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_operation_url_column_privilege()),
                            "The Operation Url checkbox is not enabled")
            self.assertTrue(table_instance.is_checkbox_enabled(roles_page.locator_is_active_column_privilege()),
                            "The Is Active checkbox is not enabled")

            # get the webelement of "Is Active" column in the Role names table
            webelem_is_active = roles_page.webelement_of_operation_is_active_column_in_privilege_table()
            # get the locators of 3 checkboxes except Operation Url checkbox
            checkbox_elements = roles_page.locators_all_checkboxes_except_is_active_priv()
            # uncheck 3 checkboxes
            table_instance.columns_settings(webelem_is_active, checkbox_elements)

            column_id_test = table_instance.is_column_displayed(roles_page.locator_id_column_privilege())
            column_operation_name_test = table_instance.is_column_displayed(roles_page.locator_operation_name_column_privilege())
            column_operation_url_test = table_instance.is_column_displayed(roles_page.locator_operation_url_column_privilege())
            column_is_active_test = table_instance.is_column_displayed(roles_page.locator_is_active_column_privilege())
            time.sleep(0.5)
            # check back 3 checkboxes
            table_instance.columns_settings(webelem_is_active, checkbox_elements)

        self.assertFalse(column_id_test, "The ID column is enabled, but should be disabled")
        self.assertFalse(column_operation_name_test, "The Operation name column is enabled, but should be disabled")
        self.assertFalse(column_operation_url_test, "The Operation Url column is enabled, but should be disabled")
        self.assertTrue(column_is_active_test, "The Is Active column is disabled, but should be enabled")

    # TODO because of the bug with filter types (we use string filters instead of number filters) ,
    # TODO some of the tests has to be re-worked in order to match the type of filter
    # ============ Filter columns by cell values (filter table results) =============== #
    def test_filters_for_role_table(self):
        """Filter column data with drop-down menu in Role table"""
        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # == Add 5th role : "-UM@myKt8B&pMT97MV#T"
        role_5_parameters = PromoRequest(self.driver).add_role_request("true", self.role5)

        # == Add 6th role : "9z4XzxtyPGwn"
        role_6_parameters = PromoRequest(self.driver).add_role_request("false", self.role6)

        self.driver.refresh()

        # Instance of TableFilter class for accessing column filter capabilities
        table_instance = Table(self.driver, roles_menu.get_the_table_element_roles_without_headers())

        # Instance of Table class
        table_filter = TableFilter(self.driver)

        # Get the ID column locator from User roles page for calling filter menu from the column's menu
        header_locator = roles_menu.locator_id_column()
        # Get the ID column webelement from User roles page
        header_web_element = roles_menu.webelement_of_id_column_in_roles_table()

        is_equal_to_or_is_equal_to = False
        is_not_equal_to_and_is_equal_to = False
        is_not_null_and_is_equal_to = False
        is_equal_to_and_is_null = False

        # get the ID value for the role 5
        role_id_role5 = role_5_parameters[0]
        role_name_role5 = role_5_parameters[1]
        role_isactive_role5 = role_5_parameters[2]
        role_id_role5_parameters = [role_id_role5, role_name_role5, role_isactive_role5]
        # get the ID value for the role 6
        role_id_role6 = role_6_parameters[0]
        role_name_role6 = role_6_parameters[1]
        role_isactive_role6 = role_6_parameters[2]
        role_id_role6_parameters = [role_id_role6, role_name_role6, role_isactive_role6]

        # ====================== Filtering on "ID" column , Role table ====================== #

        # check if column is visible in order to avoid further problems during filtering
        if table_filter.is_column_displayed(header_locator):

            # === "Is equal to" OR "Is equal to" === #

            # Filter by ID: role_id_role5 or role_id_role6 should result in 2 rows with id 5 and id 6
            table_filter.filter_from_header_by_number(header_web_element, 'Is equal to', int(role_id_role5), 'Is equal to',
                                                      int(role_id_role6), 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is True and role6_found is True:
                is_equal_to_or_is_equal_to = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is not equal to" AND "Is equal to" === #

            header_web_element = roles_menu.webelement_of_id_column_in_roles_table()

            table_filter.filter_from_header_by_number(header_web_element, 'Is not equal to', 1, 'Is equal to',
                                                      int(role_id_role6), 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is False and role6_found is True:
                    is_not_equal_to_and_is_equal_to = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is not null" AND "Is equal to" === #

            header_web_element = roles_menu.webelement_of_id_column_in_roles_table()

            table_filter.filter_from_header_by_number(header_web_element, 'Is not null', '', 'Is equal to',
                                                      int(role_id_role6), 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is False and role6_found is True:
                    is_not_null_and_is_equal_to = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is equal to" OR "Is null" === #

            header_web_element = roles_menu.webelement_of_id_column_in_roles_table()
            # role_id_role6 != 1 and role_id_role6 == 511 should result in 1 rows with id 6
            table_filter.filter_from_header_by_number(header_web_element, 'Is equal to', int(role_id_role5), 'Is null',
                                                      int(role_id_role6), 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is True and role6_found is False:
                    is_equal_to_and_is_null = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            self.assertTrue(is_equal_to_or_is_equal_to, "Filters: 'Is equal to' OR 'Is equal to' don't work")
            self.assertTrue(is_not_equal_to_and_is_equal_to, "Filters: 'Is not equal to' AND 'Is equal to' don't work")
            self.assertTrue(is_not_null_and_is_equal_to, "Filters: 'Is not null' AND 'Is equal to' don't work")
            self.assertTrue(is_equal_to_and_is_null, "Filters: 'Is equal to' AND 'Is null' don't work")

        # ====================== Filtering on "Role name" column , Role table ====================== #

        # Get the Role name column locator from User roles page for calling filter menu from the column's menu
        header_locator = roles_menu.locator_role_name_column()
        # Get the Role name column webelement from User roles page
        header_web_element = roles_menu.webelement_of_name_column_in_roles_table()

        is_equal_to_or_is_equal_to = False
        is_equal_to_and_is_not_equal_to = False
        starts_with_and_does_not_contain = False
        ends_with_or_ends_with = False
        is_null = False
        is_null_or_is_not_empty = False
        is_not_null_is_empty = False

        # check if column is visible in order to avoid further problems during filtering
        if table_filter.is_column_displayed(header_locator):

            # === "Is equal to" OR "Is equal to" === #

            # Filter by ID: role_id_role5 or role_id_role6 should result in 2 rows with id 5 and id 6
            table_filter.filter_from_header_by_string(header_web_element, 'Is equal to', role_name_role5, 'Is equal to',
                                                      role_name_role6, 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is True and role6_found is True:
                    is_equal_to_or_is_equal_to = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is equal to" AND "Is not equal to" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is equal to', role_name_role5,
                                                      'Is not equal to', role_name_role6, 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is True and role6_found is False:
                    is_equal_to_and_is_not_equal_to = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Starts with" AND "Does not contain" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Starts with', "-",
                                                                                'Does not contain', "*", 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is True and role6_found is False:
                    starts_with_and_does_not_contain = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Ends with" OR "Ends with" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Ends with', "T", 'Ends with', "n", 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is True and role6_found is True:
                    ends_with_or_ends_with = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is null" AND "Does not contain" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is null', "",
                                                      'Does not contain',
                                                      "D;,d$xTqP^_A@esKh>Sg}:rV*Y6pb3PU}>Kn`22g%eEP*u?e=K\"')xF*t!`v"
                                    "g\"NF<YsHdp&;ywPN-ym;EX*njz28qeJdeR.qe+)P}\\bA,hT\"<}24&B##&YjS+6c9,j=/", 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results
            if len(all_cells_list) == 0:
                is_null = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is null" OR "Is not empty" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is null', "", 'Is not empty', "", 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is True and role6_found is True:
                    is_null_or_is_not_empty = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is not null" AND "Is empty" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is not null', "", 'Is empty', "", 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results
            if len(all_cells_list) == 0:
                is_not_null_is_empty = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            self.assertTrue(is_equal_to_or_is_equal_to, "Filters: 'Is equal to' OR 'Is equal to' don't work")
            self.assertTrue(is_equal_to_and_is_not_equal_to, "Filters: 'Is equal to' AND 'Is not equal to' don't work")
            self.assertTrue(starts_with_and_does_not_contain, "Filters: 'Starts with' AND 'Does not contain' don't work")
            self.assertTrue(ends_with_or_ends_with, "Filters: 'Ends with' OR 'Ends with' don't work")
            self.assertTrue(is_null, "Filters: 'Is null' doesn't work")
            self.assertTrue(is_null_or_is_not_empty, "Filters: 'Is null' OR 'Is not empty' don't work")
            self.assertTrue(is_not_null_is_empty, "Filters: 'Is not null' OR 'Is empty' don't work")

        # ====================== Filtering on "IsActive" column , Role table ====================== #

        # Get the ID column locator from User roles page for calling filter menu from the column's menu
        header_locator = roles_menu.locator_is_active_column()
        # Get the ID column webelement from User roles page
        header_web_element = roles_menu.webelement_of_isactive_column_in_roles_table()

        is_true = False
        is_false = False

        # check if column is visible in order to avoid further problems during filtering
        if table_filter.is_column_displayed(header_locator):

            # === "Is true" === #

            table_filter.filter_from_header_by_radiobutton(header_web_element, True)
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is True and role6_found is False:
                is_true = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is false" === #

            table_filter.filter_from_header_by_radiobutton(header_web_element, False)
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role5_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role5_parameters)
            role6_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_role6_parameters)

            if len(all_cells_list) > 0 and role5_found is False and role6_found is True:
                is_false = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            self.assertTrue(is_true, "Filters: 'true' doesn't work")
            self.assertTrue(is_false, "Filters: 'false' doesn't work")

    @unittest.expectedFailure
    def test_filters_for_privilege_table(self):
        """Filter column data with drop-down menu in Privilege table"""
        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Instance of TableFilter class for accessing column filter capabilities
        table_instance = Table(self.driver, roles_menu.get_the_table_element_privileges_without_headers())

        # Instance of Table class
        table_filter = TableFilter(self.driver)

        # Get the ID column locator from User roles page for calling filter menu from the column's menu
        header_locator = roles_menu.locator_id_column_privilege()
        # Get the ID column webelement from User roles page
        header_web_element = roles_menu.webelement_of_id_column_in_privilege_table()

        is_equal_to_and_is_not_null = False
        is_not_equal_to_or_is_empty = False
        is_null_and_is_equal_to = False

        role_id_11_parameters = ["11", "Allow.ReadLog", "true"]
        role_id_role_11 = role_id_11_parameters[0]

        # ====================== Filtering on "ID" column , Privilege table ====================== #

        # check if column is visible in order to avoid further problems during filtering
        if table_filter.is_column_displayed(header_locator):

            # === "Is equal to" AND "Is not null" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is equal to', role_id_role_11,
                                                      'Is not null', "", 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role_id_11_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_11_parameters)

            if len(all_cells_list) > 0 and role_id_11_found is True:
                is_equal_to_and_is_not_null = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is not equal to" OR "Is empty" === #

            header_web_element = roles_menu.webelement_of_id_column_in_privilege_table()

            table_filter.filter_from_header_by_string(header_web_element, 'Is not equal to', role_id_role_11, 'Is empty',
                                                      "", 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role_id_11_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_11_parameters)

            # role_id_11_found should be False because the role 11 has to be filtered out
            if len(all_cells_list) > 0 and role_id_11_found is False:
                is_not_equal_to_or_is_empty = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is null" AND "Is equal to" === #

            header_web_element = roles_menu.webelement_of_id_column_in_privilege_table()

            table_filter.filter_from_header_by_string(header_web_element, 'Is null', '', 'Is equal to',
                                                      role_id_role_11, 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            if len(all_cells_list) == 0:
                is_null_and_is_equal_to = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)
######################
            # === "Is greater than or equal to" AND "Is less than" === #

            header_web_element = roles_menu.webelement_of_id_column_in_privilege_table()

            table_filter.filter_from_header_by_string(header_web_element, 'Is not equal to', role_id_role_11, 'Is empty',
                                                      "", 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            role_id_11_found = table_instance.find_web_element_text_from_all_cells(all_cells_list, role_id_11_parameters)

            # role_id_11_found should be False because the role 11 has to be filtered out
            if len(all_cells_list) > 0 and role_id_11_found is False:
                is_not_equal_to_or_is_empty = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

        self.assertTrue(is_equal_to_and_is_not_null, "Filters: 'Is equal to' AND 'Is not null' don't work")
        self.assertTrue(is_not_equal_to_or_is_empty, "Filters: 'Is not equal to' OR 'Is empty' don't work")
        self.assertTrue(is_null_and_is_equal_to, "Filters: 'Is null' AND 'Is equal to' don't work")

        # ====================== Filtering on "Operation name" column , Privilege table ====================== #

        # Get the Role name column locator from User roles page for calling filter menu from the column's menu
        header_locator = roles_menu.locator_operation_name_column_privilege()
        # Get the Role name column webelement from User roles page
        header_web_element = roles_menu.webelement_of_operation_name_column_in_privilege_table()

        is_equal_to_or_is_equal_to = False
        is_equal_to_and_is_not_equal_to = False
        starts_with_and_does_not_contain = False
        ends_with_or_ends_with = False
        is_null = False
        is_null_or_is_not_empty = False
        is_not_null_is_empty = False

        operation_name_11_parameters = ["11", "Allow.ReadLog", "true"]
        operation_name_11 = operation_name_11_parameters[1]

        operation_name_12_parameters = ["12", "Allow.EditLogSettings", "true"]
        operation_name_12 = operation_name_12_parameters[1]

        # check if column is visible in order to avoid further problems during filtering
        if table_filter.is_column_displayed(header_locator):

            # === "Is equal to" OR "Is equal to" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is equal to', operation_name_11,
                                                      'Is equal to', operation_name_12, 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            operation_name_11_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                                          operation_name_11_parameters)
            operation_name_12_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                                          operation_name_12_parameters)

            if len(all_cells_list) > 0 and operation_name_11_found is True and operation_name_12_found is True:
                is_equal_to_or_is_equal_to = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is equal to" AND "Is not equal to" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is equal to', operation_name_11,
                                                      'Is not equal to', operation_name_12, 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            operation_name_11_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                                          operation_name_11_parameters)
            operation_name_12_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                                          operation_name_12_parameters)

            if len(all_cells_list) > 0 and operation_name_11_found is True and operation_name_12_found is False:
                is_equal_to_and_is_not_equal_to = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Starts with" AND "Does not contain" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Starts with', "A",
                                                      'Does not contain', operation_name_12, 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            operation_name_11_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                                          operation_name_11_parameters)
            operation_name_12_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                                          operation_name_12_parameters)

            if len(all_cells_list) > 0 and operation_name_11_found is True and operation_name_12_found is False:
                starts_with_and_does_not_contain = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Ends with" OR "Ends with" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Ends with', "Log", 'Ends with', "Settings", 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            operation_name_11_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                              operation_name_11_parameters)
            operation_name_12_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                              operation_name_12_parameters)

            if len(all_cells_list) > 0 and operation_name_11_found is True and operation_name_12_found is True:
                ends_with_or_ends_with = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is null" AND "Does not contain" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is null', "", 'Does not contain', "", 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results
            if len(all_cells_list) == 0:
                is_null = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is null" OR "Is not empty" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is null', "", 'Is not empty', "", 'or')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            operation_name_11_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                                          operation_name_11_parameters)
            operation_name_12_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                                          operation_name_12_parameters)

            if len(all_cells_list) > 0 and operation_name_11_found is True and operation_name_12_found is True:
                is_null_or_is_not_empty = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            # === "Is not null" AND "Is empty" === #

            table_filter.filter_from_header_by_string(header_web_element, 'Is not null', "", 'Is empty', "", 'and')
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results
            if len(all_cells_list) == 0:
                is_not_null_is_empty = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            self.assertTrue(is_equal_to_or_is_equal_to, "Filters: 'Is equal to' OR 'Is equal to' don't work")
            self.assertTrue(is_equal_to_and_is_not_equal_to,
                            "Filters: 'Is equal to' AND 'Is not equal to' don't work")
            self.assertTrue(starts_with_and_does_not_contain,
                            "Filters: 'Starts with' AND 'Does not contain' don't work")
            self.assertTrue(ends_with_or_ends_with, "Filters: 'Ends with' OR 'Ends with' don't work")
            self.assertTrue(is_null, "Filters: 'Is null' doesn't work")
            self.assertTrue(is_null_or_is_not_empty, "Filters: 'Is null' OR 'Is not empty' don't work")
            self.assertTrue(is_not_null_is_empty, "Filters: 'Is not null' OR 'Is empty' don't work")

        # ====================== Filtering on "IsActive" column , Role table ====================== #

        # Get the ID column locator from User roles page for calling filter menu from the column's menu
        header_locator = roles_menu.locator_is_active_column_privilege()
        # Get the ID column webelement from User roles page
        header_web_element = roles_menu.webelement_of_operation_is_active_column_in_privilege_table()

        is_true = False

        # check if column is visible in order to avoid further problems during filtering
        if table_filter.is_column_displayed(header_locator):

            # === "Is true" === #

            table_filter.filter_from_header_by_radiobutton(header_web_element, True)
            # get all rows in the table
            all_cells_list = table_instance.get_all_cells_element()

            # compare results from grid with the expected filtering results , plus comparison with DB
            operation_name_11_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                              operation_name_11_parameters)
            operation_name_12_found = table_instance.find_web_element_text_from_all_cells(all_cells_list,
                                                                              operation_name_12_parameters)

            if len(all_cells_list) > 0 and operation_name_11_found is True and operation_name_12_found is True:
                is_true = True

            # clear filter and restore original grid view
            table_filter.clear_filter_form(header_web_element)

            self.assertTrue(is_true, "Filters: 'true' doesn't work")

    # ============ Change column locations by drag-and-drop with mouse =============== #
    # working only in Chrome , because drag_and_drop doesn't work with IE11
    # TODO drag_and_drop in IE11 or another similar method for changing column locations in IE11
    def test_changing_position_of_columns_roles_table(self):
        """Change position of columns in Role table"""
        # Instantiate Add Role popup window
        #add_roles_pop_up = AddRolePopUp(self.driver)

        # Instantiate User Role page
        roles_menu = UserRolesPage(self.driver)

        # Instance of TableFilter class for accessing column filter capabilities
        table_inst = TableFilter(self.driver)

        class Columns_webelement:
            column_1 = ""
            column_2 = ""
            column_3 = ""
            column_4 = ""

            @classmethod
            def update(cls, value_1, value_2, value_3, value_4):
                cls.column_1 = value_1
                cls.column_2 = value_2
                cls.column_3 = value_3
                cls.column_4 = value_4

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())
        # get the whole table webelement
        role_table_webelement = roles_menu.get_the_table_element_roles_full()

        # Read current headers from the Role table and save its names to list
        # in the order as it is appears in the HTML tree from top to down
        roles_table = 1
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM,
        # compare it from the results from the whole table webelement
        columns_default_state_bool = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move ID column to Role name column =========================== #
        # === Switch column places : "ID" and "Role name" columns === #
        table_inst.change_column_location(Columns_webelement.column_1, Columns_webelement.column_2)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        columns_id_role_name_bool = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move ID column to IsActive column =========================== #
        # === Switch column places : "ID" and "IsActive" columns === #
        table_inst.change_column_location(Columns_webelement.column_2, Columns_webelement.column_3)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_id_isactive_bool = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move ID column to Operations column =========================== #
        # === Switch column places : "ID" and "Operations" columns === #
        table_inst.change_column_location(Columns_webelement.column_3, Columns_webelement.column_4)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_id_operations_bool = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move Role name column to IsActive column =========================== #
        # === Switch column places : "Role name" and "IsActive" columns === #
        table_inst.change_column_location(Columns_webelement.column_1, Columns_webelement.column_2)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_role_name_is_active_bool = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move Role name column to Operations column =========================== #
        # === Switch column places : "Role name" and "Operations" columns === #
        table_inst.change_column_location(Columns_webelement.column_2, Columns_webelement.column_3)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_role_name_operations_bool = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move Role name column to ID column =========================== #
        # === Switch column places : "Role name" and "ID" columns === #
        table_inst.change_column_location(Columns_webelement.column_3, Columns_webelement.column_4)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_role_name_id_bool = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move IsActive column to Operations column =========================== #
        # === Switch column places : "IsActive" and "Operations" columns === #
        table_inst.change_column_location(Columns_webelement.column_1, Columns_webelement.column_2)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_is_active_operations = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move IsActive column to ID column =========================== #
        # === Switch column places : "IsActive" and "ID" columns === #
        table_inst.change_column_location(Columns_webelement.column_2, Columns_webelement.column_3)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_is_active_id = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move IsActive column to Role name column =========================== #
        # === Switch column places : "IsActive" and "Role name" columns === #
        table_inst.change_column_location(Columns_webelement.column_3, Columns_webelement.column_4)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_is_active_role_name = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move Operations column to ID column =========================== #
        # === Switch column places : "Operations" and "ID" columns === #
        table_inst.change_column_location(Columns_webelement.column_1, Columns_webelement.column_2)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_operations_id = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move Operations column to Role name column =========================== #
        # === Switch column places : "Operations" and "Role name" columns === #
        table_inst.change_column_location(Columns_webelement.column_2, Columns_webelement.column_3)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_operations_role_name = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # ============================= Move Operations column to IsActive column =========================== #
        # === Switch column places : "Operations" and "IsActive" columns === #
        table_inst.change_column_location(Columns_webelement.column_3, Columns_webelement.column_4)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_menu.webelement_of_1st_column_in_roles_table(), roles_menu.webelement_of_2nd_column_in_roles_table(),
                                  roles_menu.webelement_of_3rd_column_in_roles_table(), roles_menu.webelement_of_4th_column_in_roles_table())

        # read new order of headers from the Role table
        column_names_list_table_webelement = table_inst.get_all_headers_from_table_as_text(role_table_webelement)

        # Read column names from the Role table based on the index in DOM
        column_operations_is_active = roles_menu.names_of_all_columns_in_roles_table(column_names_list_table_webelement)

        # Test visibility of webelements on the page
        self.test_add_roles_page_elements()

        self.assertTrue(columns_default_state_bool, "Default column order in Role table is wrong")

        self.assertTrue(columns_id_role_name_bool, "Switching ID and Role name columns went wrong")
        self.assertTrue(column_id_isactive_bool, "Switching ID and IsActive columns went wrong")
        self.assertTrue(column_id_operations_bool, "Switching ID and Operations columns went wrong")

        self.assertTrue(column_role_name_is_active_bool, "Switching Role name and IsActive columns went wrong")
        self.assertTrue(column_role_name_operations_bool, "Switching Role name and Operations went wrong")
        self.assertTrue(column_role_name_id_bool, "Switching Role name and ID columns went wrong")

        self.assertTrue(column_is_active_operations, "Switching IsActive and Operations columns went wrong")
        self.assertTrue(column_is_active_id, "Switching IsActive and ID columns went wrong")
        self.assertTrue(column_is_active_role_name, "Switching IsActive and Role name columns went wrong")

        self.assertTrue(column_operations_id, "Switching Operations and ID columns went wrong")
        self.assertTrue(column_operations_role_name, "Switching Operations and Role name columns went wrong")
        self.assertTrue(column_operations_is_active, "Switching Operations and IsActive columns went wrong")

    # working only in Chrome , because drag_and_drop doesn't work with IE11
    def test_changing_position_of_columns_privileges_table(self):
        """Change position of columns in Privileges table"""
        # Instantiate User Role page
        roles_page_instance = UserRolesPage(self.driver)

        # Instance of TableFilter class for accessing column filter capabilities
        table_inst = TableFilter(self.driver)

        class Columns_webelement:
            column_1 = ""
            column_2 = ""
            column_3 = ""
            column_4 = ""
            column_5 = ""

            @classmethod
            def update(cls, value_1, value_2, value_3, value_4, value_5):
                cls.column_1 = value_1
                cls.column_2 = value_2
                cls.column_3 = value_3
                cls.column_4 = value_4
                cls.column_5 = value_5

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())
        # get the whole table webelement
        priv_table_webelement = roles_page_instance.get_the_table_element_privileges_full()

        # Read current headers from the Privilege table and save its names to list
        # in the order as it is appears in the HTML tree from top to down
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        # Read column names from the Privilege table based on the index in DOM,
        # compare it from the results from the whole table webelement
        columns_default_state_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move checkbox column to ID column =========================== #
        # === Switch column places : checkbox and "ID" columns === #
        table_inst.change_column_location(Columns_webelement.column_1, Columns_webelement.column_2)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        # Read column names from the Role table based on the index in DOM
        columns_checkbox_id_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move checkbox to "OperationName" column =========================== #
        # === Switch column places : checkbox to "OperationName" columns === #
        table_inst.change_column_location(Columns_webelement.column_2, Columns_webelement.column_3)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        # Read column names from the Role table based on the index in DOM
        columns_checkbox_operation_name_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move checkbox to "OperationUrl" column =========================== #
        # === Switch column places : checkbox and "OperationUrl"  columns === #
        table_inst.change_column_location(Columns_webelement.column_3, Columns_webelement.column_4)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        # Read column names from the Role table based on the index in DOM
        columns_checkbox_operation_url_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move checkbox column to IsActive column =========================== #
        # === Switch column places : checkbox and "IsActive" columns === #
        table_inst.change_column_location(Columns_webelement.column_4, Columns_webelement.column_5)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        # Read column names from the Role table based on the index in DOM
        columns_checkbox_isactive_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "ID" column to "OperationName" column =========================== #
        # === Switch column places : "ID" and "OperationName" columns === #
        table_inst.change_column_location(Columns_webelement.column_1, Columns_webelement.column_2)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        # Read column names from the Role table based on the index in DOM
        columns_id_operation_name_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "ID" column to "OperationUrl" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_2, Columns_webelement.column_3)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_id_operation_url_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "ID" column to "IsActive" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_3, Columns_webelement.column_4)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_id_isactive_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "ID" column to checkbox column =========================== #
        table_inst.change_column_location(Columns_webelement.column_4, Columns_webelement.column_5)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_id_checkbox_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move  "OperationName" to "OperationUrl" columns=========================== #
        table_inst.change_column_location(Columns_webelement.column_1, Columns_webelement.column_2)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_operation_name_operation_url_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "OperationName" to "IsActive" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_2, Columns_webelement.column_3)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_operation_name_is_active_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "OperationName" to checkbox column =========================== #
        table_inst.change_column_location(Columns_webelement.column_3, Columns_webelement.column_4)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_operation_name_checkbox_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "OperationName" to "ID" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_4, Columns_webelement.column_5)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_operation_name_id_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "OperationUrl" column to "IsActive" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_1, Columns_webelement.column_2)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        # Read column names from the Role table based on the index in DOM
        columns_url_operation_isactive_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "OperationUrl" column to checkbox column =========================== #
        table_inst.change_column_location(Columns_webelement.column_2, Columns_webelement.column_3)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_operation_url_checkbox_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "OperationUrl" column to "ID" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_3, Columns_webelement.column_4)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_operation_url_id_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "OperationUrl" to "OperationName" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_4, Columns_webelement.column_5)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_operation_url_operation_name_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "IsActive" to checkbox column =========================== #
        table_inst.change_column_location(Columns_webelement.column_1, Columns_webelement.column_2)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        # Read column names from the Role table based on the index in DOM
        columns_isactive_checkbox_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "IsActive" column to "ID" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_2, Columns_webelement.column_3)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_isactive_id_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "IsActive" column to "OperationName" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_3, Columns_webelement.column_4)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_isactive_operation_name_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)

        # ============================= Move "IsActive" to "OperationUrl" column =========================== #
        table_inst.change_column_location(Columns_webelement.column_4, Columns_webelement.column_5)

        # save the column names in the order as shown in GUI
        Columns_webelement.update(roles_page_instance.webelement_of_1st_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_2nd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_3rd_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_4th_column_in_privilege_table(),
                                  roles_page_instance.webelement_of_5th_column_in_privilege_table())

        # read new order of headers from the Role table
        new_order_of_column_names_list = table_inst.get_all_headers_from_table_as_text(priv_table_webelement)

        columns_isactive_operation_url_bool = roles_page_instance.names_of_all_columns_in_privilege_table(new_order_of_column_names_list)


        # Test visibility of webelements on the page
        self.test_add_roles_page_elements()

        self.assertTrue(columns_default_state_bool, "Default column order in Role table is wrong")

        self.assertTrue(columns_checkbox_id_bool, "Switching checkbox and ID columns went wrong")
        self.assertTrue(columns_checkbox_operation_name_bool, "Switching checkbox and OperationName columns went wrong")
        self.assertTrue(columns_checkbox_operation_url_bool, "Switching checkbox and OperationUrl columns went wrong")
        self.assertTrue(columns_checkbox_isactive_bool, "Switching checkbox and IsActive columns went wrong")

        self.assertTrue(columns_id_operation_name_bool, "Switching ID and OperationName columns went wrong")
        self.assertTrue(columns_id_operation_url_bool, "Switching ID and OperationUrl went wrong")
        self.assertTrue(columns_id_isactive_bool, "Switching ID and IsActive columns went wrong")
        self.assertTrue(columns_id_checkbox_bool, "Switching ID and checkbox columns went wrong")

        self.assertTrue(columns_operation_name_operation_url_bool, "Switching OperationName and OperationUrl columns went wrong")
        self.assertTrue(columns_operation_name_is_active_bool, "Switching OperationName and IsActive columns went wrong")
        self.assertTrue(columns_operation_name_checkbox_bool, "Switching OperationName and checkbox columns went wrong")
        self.assertTrue(columns_operation_name_id_bool, "Switching OperationName and ID columns went wrong")

        self.assertTrue(columns_url_operation_isactive_bool, "Switching OperationUrl and IsActive columns went wrong")
        self.assertTrue(columns_operation_url_checkbox_bool, "Switching OperationUrl and checkbox columns went wrong")
        self.assertTrue(columns_operation_url_id_bool, "Switching OperationUrl and ID columns went wrong")
        self.assertTrue(columns_operation_url_operation_name_bool, "Switching OperationUrl and OperationName columns went wrong")

        self.assertTrue(columns_isactive_checkbox_bool, "Switching IsActive and checkbox columns went wrong")
        self.assertTrue(columns_isactive_id_bool, "Switching IsActive and ID columns went wrong")
        self.assertTrue(columns_isactive_operation_name_bool, "Switching IsActive and OperationName columns went wrong")
        self.assertTrue(columns_isactive_operation_url_bool, "Switching IsActive and OperationUrl columns went wrong")

    def test_attaching_detaching_roles_from_user(self):
        """Attaching of role to the user , then deleting the role and verifying that the role was really detached from user"""
        # Add new role in Roles page
        role1_parameters = PromoRequest(self.driver).add_role_request("true", self.role1)
        self.driver.refresh()

        home_page = HomePage(self.driver)
        # Click Users tab
        home_page.click_users_menuitem()
        time.sleep(1)

        user_page_instance = UsersPage(self.driver)

        # Instance of Table class
        user_table_inst = Table(self.driver, user_page_instance.get_webelement_user_table())
        # save all rows from Users table
        table_cells_webelement = user_table_inst.get_all_cells_element()
        # check if our test user is present in the Users table or not, if yes then no need to create the same user
        if user_table_inst.find_web_element_text_from_all_cells(table_cells_webelement,
                                                                [self.login, self.email, self.user_name]):
            # click on the user name
            webelement_of_user = user_page_instance.click_on_the_user_by_name(self.login)
            # scroll to the user name
            self.driver.execute_script("return arguments[0].scrollIntoView(true);", webelement_of_user)

        else:
            # if user is not present in the Users table , create a new test user
            PromoRequest(self.driver).add_user_request(self.user_id, self.login, self.email,
                                                            self.auth_type, self.domain, self.is_active, self.user_name)
            # click on the user name
            user_page_instance.click_on_the_user_by_name(self.user_name)

        # Instance of Table with roles located in the Users page
        roles_table_in_user_page_inst = Table(self.driver, user_page_instance.get_webelement_role_table_in_user_page())
        # get all rows from the Roles table in the Users page
        roles_table_in_user_page_inst.get_all_cells_element()
        # all rows from the Users table
        user_page_instance.click_on_the_user_by_name(self.role1)
        # Press "Save changes" button in the Users page
        save_changes_button = user_page_instance.get_save_changes_button_user_page()
        save_changes_button.click()
        # Press Roles tab / go back to the Roles page
        home_page.click_roles_menuitem()
        time.sleep(1)
        # Press Roles tab / go back to the Roles page
        role_id = role1_parameters[0]
        role_isactive = role1_parameters[2]
        role_name = role1_parameters[1]
        # Delete the role
        PromoRequest(self.driver).delete_role_request(role_id, role_isactive, role_name)
        # Press Users tab / go back to the Users page
        home_page.click_users_menuitem()
        time.sleep(1)
        # Verify that the role was deleted from the Users page as well
        self.assertEqual(user_page_instance.click_on_the_user_by_name(self.role1), "role not found")

    def test_edit_role_save_changes(self):
        """Editing existing Role and verifying if results were saved successfully"""
        role2_parameters = PromoRequest(self.driver).add_role_request("true", self.role2)
        self.driver.refresh()
        # Save role's parameters returned from the server after sending new role request
        role_id = role2_parameters[0]
        role_isactive = role2_parameters[2]
        role_name = role2_parameters[1]

        roles_page_instance = UserRolesPage(self.driver)
        # Add new role pop up window is the same as Edit pop up window
        add_roles_pop_up = AddRolePopUp(self.driver)
        # Press Edit role button
        roles_page_instance.edit_role_by_id(role_id)
        # Enter new role name, press "IsActive" button, and press "Update"/Save button
        add_roles_pop_up.edit_role(self.role_name_yes, 'yes')

        # Verify that the new role appears in the DB and in the grid, and that the roles' parameters match
        self.assertTrue(roles_page_instance.verify_new_role_grid_vs_db(self.role_name_yes),
                                                        "The edited role data doesn't correspond to the DB data")
        # delete the modified role
        PromoRequest(self.driver).delete_role_request(role_id, role_isactive, role_name)

    def test_make_changes_and_dont_cancel_them(self):
        """Checking few privileges and navigating to the page with users, if not canceled, the changes should remain on the Roles page"""
        role3_parameters = PromoRequest(self.driver).add_role_request("true", self.role3)
        self.driver.refresh()
        # Save role's parameters returned from the server after sending new role request
        role_id = role3_parameters[0]
        role_isactive = role3_parameters[2]
        role_name = role3_parameters[1]

        roles_page_instance = UserRolesPage(self.driver)

        # Click with the mouse on the Roles row in the Roles table
        roles_page_instance.click_on_the_role(role_name)
        # ids of privilege (random ids)
        ids = [1, 42, 73]
        # check 3 random checkboxes in privileges table
        roles_page_instance.click_on_the_privilege_by_ids(ids)

        home_page = HomePage(self.driver)
        # press Users tab in order to switch to another page
        home_page.click_users_menuitem()

        dialog_window_instance = UnsavedDataDialog(self.driver)

        # test all webelements of the pop-up window
        self.assertTrue(dialog_window_instance.unsave_changes_dialog_window_test(), "General test of dialog window 'Unsaved data' has failed")

        # when dialog window about unsaved data appears, on question if user want to save changes press "Cancel" button
        dialog_window_instance.save_changes_click_cancel()

        ids_found = roles_page_instance.verify_privilege_checkboxes_state(ids)
        # verify that checkboxes checked/changes are saved
        self.assertTrue(ids_found[0], "Checkbox " + str(ids[0]) + " is not checked, but it should be checked")
        self.assertTrue(ids_found[1], "Checkbox " + str(ids[1]) + " is not checked, but it should be checked")
        self.assertTrue(ids_found[2], "Checkbox " + str(ids[2]) + " is not checked, but it should be checked")

        PromoRequest(self.driver).delete_role_request(role_id, role_isactive, role_name)

    def test_make_changes_and_cancel_them(self):
        """Checking few privileges and navigating to the page with users, if canceled, the changes should disappear on the Roles page"""
        role4_parameters = PromoRequest(self.driver).add_role_request("true", self.role4)
        self.driver.refresh()
        # Save role's parameters returned from the server after sending new role request
        role_id = role4_parameters[0]
        role_isactive = role4_parameters[2]
        role_name = role4_parameters[1]

        roles_page_instance = UserRolesPage(self.driver)

        # Click with the mouse on the Roles row in the Roles table
        roles_page_instance.click_on_the_role(role_name)
        # ids of privilege (random ids)
        ids = [13, 36, 67]
        # check 3 random checkboxes in privileges table
        roles_page_instance.click_on_the_privilege_by_ids(ids)

        home_page = HomePage(self.driver)
        # press Users tab in order to switch to another page
        home_page.click_users_menuitem()

        dialog_window_instance = UnsavedDataDialog(self.driver)

        # test all webelements of the pop-up window
        self.assertTrue(dialog_window_instance.unsave_changes_dialog_window_test(), "General test of dialog window 'Unsaved data' has failed")

        # when dialog window about unsaved data appears, on question if user want to save changes press "OK" button
        dialog_window_instance.save_changes_click_ok()
        # press Roles tab in order to switch back to the Roles page
        home_page.click_roles_menuitem()

        # click on the role
        roles_page_instance.click_on_the_role(role_name)

        ids_found = roles_page_instance.verify_privilege_checkboxes_state(ids)
        # verify that checkboxes unchecked/changes were not saved
        self.assertFalse(ids_found[0], "Checkbox " + str(ids[0]) + " is checked, but it shouldn't be checked")
        self.assertFalse(ids_found[1], "Checkbox " + str(ids[1]) + " is checked, but it shouldn't be checked")
        self.assertFalse(ids_found[2], "Checkbox " + str(ids[2]) + " is checked, but it shouldn't be checked")

        PromoRequest(self.driver).delete_role_request(role_id, role_isactive, role_name)














