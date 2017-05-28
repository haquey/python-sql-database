# Functions for reading tables and databases

import glob
from database import *

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.

# A database is a dict of {str:table},
# where the keys are table names and values are the tables.

# YOU DON'T NEED TO KEEP THE FOLLOWING CODE IN YOUR OWN SUBMISSION
# IT IS JUST HERE TO DEMONSTRATE HOW THE glob CLASS WORKS. IN FACT
# YOU SHOULD DELETE THE PRINT STATEMENT BEFORE SUBMITTING

# Write the read_table and read_database functions below


def read_table(file_name):
    '''(str) -> Table

    Given the name of a table file that is found within the same directory,
    read the file's contents and produce a corresponding table object.

    REQ: File given must be in the same directory
    REQ: File given mus be a .csv file
    REQ: String input for the file name must be in the form "___.csv"
    '''
    # Obtain a list of the contents of the file
    open_file = open(file_name, "r")
    all_lines = open_file.readlines()
    open_file.close()
    info_dict = {}
    all_lines_fixed = []

    # Make a new list with all the contents of the file appropriately split
    for each_line in all_lines:
        all_lines_fixed.append(each_line.strip().split(','))
    # Seperate the information regarding column titles and their content
    HEADER_INDEX = 0
    headers = all_lines_fixed[HEADER_INDEX]
    del all_lines_fixed[HEADER_INDEX]
    # Input the column titles/headers and row information into a new Table
    res_table = Table()
    res_table.dict_info(headers, all_lines_fixed)

    return res_table


def read_database():
    '''() -> Database

    Processes all files within the directory with a .csv extension and creates
    a database object representing all the processed files.

    REQ: Files read must be in the same directory
    REQ: Files read must .csv files
    '''
    database_obj = Database()
    # List the names of all th eligible files within the directory
    file_list = glob.glob('*.csv')
    for file_name in file_list:
        # Create a table object for each table name and insert the information
        # into the database object
        just_name = file_name[:-4]
        database_obj.database_info(just_name, read_table(file_name))

    return database_obj
