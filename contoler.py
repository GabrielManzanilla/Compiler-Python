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





def evaluate(node):

    if isinstance(node, ast.BinOp):  # Nodo de operación binaria
        # Evaluar operandos con reutilización de temporales
        left = evaluate(node.left)
        right= evaluate(node.right)
        op_type = type(node.op)
        # contador_temp=config.CONTADOR["temp"]
        
        if op_type in OPERATORS:
            # Actualizar el valor del temporal actual con el resultado de la operación
            result = OPERATORS[op_type](left, right)

            """Detectar si hay temporales en alguno de los nodos"""
            temp_in_left=next((clave for clave, valor in temp_values.items() if valor == left), None)
            temp_in_right=next((clave for clave, valor in temp_values.items() if valor == right), None)

            """Detectar si alguno de los datos es una variable y recuperar el dato en caso de que sea asi"""
            left= next((clave for clave, (type_data, value_data) in config.lexemas.items() if value_data == left), left)
            right= next((clave for clave, (type_data, value_data) in config.lexemas.items() if value_data == right), right)

            if temp_in_left and temp_in_right==None:
                contador_temp=config.CONTADOR["temp"]
                #print(f"caso left True y Right None {contador_temp}")
                config.triplo.append([f"T{contador_temp}", right, OPERATOR_SYMBOLS[op_type]])
                #print(f"T{contador_temp} {OPERATOR_SYMBOLS[op_type]} {right}")

            elif temp_in_left==None and temp_in_right:
                contador_temp=config.CONTADOR["temp"]
                #print(f"caso left None y Right True {contador_temp}")
                contador_temp+=1
                config.CONTADOR["temp"]=contador_temp
                config.triplo.append([f"T{contador_temp}", left, "="])
                #print(f"T{contador_temp} = {left}")
                config.triplo.append([f"T{contador_temp}", temp_in_right, OPERATOR_SYMBOLS[op_type]])
                #print(f"T{contador_temp} {OPERATOR_SYMBOLS[op_type]} {temp_in_right}")

            elif temp_in_left and temp_in_right:
                #print(f"caso left True y Right True {contador_temp}")
                contador_temp=config.CONTADOR["temp"]
                config.triplo.append([temp_in_left, temp_in_right , OPERATOR_SYMBOLS[op_type]])
                #print(f"{temp_in_left} {OPERATOR_SYMBOLS[op_type]} {temp_in_right}")
            else:
                config.CONTADOR["temp"]=1 #inicializa el contador
                contador_temp=config.CONTADOR["temp"] #recupera el valor 
                #print(f"caso else {contador_temp}")
                config.triplo.append([f"T{contador_temp}", left, "="])
                #print(f"T{contador_temp} = {left}")
                config.triplo.append([f"T{contador_temp}", right, OPERATOR_SYMBOLS[op_type]])
                #print(f"T{contador_temp} {OPERATOR_SYMBOLS[op_type]} {right}")
            
            temp_values[f"T{contador_temp}"]=result
            # print(temp_values)
            return result
        

    elif isinstance(node, ast.UnaryOp):  # Operación unaria
        #contador_temp=config.CONTADOR["temp"]
        operand = evaluate(node.operand, contador_temp)
        if isinstance(node.op, ast.USub):
            result = -operand
            return result
    elif isinstance(node, ast.Constant):  # Nodo de constante
        return node.value
    elif isinstance(node, ast.Name):  # Nodo de variable
        return node.value
    else:
        raise TypeError(f"Tipo de nodo no soportado: {type(node)}")

def eval_expr(expr):
    # Reiniciar los valores de los temporales
    tree = ast.parse(expr, mode='exec')
    for node in tree.body:
        if isinstance(node, ast.Assign):
            var_id= node.targets[0].id
            result = evaluate(node.value)
            contador_temp=config.CONTADOR["temp"]
            config.triplo.append([var_id, f"T{contador_temp}", "="])
            print(f"{var_id} = T{contador_temp}")
            config.CONTADOR["temp"]=1
            

# Ejemplo de us
# expression = "_Var = 59 + 3 * 2 + 4 - 5 "
# result = eval_expr(expression)

# print("-----------|TRIPLO|-----------")
# for index,i in enumerate(triplo_temp):
#     config.triplo.append([index+1]+i)

# for i in config.triplo:
#     print(i)


# """" Prueba """
