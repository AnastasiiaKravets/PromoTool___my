from selenium.webdriver.support.wait import WebDriverWait

_tuple = (' ', '_', '-', ',', ';', ':', '!', '?', '.', "'", '"', '(', ')', '[', ']', '*', '{', '}', '@', '*', '/',
          '\\', '&', '#', '%', '`', '^', '+', '>', '=', '>', '|', '~', '$', '0', '1', '2', '3', '4', '5', '6',
          '7', '8', '9', 'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h',
          'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r',
          'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z')


def compare_two_characters(character_1, character_2):
    """
    Compare 2 characters according to Kendo's UI algorithm .
    :param character_1, character_2
    (basically character in python is an unchangeable  string of length 1)
    :return: if character_1 is bigger than character_2 then return 1, else return 2, if they are the same return 3
    """
    if _tuple.index(character_1) > _tuple.index(character_2):
        return 1
    elif _tuple.index(character_1) < _tuple.index(character_2):
        return 2
    elif _tuple.index(character_1) == _tuple.index(character_2):
        return 3


def compare_two_strings(string_1, string_2, isInt):
    """
    Compare 2 strings according to Kendo's UI algorithm .
    :param string_1, string_2: each string contains characters , for instance, we firstly compare
            characters at index 0 of both strings , if they are equal we compare characters at index 1 and so on
            isInt = True indicates we want to compare two integers , then the comparison is straightforward
    :return: if string_1 is bigger than string_2 then return 1, else return 2, if they are the same return 3
    """
    if isInt:
        if string_1 > string_2:
            return 1
        elif string_1 < string_2:
            return 2
        elif string_1 == string_2:
            return 3
    else:
        inx_1 = 0
        inx_2 = 0
        # make sure we will not access non-existing index in both strings
        while inx_1 < len(string_1) and inx_2 < len(string_2):

            # compare characters from both strings at the same index location (for instance, string_1[0] vs string_2[0]
            # if they are not the same, then pass them to "compare_two_characters" method , which will define the
            # order of two characters according to Kendo's rules, which in turn will define the order of our 2 strings.
            # If, for example, character_1 > character_2 then automatically string_1 > string_2
            if compare_two_characters(string_1[inx_1], string_2[inx_2]) == 1:
                return 1
            elif compare_two_characters(string_1[inx_1], string_2[inx_2]) == 2:
                return 2
            elif compare_two_characters(string_1[inx_1], string_2[inx_2]) == 3:
                inx_1 = inx_1 + 1
                inx_2 = inx_2 + 1
        # if 2 strings has equal characters, but one string is longer than the other , then
        # the longer string is bigger than the shorter one
        if inx_1 == len(string_1) and len(string_1) < len(string_2):
            return 2
        elif inx_2 == len(string_2) and len(string_1) > len(string_2):
            return 1
        # if 2 strings are identical, meaning all of their characters are equal and their lengths are equal too,
        # then return 3
        elif len(string_1) == len(string_2) and inx_1 == len(string_1) and inx_2 == len(string_2):
            return 3

class KendoSorting:
    def __init__(self, driver, list_of_rows_web, column_index):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        self.list_from_grid = []
        for row in list_of_rows_web:
            if len(row) > 0:
                temp_string = (row[column_index].text).lower()
                self.list_from_grid.append(temp_string)

    def sort_strings_ascending(self, isInt):
        """
        Sort the list of strings according to Kendo's UI algorithm ascending, by using simple bubble sort
        :param list_of_string: list with strings from the UI table
        :return: sorted list of strings according to Kendo's algorithm
        """
        if isInt:
            list_kendo_sorted = [int(i) for i in self.list_from_grid]
        else:
            list_kendo_sorted = [str(i) for i in self.list_from_grid]

        length = len(list_kendo_sorted) - 1
        sorted_columns = False

        while not sorted_columns:
            sorted_columns = True
            for i in range(length):
                string_1 = list_kendo_sorted[i]
                string_2 = list_kendo_sorted[i + 1]
                # if list_from_grid[i] > list_of_strings[i+1] => string_1 > string_2
                if compare_two_strings(string_1, string_2, isInt) == 1:
                    sorted_columns = False
                    list_kendo_sorted[i + 1] = string_1
                    list_kendo_sorted[i] = string_2

        # convert ints back to strings
        if isInt:
            list_kendo_sorted = [str(i) for i in self.list_from_grid]

        for inx in range(len(list_kendo_sorted)):
            if list_kendo_sorted[inx] != self.list_from_grid[inx]:
                return False
        return True

    def sort_strings_descending(self, isInt):
        """
        Sort the list of strings according to Kendo's UI algorithm descending, by using simple bubble sort
        :param list_of_string: list with strings from the UI table
        :return: sorted list of strings according to Kendo's algorithm
        """
        if isInt:
            list_of_elements = [int(i) for i in self.list_from_grid]
        else:
            list_of_elements = [str(i) for i in self.list_from_grid]

        length = len(list_of_elements) - 1
        sorted_columns = False

        while not sorted_columns:
            sorted_columns = True
            for i in range(length):
                string_1 = list_of_elements[i]
                string_2 = list_of_elements[i+1]
                # if list_of_strings[i] < list_of_strings[i+1] <= string_1 > string_2
                if compare_two_strings(string_1, string_2, isInt) == 2:
                    sorted_columns = False
                    list_of_elements[i+1] = string_1
                    list_of_elements[i] = string_2

        # convert ints back to strings
        if isInt:
            list_of_elements = [str(i) for i in self.list_from_grid]

        for inx in range(len(list_of_elements)):
            if list_of_elements[inx] != self.list_from_grid[inx]:
                return False
        return True
