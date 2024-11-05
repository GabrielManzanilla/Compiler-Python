import ast
import operator
import config

# Diccionario de operadores
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow
}

triplo_temp = []

# Diccionario para los símbolos de los operadores
OPERATOR_SYMBOLS = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.Pow: "**"
}

# Variables temporales reutilizables
temp_values = {}

# Declarar is_First como una variable global
is_First = True

def evaluate(node):
    global is_First  # Referencia a la variable global
    if isinstance(node, ast.BinOp):  # Nodo de operación binaria
        is_First = False
        # Evaluar operandos con reutilización de temporales
        left = evaluate(node.left)
        right = evaluate(node.right)
        op_type = type(node.op)

        if op_type in OPERATORS:
            # Actualizar el valor del temporal actual con el resultado de la operación
            result = OPERATORS[op_type](left, right)

            """Detectar si hay temporales en alguno de los nodos"""
            temp_in_left = next((clave for clave, valor in temp_values.items() if valor == left), None)
            temp_in_right = next((clave for clave, valor in temp_values.items() if valor == right), None)

            """Detectar si alguno de los datos es una variable y recuperar el dato en caso de que sea asi"""
            left = next((clave for clave, (type_data, value_data) in config.lexemas.items() if value_data == left), left)
            right = next((clave for clave, (type_data, value_data) in config.lexemas.items() if value_data == right), right)

            # Lógica para manejar los diferentes casos
            if temp_in_left and temp_in_right == None:
                contador_temp = config.CONTADOR["temp"]
                config.triplo.append([f"T{contador_temp}", right, OPERATOR_SYMBOLS[op_type]])

            elif temp_in_left == None and temp_in_right:
                contador_temp = config.CONTADOR["temp"]
                contador_temp += 1
                config.CONTADOR["temp"] = contador_temp
                config.triplo.append([f"T{contador_temp}", left, "="])
                config.triplo.append([f"T{contador_temp}", temp_in_right, OPERATOR_SYMBOLS[op_type]])

            elif temp_in_left and temp_in_right:
                contador_temp = config.CONTADOR["temp"]
                config.triplo.append([temp_in_left, temp_in_right, OPERATOR_SYMBOLS[op_type]])
            else:
                config.CONTADOR["temp"] = 1
                contador_temp = config.CONTADOR["temp"]
                config.triplo.append([f"T{contador_temp}", left, "="])
                config.triplo.append([f"T{contador_temp}", right, OPERATOR_SYMBOLS[op_type]])
            
            temp_values[f"T{contador_temp}"] = result
            return result

    elif isinstance(node, ast.UnaryOp):
        operand = evaluate(node.operand)
        if isinstance(node.op, ast.USub):
            result = -operand
            return result
    elif isinstance(node, ast.Constant):
        if is_First:
            contador_temp = config.CONTADOR["temp"]
            config.triplo.append([f"T{contador_temp}", node.value, "="])
        return node.value
    elif isinstance(node, ast.Name):
        if is_First:
            contador_temp = config.CONTADOR["temp"]
            config.triplo.append([f"T{contador_temp}", node.id, "="])
        (type_data, result) = config.lexemas[node.id]
        return result
    else:
        raise TypeError(f"Tipo de nodo no soportado: {type(node)}")

def eval_expr(expr):
    # Reiniciar los valores de los temporales
    global is_First
    is_First = True  # Reiniciar el estado de is_First al evaluar una nueva expresión
    tree = ast.parse(expr, mode='exec')
    for node in tree.body:
        if isinstance(node, ast.Assign):
            var_id = node.targets[0].id
            result = evaluate(node.value)
            contador_temp = config.CONTADOR["temp"]
            config.triplo.append([var_id, f"T{contador_temp}", "="])
            print(f"{var_id} = T{contador_temp}")
            config.CONTADOR["temp"] = 1

