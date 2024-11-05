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
            # Mostrar el paso con el operador

            clave_left=next((clave for clave, valor in temp_values.items() if valor == left), None)
            clave_right=next((clave for clave, valor in temp_values.items() if valor == right), None)

            if clave_left and clave_right==None:
                contador_temp=config.CONTADOR["temp"]
                #print(f"caso left True y Right None {contador_temp}")
                print(contador_temp)
                print(f"T{contador_temp} {OPERATOR_SYMBOLS[op_type]} {right}")

            elif clave_left==None and clave_right:
                contador_temp=config.CONTADOR["temp"]
                #print(f"caso left None y Right True {contador_temp}")
                contador_temp+=1
                config.CONTADOR["temp"]=contador_temp
                print(f"T{contador_temp} = {left}")
                print(f"T{contador_temp} {OPERATOR_SYMBOLS[op_type]} {clave_right}")

            elif clave_left and clave_right:
                #print(f"caso left True y Right True {contador_temp}")
                contador_temp=config.CONTADOR["temp"]
                print(f"{clave_left} {OPERATOR_SYMBOLS[op_type]} {clave_right}")
            else:
                config.CONTADOR["temp"]=1 #inicializa el contador
                contador_temp=config.CONTADOR["temp"] #recupera el valor 
                #print(f"caso else {contador_temp}")
                print(f"T{contador_temp} = {left}")
                print(f"T{contador_temp} {OPERATOR_SYMBOLS[op_type]} {right}")
            
            temp_values[f"T{contador_temp}"]=result
            # print(temp_values)
            return result
        

    elif isinstance(node, ast.UnaryOp):  # Operación unaria
        #contador_temp=config.CONTADOR["temp"]
        operand = evaluate(node.operand, contador_temp)
        if isinstance(node.op, ast.USub):
            result = -operand
            #temp_values[f"T{contador_temp}"] = result
            #triplo_temp.append([contador_temp, "-", operand, None, result])
            # print(f"{contador_temp} = -{operand} -> {result}")
            return result
    elif isinstance(node, ast.Constant):  # Nodo de constante
        #contador_temp=config.CONTADOR["temp"]
        #temp_values[f"T{contador_temp}"] = node.value
        #triplo_temp.append([contador_temp, "=", node.value, None, node.value])
        # print(f"{contador_temp} = {node.value}")
        return node.value
    elif isinstance(node, ast.Name):  # Nodo de variable
        #contador_temp=config.CONTADOR["temp"]
        #temp_values[f"T{contador_temp}"] = node.value
        #triplo_temp.append([contador_temp, "=", node.id, None, node.id])
        # print(f"{contador_temp} = {node.id}")
        return node.value
    else:
        raise TypeError(f"Tipo de nodo no soportado: {type(node)}")

def eval_expr(expr):
    # Reiniciar los valores de los temporales
    tree = ast.parse(expr, mode='exec')
    for node in tree.body:
        if isinstance(node, ast.Assign):
            result = evaluate(node.value)
            return result

# Ejemplo de uso
expression = "_Var = 5 + 3 * 2 + 4 - (5 + 1)"
result = eval_expr(expression)

print("-----------|TRIPLO|-----------")
for index,i in enumerate(triplo_temp):
    config.triplo.append([index+1]+i)

for i in config.triplo:
    print(i)


"""" Prueba """
