
from asiggnment_variables import *
import config
from append_table import fill_table_lexemas, fill_table_errors, fill_table_triplo
from contoler import eval_expr


def compile(code, table_lexemas, table_errors, triplo_table):
    config.lexemas.clear() #limpiar la tabla
    config.errors.clear() #limpiar la tabla
    code_lines=code.split("\n")

    for index, line in enumerate(code_lines):
        identify_operation(line, index+1)
        eval_expr(line)
    print(config.triplo)
    fill_table_lexemas(table_lexemas, config.lexemas)
    fill_table_errors(table_errors, config.errors)
    fill_table_triplo(triplo_table, config.triplo)


