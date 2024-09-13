#--importacion de modulos--
import ast
import re
#--importacion de funciones externas
from breaker import break_error_regex
#-- importacion del archivo donde se encuentra el arreglo
import config

regex=r"^_[A-Z][a-zA-Z0-9_]*$"





def append_error(var_id):
     print("Error table")

def parse_binop(node):
    left_operands=[]
    right_operands=[]

    #lado izquierdo
    if isinstance(node.left, ast.BinOp):
        left_operands.extend(parse_binop(node.left))  # Recursivamente descomponer el lado izquierdo
    elif isinstance(node.left, ast.Name):
        var_id=node.left.id
        (left_operands.append([var_id, type(var_id)]) if  var_id in config.lexemas else append_error(var_id))if re.match(regex, var_id) else break_error_regex(var_id)
        #si hace match con el regex y ya se encuentra en la tabla de lexemas se añade el id y su tipo a la lista, sino se manda a una funcion para insertar errores
    elif isinstance(node.left, ast.Constant):
        dato=node.left.value
        left_operands.append([dato, type(dato)])  # Si es una constante se añade al arreglo el dato y su tipo

    # Lado derecho
    if isinstance(node.right, ast.BinOp):
        right_operands.extend(parse_binop(node.right))  # Recursivamente descomponer el lado derecho
    elif isinstance(node.right, ast.Name):
        var_id=node.right.id
        (right_operands.append([var_id, type(var_id)]) if var_id in config.lexemas else append_error(var_id))if re.match(regex, var_id) else break_error_regex(var_id)
    elif isinstance(node.right, ast.Constant):
        dato=node.left.value
        right_operands.append([dato, type(dato)]) # Si es una constante, extraer el valor

    return left_operands + right_operands





def identify_operation(code_line):
        tree =ast.parse(code_line)
        for node in tree.body:
            if isinstance(node, ast.Assign): #compruba que la linea sea de asignacion
                if isinstance(node.value, ast.BinOp):
                        operands= parse_binop(node.value)
                elif isinstance(node.value, ast.Constant):
                        var_id=node.targets[0].id #se obtiene el nombre de la variable
                        value=node.value.value #se obtiene el valor de su dato
                        type_value=type(value) #se obtiene el tipo de dato de la variable
                        config.lexemas[var_id]=(type_value, value) if re.match(regex, var_id) else break_error_regex(var_id)

