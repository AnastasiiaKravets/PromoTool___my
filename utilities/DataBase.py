import pymssql
from utilities import user_info


def get_connection_parameters():
    return dict(
        server='s-kv-center-s70',
        database='PromoToolGlobus',
        user=user_info._data_base_user,
        password=user_info._data_base_password
    )


def escape_apostrophes_for_sql_query(input_string):
    # check if the input is really a string
    if not isinstance(input_string, str):
        input_string = str(input_string)

    # if there were apostrophes found, split the original string, between apostrophes, remove all apostrophes,
    # and after each substring insert 2 apostrophes, which will be the same as to insert 1 apostrophe near existing one

    # if no apostrophe located return the string as it is
    if len(input_string) > 0 and input_string.find("'") < 0:
        return input_string
    # if at least one apostrophe located start splitting the string near each apostrophe
    elif len(input_string) > 0 and input_string.find("'") >= 0:
        # temp_res should contain all substrings divided by apostrophes
        temp_res = input_string.split("'")
        count = 0  # count substrings
        substr = ""
        for current_substr in temp_res:
            # if apostrophe was located at the beginning , just add 2 apostrophes at the beginning
            if count == 0 and len(current_substr) == 0:
                substr = "'" + "'" + current_substr
            # if last substring was reached , attach it to the rest of the strings
            elif count >= len(temp_res) - 1:
                substr = substr + current_substr
            # attach the apostrophe after current substring (there are 2 apostrophes,
            # because when the string is split the original apostrophe was deleted)
            else:
                substr = substr + current_substr + "'" + "'"
            count = count + 1
        return substr
    # just in unpredictable case - return the string unchanged
    else:
        return input_string


class DataBase:
    def __init__(self, kwargs):
        try:
            self.connection = pymssql.connect(**kwargs)
            self.cursor = self.connection.cursor()
        except Exception as e:
            ('____EXCEPTION WITH DATA BASE____ ' + str(e))

    def __del__(self):
        try:
            self.connection.close()
        except AttributeError:
            print('DataBase connection was not closed')

    def select(self, select_string):

        self.cursor.execute(select_string)
        row_dict = {}
        inx = 0
        for row in self.cursor:
            if len(row) > 0:
                row_dict[inx] = row
                inx = inx + 1

        return row_dict

    def execute(self, string):
        self.cursor.execute(string)
        self.connection.commit()

    def select_in_list(self, select_string):
        """
        :param select_string: 
        :return: list of tuples
        """
        self.cursor.execute(select_string)
        list = []
        for row in self.cursor:
            list.append(row)
        return list

    def get_last_id(self, table):
        return self.select_in_list(
            'SELECT TOP 1 [Id] FROM {0} ORDER BY [Id] DESC'.format(table))[0][0]

    def get_id(self, select_string):
        result = self.select_in_list(select_string)
        try:
            return result[0][0]
        except:
            return None

