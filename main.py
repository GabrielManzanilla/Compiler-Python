import time
from asiggnment_variables import *
import config
from append_table import fill_table_lexemas, fill_table_errors



def compile(code, table_lexemas, table_errors):
    table_lexemas.clear()
    table_errors.clear()
    code_lines=code.split("\n")
    print(code_lines)
    for index, line in enumerate(code_lines):
        identify_operation(line, index+1)
        
    fill_table_lexemas(table_lexemas, config.lexemas)
    fill_table_errors(table_errors, config.errors)


