# --importacion de modulos-- 
import ast
import re
import operator

# --importacion de funciones externas
from compare import compare_types
from handler_error import append_error
# --importacion del archivo donde se encuentra el arreglo
import config

# Expresión regular para variables válidas
regex = r"^_[A-Z][a-zA-Z0-9_]*$"

# Diccionario de operadores
def obtener_operador(binop):
    operadores = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow
    }
    return operadores[type(binop)]  # Devuelve la operación correspondiente

# Variables temporales reutilizables
temp_values = {"T1": None, "T2": None}

# Funcion para descomponer la operacion binaria
def parse_binop(node, index):
    left_operands = []
    right_operands = []

    # Asignación de temporales para resultados parciales
    temporal = "T1"

    # Lado izquierdo
    if isinstance(node.left, ast.BinOp):
        operands, left_value_data = parse_binop(node.left, index)  # Descomposición recursiva
        left_operands.extend(operands)
    elif isinstance(node.left, ast.Name):
        var_id = node.left.id
        if re.match(regex, var_id):
            if var_id in config.lexemas:
                type_data, left_value_data = config.lexemas[var_id]
            else:
                append_error(var_id, index, "Variable indefinida")
                type_data = None
            left_operands.append([var_id, type_data]) if node.left.id is not None else None
        else:
            append_error(var_id, index, "REGEX incorrecto")
    elif isinstance(node.left, ast.Constant):
        left_value_data = node.left.value
        temp_values[temporal] = left_value_data  # Asignar el valor al temporal
        print(f"{temporal} = {left_value_data}")
        left_operands.append([left_value_data, type(left_value_data)]) if node.left.value is not None else None

    # Lado derecho
    temporal = "T2" if temporal == "T1" else "T1"  # Alternar el uso de T1 y T2
    if isinstance(node.right, ast.BinOp):
        operands, right_value_data = parse_binop(node.right, index)  # Descomposición recursiva
        right_operands.extend(operands)
    elif isinstance(node.right, ast.Name):
        var_id = node.right.id
        if re.match(regex, var_id):
            if var_id in config.lexemas:
                type_data, right_value_data = config.lexemas[var_id]
            else:
                append_error(var_id, index, "Variable indefinida")
                type_data = None
            right_operands.append([var_id, type_data]) if node.right.id is not None else None
        else:
            append_error(var_id, index, "REGEX incorrecto")
    elif isinstance(node.right, ast.Constant):
        right_value_data = node.right.value
        temp_values[temporal] = right_value_data  # Asignar el valor al temporal
        print(f"{temporal} = {right_value_data}")
        right_operands.append([right_value_data, type(right_value_data)]) if node.right.value is not None else None

    # Obtener operador y aplicar operación entre temporales
    operador = obtener_operador(node.op)
    try:
        result = operador(temp_values["T1"], temp_values["T2"])
        temp_values["T1"] = result  # Guardar el resultado final en T1
        print(f"{temporal} = {temp_values['T1']} {config.OPERATOR_SYMBOLS[type(node.op)]} {temp_values['T2']} -> {result}")
    except Exception as e:
        result = None
        append_error("Operación inválida", index, str(e))

    operands = left_operands + right_operands
    return operands, result

# Función auxiliar para procesar constantes
def process_constant(node, var_id, index):
    value = node.value
    type_value = type(value)
    if re.match(regex, var_id):
        config.lexemas[var_id] = (type_value, value)
    else:
        append_error(var_id, index, "REGEX incorrecto")

# Función auxiliar para procesar nombres de variables
def process_name(node, var_id, index):
    if re.match(regex, var_id):
        if var_id in config.lexemas:
            config.lexemas[var_id] = config.lexemas[var_id]
        else:
            append_error(var_id, index, "Variable indefinida")
    else:
        append_error(var_id, index, "REGEX incorrecto")

# Función para identificar la operación de asignación
def identify_operation(code):
    tree = ast.parse(code, mode='exec')
    for index, node in enumerate(tree.body):
        index += 1
        try:
            if isinstance(node, ast.Assign):  # Comprueba que la línea sea de asignación
                var_id = node.targets[0].id
                if isinstance(node.value, ast.BinOp):
                    if re.match(regex, var_id):
                        operands, result = parse_binop(node.value, index)
                        type_result = compare_types(operands, index, var_id)
                        config.lexemas[var_id] = (type_result, result)
                    else:
                        append_error(var_id, index, "REGEX incorrecto")
                elif isinstance(node.value, ast.Name):
                    process_name(node.value, var_id, index)
                elif isinstance(node.value, ast.Constant):
                    process_constant(node.value, var_id, index)
        except Exception as e:
            print(f"Error en la operación de asignación: {e}")
