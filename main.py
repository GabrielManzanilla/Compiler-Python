

import config
from append_table import fill_table_lexemas, fill_table_errors, fill_table_triplo
from admin_jumps import add_jumps_in_triplo
from parse_ast import evaluate


def compile(code, table_lexemas, table_errors, triplo_table):

    config.lexemas.clear() #limpiar la tabla
    config.errors.clear() #limpiar la tabla
    config.triplo.clear() #limpiar la tabla
    config.TEMPORALS.clear() #limpiar la tabla
    config.CONDITIONS.clear() #limpiar la tabla
    config.is_First=True #reiniciar la variable
    config.is_BinOp=False #reiniciar la variable
    config.is_Condition=False #reiniciar la variable
    config.is_Comparator=False #reiniciar la variable
    config.CONTADOR_IF=0 #reiniciar la variable

    config.CONTADOR={
    "temp": 1,
    "operator_comparator":None
    }

    config.JUMPS=[]
    config.INDEX_JMP=[]

    table_lexemas.clearContents() #limpiar la tabla
    table_errors.clearContents() #limpiar la tabla
    triplo_table.clearContents() #limpiar la tabla

    evaluate(code) #evaluar el codigo

    fill_table_lexemas(table_lexemas, config.lexemas)
    fill_table_errors(table_errors, config.errors)
    fill_table_triplo(triplo_table, config.triplo)


