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
    ast.Pow: "**",
    ast.Gt: ">",
    ast.GtE: ">=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Eq: "==",
    ast.NotEq: "!=",
    ast.Is: "is",
    ast.IsNot: "is not",
    ast.In: "in",
    ast.NotIn: "not in",
    ast.And: "and",
    ast.Or: "or",
    ast.USub: "-"

}


# Variables temporales reutilizables
temp_values = {}

def evaluate(node, is_If=False):
    is_First=True
    if isinstance(node, ast.BinOp):  # Nodo de operación binaria
        is_First=False
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
        if is_If is False and is_First is True:
            contador_temp=config.CONTADOR["temp"]
            config.triplo.append([f"T{contador_temp}", node.value, "="])
        return node.value
    elif isinstance(node, ast.Name):  # Nodo de variable
        if is_If is False and is_First is True:
            contador_temp=config.CONTADOR["temp"]
            config.triplo.append([f"T{contador_temp}", node.id, "="])
        (type_data, result)=config.lexemas[node.id]
        return result
    elif isinstance(node, ast.Assign):
        var_id= node.targets[0].id
        result = evaluate(node.value)
        config.lexemas[var_id]=(type(result), result)
        contador_temp=config.CONTADOR["temp"]
        config.triplo.append([var_id, f"T{contador_temp}", "="])
        config.CONTADOR["temp"]=1



    elif isinstance(node, ast.If):
        condition = extract_if_conditions(node.test)
        config.triplo.append([f"TR1", f"TRUE", "CONTINUE"])
        config.triplo.append([f"TR1", f"FALSE", "SINO"])
        config.JUMPS.append([])
        body = [evaluate(stmt) for stmt in node.body]
        if node.orelse:
            config.triplo.append([f"", "ENDIF", "JR"])
            orelse = [evaluate(stmt) for stmt in node.orelse]
            config.triplo.append([f"", "ENDELSE", "JR"])


            
    else:
        raise TypeError(f"Tipo de nodo no soportado: {type(node)}")




def extract_if_conditions(node):
    """Extrae y procesa condiciones con operadores lógicos `and`/`or` en nodos `If`."""
    if isinstance(node, ast.BoolOp):
        op = type(node.op).__name__  # Identifica si es `And` o `Or`
        config.CONTADOR["operator_comparator"]=op
        op= config.CONTADOR["operator_comparator"]
        conditions = [extract_if_conditions(value) for value in node.values]
        contador_temp=config.CONTADOR["temp"]
        try:
            left1 = conditions[0]['left']
            operator1 = conditions[0]['operators']
            comparator1 = conditions[0]['comparators']
            left1= next((clave for clave, (type_data, value_data) in config.lexemas.items() if value_data == left1), left1)
            print(f"left1: {left1}")
            config.triplo.append([f"T{contador_temp}", left1, "="])
            config.triplo.append([f"T{contador_temp}", comparator1, operator1])
        except:
            None

        if(op=="And"):
            config.triplo.append([f"TR1", f"TRUE", "AND"])
            config.triplo.append([f"TR1", f"FALSE", "SINO"])
        elif(op=="Or"):
            config.triplo.append([f"TR1", f"TRUE", "SI"])
            config.triplo.append([f"TR1", f"FALSE", "OR"])
        # else:
        #     config.triplo.append([f"TR1", f"TRUE", "SINO"])
        #     config.triplo.append([f"TR1", f"FALSE", "CONTINUE"])
        # Extraer el segundo diccionario
        left2 = conditions[1]['left']
        operator2 = conditions[1]['operators']
        comparator2 = conditions[1]['comparators']
        config.triplo.append([f"T{contador_temp}", left2, "="])
        config.triplo.append([f"T{contador_temp}", comparator2, operator2])
        # Imprimir los valores extraídos

        return {"op": op, "conditions": conditions}


    elif isinstance(node, ast.Compare):
        try:
            (type_left, left) =config.lexemas[node.left.id]
        except:
            left=node.left.value

        operators = [OPERATOR_SYMBOLS[type(op)] for op in node.ops]
        comparators = [evaluate(c,True) for c in node.comparators]
        contador_temp = config.CONTADOR["temp"]
        config.triplo.append([f"T{contador_temp}", node.left.id, "="])
        try:
            var_id= next((clave for clave, (type_data, value_data) in config.lexemas.items() if value_data == comparators[0]), comparators[0])
            config.triplo.append([f"T{contador_temp}", var_id, operators[0]])
        except:
            config.triplo.append([f"T{contador_temp}", comparators[0], operators[0]])

        return {"left": left, "operators": operators[0], "comparators": comparators[0]}



def eval_expr(expr):
    # Reiniciar los valores de los temporales

    tree = ast.parse(expr, mode='exec')
    for node in tree.body:
        evaluate(node)


# code="""
# _Var=10
# if 5<20:
# 	_Var2=1+1"""
# eval_expr(code)
# [print(tr) for tr in config.triplo]