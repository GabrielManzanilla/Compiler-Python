#--importacion de modulos--
import ast
import re
#--importacion de funciones externas
from breaker import break_error_regex
from compare import compare_types
from handler_error import append_error
#-- importacion del archivo donde se encuentra el arreglo
import config


regex=r"^_[A-Z][a-zA-Z0-9_]*$"

#----Funcion para descomponer la operacion binaria----
def parse_binop(node, index):
    left_operands=[]
    right_operands=[]

    #lado izquierdo
    if isinstance(node.left, ast.BinOp):
        left_operands.extend(parse_binop(node.left, index))  # Recursivamente descomponer el lado izquierdo
    elif isinstance(node.left, ast.Name):
        var_id=node.left.id
        if re.match(regex, var_id):
            if  var_id in config.lexemas:
                type_data, value_data=config.lexemas[var_id]
                left_operands.append([var_id, type_data])
             
            else: append_error(var_id, index, "Variable indefinida")

        else: break_error_regex(var_id)
        #si hace match con el regex y ya se encuentra en la tabla de lexemas se añade el id y su tipo a la lista, sino se manda a una funcion para insertar errores
        #type_data, value_data=config.lexemas[var_id]
    elif isinstance(node.left, ast.Constant):
        dato=node.left.value
        left_operands.append([dato, type(dato)])  # Si es una constante se añade al arreglo el dato y su tipo

    # Lado derecho
    if isinstance(node.right, ast.BinOp):
        right_operands.extend(parse_binop(node.right, index))  # Recursivamente descomponer el lado derecho
    elif isinstance(node.right, ast.Name):
        var_id=node.right.id
        if re.match(regex, var_id):
            if  var_id in config.lexemas:
                type_data, value_data=config.lexemas[var_id]
                right_operands.append([var_id, type_data])
             
            else: append_error(var_id, index, "Variable indefinida")

        else: break_error_regex(var_id)

    elif isinstance(node.right, ast.Constant):
        dato=node.right.value
        right_operands.append([dato, type(dato)]) # Si es una constante, extraer el valor

    
    return left_operands + right_operands




#----Funcion para identificar la operacion de asignacion----
def identify_operation(code_line, index):
        tree =ast.parse(code_line)
        for node in tree.body:
            if isinstance(node, ast.Assign): #compruba que la linea sea de asignacion
                var_id=node.targets[0].id #se obtiene el nombre de la variable
                if isinstance(node.value, ast.BinOp):
                    if re.match(regex, var_id): #se comprueba que la variable tenga la sintaxis correcta
                        operands= parse_binop(node.value, index)
                        type_result=compare_types(operands, index)
                        config.lexemas[var_id]=(type_result, None)

                    else:
                        break_error_regex(var_id)

                elif isinstance(node.value, ast.Constant):
                    value=node.value.value #se obtiene el valor de su dato
                    type_value=type(value) #se obtiene el tipo de dato de la variable
                    config.lexemas[var_id]=(type_value, value) if re.match(regex, var_id) else break_error_regex(var_id)