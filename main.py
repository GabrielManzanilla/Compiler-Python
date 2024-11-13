

import config
from append_table import fill_table_lexemas, fill_table_errors, fill_table_triplo
from admin_jumps import add_jumps_in_triplo
from parse_ast import evaluate


def compile(code, table_lexemas, table_errors, triplo_table):
    config.lexemas.clear() #limpiar la tabla
    config.errors.clear() #limpiar la tabla
    config.triplo.clear() #limpiar la tabla


    evaluate(code) #evaluar el codigo

    fill_table_lexemas(table_lexemas, config.lexemas)
    fill_table_errors(table_errors, config.errors)
    fill_table_triplo(triplo_table, config.triplo)


