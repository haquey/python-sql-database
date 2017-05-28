class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self):
        '''(Table) -> NoneType

        Initiliaze this table with a dictionary representing the
        table itself
        '''
        self.table_dict = {}

    def dict_info(self, headers, column_contents):
        '''(Table, list of str, list of str) -> NoneType

        Given the column titles/headers and their contents, edit the
        information in the object Table's dictionary representing
        the table itself.
        '''
        for i in range(len(headers)):
            # First create the headers within the table without any information
            # within the rows
            column_title = headers[i]
            self.table_dict[column_title] = []
            # Fill in the rows with the appropriate information corresponding
            # to the created headers
            for element in column_contents:
                self.table_dict[column_title].append(element[i].strip())

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        self.table_dict = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self.table_dict

    def __str__(self):
        return str(self.table_dict)

    def set_headers_and_contents(self, header, rows):
        '''(Table, list of str, list of str) -> NoneType
        Given a the table's header and row information, insert the header and
        the correspondiing information within the rows into the dictionary
        representation of the table.
        '''
        self.table_dict[header] = rows

    def get_headers(self):
        '''(Table) -> NoneType

        Obtain a list of the headers/column titles within the table. These
        are the key values within the dictionary representation of the table.
        '''
        headers = self.table_dict.keys()
        return list(headers)

    def select_columns(self, header):
        '''(Table, list of str) -> NoneType

        Given a list of headers/column titles, edit the information within the
        dictionary such that only the contents within the specified
        headers/column titles remain.
        '''
        column_contents = {}
        for names in header:
            # Keep only the information within the specified headers
            column_contents[names] = self.table_dict[names]
        self.table_dict = column_contents

    def perform_where_equals(self, before_operator, after_operator):
        '''(Table, str, str) -> NoneType

        Given two column titles/headers that appear before and after the
        'equals' operator, edit the Table's dictionary such that it joins where
        the columns' elements are equal.
        '''
        joined_table = {}
        column_titles = self.get_headers()
        current_table = self.table_dict
        # Create a new table to hold the values where the columns are equal
        for title in column_titles:
            joined_table[title] = []
        # Populate the table where values within the specified columns equal
        for i in range(self.num_rows()):
            if ((current_table[before_operator][i]) == (current_table
                                                        [after_operator][i])):
                for title in column_titles:
                    joined_table[title].append(current_table[title][i])
        # Fix the original table to the newly joined one
        self.table_dict = joined_table

    def perform_where_equals_value(self, column_title, value):
        '''(Table, str, str) -> NoneType

        Given a column title/header and a specified value that appear before
        and after the 'equals' operator, edit the Table's dictionary such that
        it joins where the specified the column's elements are equal to the
        value.
        '''
        joined_table = {}
        column_titles = self.get_headers()
        current_table = self.table_dict
        # Get rid of the quotation marks in case the specified value is
        # something like 'Alice' so that it is identified within the table
        FIRST_CHARACTER_INDEX = 0
        SECOND_CHARACTER_INDEX = 1
        SECOND_LAST_CHARACTER_INDEX = -1
        if value[FIRST_CHARACTER_INDEX] == "'":
            value = value[SECOND_CHARACTER_INDEX:SECOND_LAST_CHARACTER_INDEX]
        # Create a new table to hold the values where the column=value
        for title in column_titles:
            joined_table[title] = []
        # Populate the table where the specified value equals the column values
        for i in range(self.num_rows()):
            if (current_table[column_title][i]) == value:
                for title in column_titles:
                    joined_table[title].append(current_table[title][i])
        # Fix the original table to the newly joined one
        self.table_dict = joined_table

    def perform_where_more_than(self, before_operator, after_operator):
        '''(Table, str, str) -> NoneType

        Given two column titles/header that appear before and after the
        'more than' operator, edit the Table's dictionary such that it joins
        where the first specified column's elements are more
        than the other.
        '''
        joined_table = {}
        column_titles = self.get_headers()
        current_table = self.table_dict
        # Create a new table to hold the specified values
        for title in column_titles:
            joined_table[title] = []
        # Create a new table to hold the values where the element of the first
        # column is more than the second column
        for i in range(self.num_rows()):
            if ((current_table[before_operator][i]) > (current_table
                                                       [after_operator][i])):
                for title in column_titles:
                    joined_table[title].append(current_table[title][i])
        # Populate the table with the specified values
        self.table_dict = joined_table

    def perform_where_more_than_value(self, column_title, value):
        '''(Table, str, str) -> NoneType

        Given a column title/header and a specified value that appear before
        and after the 'more than' operator, edit the Table's dictionary such
        that it joins where the first specified column's elements are more
        than the other.
        '''
        joined_table = {}
        column_titles = self.get_headers()
        current_table = self.table_dict
        # Get rid of the quotation marks in case the specified value is
        # something like 'What if' so that it is identified within the table
        FIRST_CHARACTER_INDEX = 0
        SECOND_CHARACTER_INDEX = 1
        SECOND_LAST_CHARACTER_INDEX = -1
        if value[FIRST_CHARACTER_INDEX] == "'":
            value = value[SECOND_CHARACTER_INDEX:SECOND_LAST_CHARACTER_INDEX]
        # Create a new table to hold the specified values
        for title in column_titles:
            joined_table[title] = []
        # Create a new table to hold the values where the element of the first
        # column is more than the specified value
        for i in range(self.num_rows()):
            if (current_table[column_title][i]) > value:
                for title in column_titles:
                    joined_table[title].append(current_table[title][i])
        # Populate the table with the specified values
        self.table_dict = joined_table

    def num_rows(self):
        '''(Table) -> int

        Obtain the number of rows found in the table
        '''
        headers = self.get_headers()
        for name in headers:
            # The number of rows corresponds with the number of elements in
            # the lists within the dictionary representation of the table
            row_count = len(self.table_dict[name])
        return row_count


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self):
        '''(Database) -> NoneType

        Initiliaze this table with a dictionary representing the
        database itself.
        '''
        self.database_dict = {}

    def database_info(self, file_name, table_obj):
        '''(Table, list of str, list of str) -> NoneType

        Given the column titles/headers and their contents, edit the
        information in the object Table's dictionary representing
        the table itself.
        '''
        self.database_dict[file_name] = table_obj

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self.database_dict = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self.database_dict

    def db_table(self, table_name):
        '''(Database) -> Table

        Retrieve the corresponding Table object within the database given
        the Table object's name.
        '''
        return self.database_dict[table_name]
