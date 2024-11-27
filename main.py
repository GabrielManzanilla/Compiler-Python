import config
from append_table import fill_table_lexemas, fill_table_errors, fill_table_triplo
from admin_jumps import add_jumps_in_triplo
from parse_ast import evaluate
from optimizer import CodeOptimizer  # Añadir esta importación

def compile(code, table_lexemas, table_errors, triplo_table):
    # Inicializar el optimizador
    optimizer = CodeOptimizer()
    
    # Optimizar el código antes de comenzar la compilación
    optimized_code = optimizer.optimize(code)
    
    # Limpiar todas las estructuras de datos como antes
    config.lexemas.clear()
    config.errors.clear()
    config.triplo.clear()
    config.TEMPORAL_ACTUAL.clear()
    config.CONDITIONS.clear()
    config.is_First = True
    config.is_BinOp = False
    config.is_Condition = False
    config.is_Comparator = False
    config.is_BoolOp = False
    config.CONTADOR_IF = 0
    config.index_global=1
    config.CONTADOR = {
        "temp": 1,
        "operator_comparator": None
    }

    config.JUMPS = []
    config.INDEX_JMP = []

    # Limpiar las tablas
    table_lexemas.clearContents()
    table_errors.clearContents()
    triplo_table.clearContents()

    # Evaluar el código optimizado en lugar del código original
    evaluate(optimized_code)

    # Llenar las tablas como antes
    fill_table_lexemas(table_lexemas, config.lexemas)
    fill_table_errors(table_errors, config.errors)
    fill_table_triplo(triplo_table, config.triplo)