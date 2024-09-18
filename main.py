
from asiggnment_variables import *
import config
from append_table import fill_table_lexemas, fill_table_errors



def compile(code, table_lexemas, table_errors):
    config.lexemas.clear() #limpiar la tabla
    config.errors.clear() #limpiar la tabla
    code_lines=code.split("\n")

    for index, line in enumerate(code_lines):
        identify_operation(line, index+1)
        
    fill_table_lexemas(table_lexemas, config.lexemas)
    fill_table_errors(table_errors, config.errors)


