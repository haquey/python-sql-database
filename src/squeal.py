from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results

# USED TO SPLICE THE WHERE CLAUSE
BEFORE_OPERATOR_INDEX = 0
AFTER_OPERATOR_INDEX = 1
# USED TO INSERT TABLE OBJECTS FOUND IN A LIST INTO A FUNCTION
FIRST_TABLE_INDEX = 0
SECOND_TABLE_INDEX = 1
# USED TO SPLICE THE QUERY INTO MEANINGFUL PARTS TO PROCESS
COLUMN_SELECTION_INDEX = 1
TABLE_NAME_SELECTION_INDEX = 3
WHERE_CLAUSE_INDEX = 5


def num_rows(table_obj):
    '''(Table) -> int

    Given a table object, determine the number of rows found within the table
    using its dictionary representation.

    REQ: Each column within the table should have the same number of rows

    >>> table = Table()
    >>> table.set_dict({'a': ['THIS','IS','A','TEST'],
                        'b': ['There','are', 'four', 'rows']})
    >>> num_rows(table)
    4

    >>> table = Table()
    >>> table.set_dict({1 : [], 2 : []})
    >>> num_rows(table)
    0
    '''
    num_rows = table_obj.num_rows()
    return num_rows


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.

    REQ: Table dictionary must be proper format {column_title: list of str}
    REQ: All columns should have same number of rows

    >>> table = Table()
    >>> table.set_dict({'THIS': ['THIS','IS','A','TEST'],
                        'IS': ['There', 'are', 'four', 'rows'],
                        'A': ['There', 'are', 'four', 'rows'],
                        'TEST': ['IT', 'works', 'it', 'WORKS!']})
    >>> print_csv(table)
    THIS,TEST,A,IS
    THIS,IT,There,There
    IS,works,are,are
    A,it,four,four
    TEST,WORKS!,rows,rows

    >>> table.set_dict({'THIS': [], 'WORKS': [], 'AS': [], 'WELL': []})
    >>> print_csv(table)
    WELL,THIS,AS,WORKS
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = num_rows(table)
    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))


def where_equals_clause(clause, table_name):
    '''(str, Table) -> Table
    Given a Table object and a clause countaining two column titles and
    a value, return a table that is joined at the indicated columns or
    specified value where they are equal.

    REQ: Specified columns must exist within the table
    REQ: Column titles must exist within the tables
    '''
    # Break up the clause into the column titles or value
    constraints = clause.split('=')
    before_operator = constraints[BEFORE_OPERATOR_INDEX]
    after_operator = constraints[AFTER_OPERATOR_INDEX]
    # If the token after the operator is a value:
    if after_operator not in table_name.get_headers():
        table_name.perform_where_equals_value(before_operator, after_operator)
    # If the token after the operator is a column title
    else:
        table_name.perform_where_equals(before_operator, after_operator)
    return table_name


def where_more_than_clause(clause, table_name):
    '''(str, Table) -> Table

    Given a Table object and a clause countaining two column titles and
    a value, return a table that is joined at the indicated columns or
    specified value where the first constraint is more than the second.

    REQ: Specified columns must exist within the table
    REQ: Column titles must exist within the tables
    '''
    # Break up the clause into the column titles or value
    constraints = clause.split('>')
    before_operator = constraints[BEFORE_OPERATOR_INDEX]
    after_operator = constraints[AFTER_OPERATOR_INDEX]
    # If the token after the operator is a value:
    if after_operator not in table_name.get_headers():
        table_name.perform_where_more_than_value(before_operator,
                                                 after_operator)
    # If the token after the operator is a column title
    else:
        table_name.perform_where_more_than(before_operator, after_operator)
    return table_name


def where_clause(table_name, where_query):
    '''(Table, list of str) -> Table

    Given a Table object and a where clause, interpret the where clause to
    produce the appropriate corresponding table that is joined according to the
    instructions of the where clause.

    REQ: Where clauses must have proper syntax (column=column,column='value',
         column>column,column>'value')
    REQ: Column titles must exist within the tables
    '''
    for clause in where_query:
        # Look for an '=' operator in the clause and run the appropriate task
        if '=' in clause:
            table_name = where_equals_clause(clause, table_name)
        # Look for a '>' operator in the clause and run the appropriate task
        elif '>' in clause:
            table_name = where_more_than_clause(clause, table_name)

    return table_name


