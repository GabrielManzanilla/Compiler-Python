import ast
import re


regex=r"^_[A-Z][a-zA-Z0-9_]*$"

def assignment_var_details(target, node):
    if re.match(regex, target.id): #comprueba sintaxis de la variable con regex
        value_data=(node.value)
        type_data= type(value_data) #llama a una funcion para que se asigne si es de tipo real-int o string-char
        variable=target.id
        return variable,type_data,value_data #se añade al diccionario la variable, su tipo de dato y el dato que la variable contiene
    else:
        print("sintaxis de variable no aceptada", target.id)
        return None, None, None


def error_table():
     print("Error table")

def parse_binop(node, vars):
    left_operands=[]
    right_operands=[]

    if isinstance(node.left, ast.BinOp):
        left_operands.extend(parse_binop(node.left))  # Recursivamente descomponer el lado izquierdo

    elif isinstance(node.left, ast.Name):
        if re.match(regex, node.left.id):
            error_table(node.left.id) if node.left.id not in vars else None 
            left_operands.append(type(node.left.id)) #si es una variable se comprueba que siga el regex y que este en la tabla de variables, sino se manda a la tabla de errores

    elif isinstance(node.left, ast.Constant):
        left_operands.append(type(node.left.value))  # Si es una constante, extraer el valor

    # Lado derecho
    if isinstance(node.right, ast.BinOp):
        right_operands.extend(parse_binop(node.right))  # Recursivamente descomponer el lado derecho

    elif isinstance(node.right, ast.Name):
        error_table(node.left.id) if node.left.id not in vars else None 
        right_operands.append(type(node.right.id))  # Si es un nombre de variable, extraer el id error_table(node.left.id) if node.left.id not in vars else None 
        right_operands.append(type(node.right.id))  # Si es un nombre de variable, extraer el id  # Si es un nombre de variable, extraer el id

    elif isinstance(node.right, ast.Constant):
        right_operands.append(type(node.right.value))  # Si es una constante, extraer el valor

    print( left_operands + right_operands)
      

def define_vars(code_line, vars):
        tree =ast.parse(code_line)
        for node in tree.body:
            if isinstance(node, ast.Assign): #compruba que la linea sea de asignacion
                if isinstance(node.value, ast.BinOp):
                        operands= parse_binop(node.value, vars)
                        return operands
                elif isinstance(node.value, ast.Constant):
                        #dany estuvo aqui sdsfddvcvcbvb
                        return assignment_var_details(node.targets[0], node.value)

        return None, None, None
