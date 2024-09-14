#--importacion de modulos--
import ast
import re
#--importacion de funciones externas
from breaker import break_error_regex
#-- importacion del archivo donde se encuentra el arreglo
import config

regex=r"^_[A-Z][a-zA-Z0-9_]*$"




#----Funcion para descomponer la operacion binaria----
def append_error(lexema, index, mensaje): #funcion para añadir errores a la tabla de errores (lexema donde esta el error, el index, tipo de error)
    print("Error table")
    tamanio=len(config.errors)
    token="ErrorSem"+str(tamanio+1)
    config.errors[token]=(lexema,index, mensaje)



def parse_binop(node, index):
    left_operands=[]
    right_operands=[]

    #lado izquierdo
    if isinstance(node.left, ast.BinOp):
        left_operands.extend(parse_binop(node.left, index))  # Recursivamente descomponer el lado izquierdo
    elif isinstance(node.left, ast.Name):
        var_id=node.left.id
        (left_operands.append([var_id, type(var_id)]) if  var_id in config.lexemas else append_error(var_id, index, "Variable indefinida"))if re.match(regex, var_id) else break_error_regex(var_id)
        #si hace match con el regex y ya se encuentra en la tabla de lexemas se añade el id y su tipo a la lista, sino se manda a una funcion para insertar errores
    elif isinstance(node.left, ast.Constant):
        dato=node.left.value
        left_operands.append([dato, type(dato)])  # Si es una constante se añade al arreglo el dato y su tipo

    # Lado derecho
    if isinstance(node.right, ast.BinOp):
        right_operands.extend(parse_binop(node.right, index))  # Recursivamente descomponer el lado derecho
    elif isinstance(node.right, ast.Name):
        var_id=node.right.id
        (right_operands.append([var_id, type(var_id)]) if var_id in config.lexemas else append_error(var_id, index, "Variable indefinida"))if re.match(regex, var_id) else break_error_regex(var_id)
    elif isinstance(node.right, ast.Constant):
        dato=node.right.value
        right_operands.append([dato, type(dato)]) # Si es una constante, extraer el valor

    return left_operands + right_operands



#----Funcion para comparar tipos de datos----
def compare_types(operands, index): #operands=[[id, type], [id, type], ...]
    base_type=operands[0][1] #pasando la tipo del primer elemento
    diferent_elements=[]
    type_numeric_elements=[] 
    for element in operands:
        if isinstance(base_type,(int,float)) & isinstance(element[1],(int,float)): 
            type_numeric_elements.append(element[1])
            continue
        elif element[1]!= base_type:
            diferent_elements.append(element[0])

    if not len(diferent_elements) == 0:
        append_error(diferent_elements, index, "Incompatibilidad de tipos")
        return None
    else:
        return float if float in type_numeric_elements else int
            


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