def process_two_tables(database, table_names):
    '''(Database, list of str) -> Table

    Given a list containing two table names that exist within the inserted
    Database object, return the cartesian product of the two tables.

    REQ: Table names must correspond to existing table names in the database
    REQ: List should contain at least two elements
    '''
    table_list = []
    for name in table_names:
        # Find the Table objects that correspond with the table names
        table_list.append(database.db_table(name))
    # Return the cartesian product of the two table objects in the list
    return cartesian_product(table_list[FIRST_TABLE_INDEX],
                             table_list[SECOND_TABLE_INDEX])


def run_query(database_obj, str_query):
    '''(Database, str) -> Table

    Given a database object and a query, interpret the query to perform
    the appropriate functions to produce a table corresponding to the query's
    instructions.

    REQ: The input query must have proper syntax
    REQ: Database must be a valid database containing dictionary in
         proper format {file_name : Table}
    '''
    # Break up the input query into its meaningful tokens
    input_query = str_query.split(' ', 5)
    column_names = input_query[COLUMN_SELECTION_INDEX].split(',')
    table_names = input_query[TABLE_NAME_SELECTION_INDEX].split(',')

    # Perform the appropraite functions depending on the number of tables
    if len(table_names) == 1:
        res_table = database_obj.db_table(table_names[FIRST_TABLE_INDEX])

    elif len(table_names) == 2:
        res_table = process_two_tables(database_obj, table_names)

    elif len(table_names) > 2:
        table_list = []
        for name in table_names:
            table_list.append(database_obj.db_table(name))

        res_table = cartesian_product(table_list[FIRST_TABLE_INDEX],
                                      table_list[SECOND_TABLE_INDEX])
        for i in range(2, len(table_list) - 1):
            res_table = cartesion_product(res_table, table_list[i])
    # Interpret the where clause of the query if it exists
    if len(input_query) > 4:
        where_query = input_query[WHERE_CLAUSE_INDEX].split(',')
        res_table = where_clause(res_table, where_query)

    # Interpret the column selection clause of the query if it exists
    if column_names != ['*']:
        res_table.select_columns(column_names)

    return res_table


def cartesian_product(table1, table2):
    '''(Table, Table) -> Table

    Given two table objects, produce a new table object that is the
    cartesian product of the two that were inserted.

    REQ: Both tables are properly formatted
    REQ: Both tables have contents

    >>> new_table = Table()
    >>> new_table2 = Table()
    >>> new_table.set_dict({'8': ['a', 'b', 'c'], '9': ['z', 'x', 'y'],
                            '10': ['%', '&', '!']})
    >>> new_table2.set_dict({'CSC': ['Py', 'th', 'on'],
                             'A08': ['y', 'e', 's']})
    >>> res_table = cartesian_product(new_table, new_table2)
    >>> res_table.get_dict()
    {'CSC': ['Py', 'th', 'on', 'Py', 'th', 'on', 'Py', 'th', 'on'],
     'A08': ['y', 'e', 's', 'y', 'e', 's', 'y', 'e', 's'],
     '10': ['%', '%', '%', '&', '&', '&', '!', '!', '!'],
     '9': ['z', 'z', 'z', 'x', 'x', 'x', 'y', 'y', 'y'],
     '8': ['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'c']}

     >>> new_table.set_dict({'o': ['Y', 'a', 'Y']})
     >>> new_table2.set_dict({'a': ['HE', 'LL', 'o'], 'to': ['Y', 'O', 'U']})
     >>> res_table = cartesian_product(new_table, new_table2)
     >>> res_table.get_dict()
     {'a': ['HE', 'LL', 'o', 'HE', 'LL', 'o', 'HE', 'LL', 'o'],
      'o': ['Y', 'Y', 'Y', 'a', 'a', 'a', 'Y', 'Y', 'Y'],
      'to': ['Y', 'O', 'U', 'Y', 'O', 'U', 'Y', 'O', 'U']}
    '''
    new_table = Table()
    # Get the length of the tables/number of rows
    len_table1 = table1.num_rows()
    len_table2 = table2.num_rows()
    # Multiply the first table's individual elements by length of the second
    for header in table1.table_dict:
        rows = []
        for i in range(len_table1):
            rows += [table1.table_dict[header][i]]*len_table2
        # Input the information into the new table object
        new_table.set_headers_and_contents(header, rows)
    # Multiply the the second table by the length of the first
    for header in table2.table_dict:
        rows2 = table2.table_dict[header]*len_table1
        # Input the information into the new table object
        new_table.set_headers_and_contents(header, rows2)

    return new_table

if(__name__ == "__main__"):
    query = input("Enter a SQuEaL query, or a blank line to exit:")

    while query != '':
        database = read_database()
        process_database_and_query = run_query(database, query)
        print_csv(process_database_and_query)
        query = input("Enter a SQuEaL query, or a blank line to exit:")
