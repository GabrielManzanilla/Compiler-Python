import ast
import re


regex=r"^_[A-Z][a-zA-Z0-9_]*$"

def assignment_var_details(target, node):
    if re.match(regex, target.id): #comprueba sintaxis de la variable con regex
        value_data=(node.body[0].value.value)
        type_data= type(value_data) #llama a una funcion para que se asigne si es de tipo real-int o string-char
        variable=str(target.id)
        return variable,type_data,value_data #se añade al diccionario la variable, su tipo de dato y el dato que la variable contiene
    else:
        print("sintaxis de variable no aceptada", target.id)
        return None, None, None



def define_vars(code_line):
    try:
        node =ast.parse(code_line, mode='exec')
        if isinstance(node.body[0], ast.Assign): #compruba que la linea sea de asignacion
            for target in node.body[0].targets:
                return assignment_var_details(target, node)
        elif isinstance(node.body[0], ast.Assign):
            operation=node.body[0].value
            
                # if vars[target.id]:  return assignment_var_details(target, node)

    except Exception as e:
        print(f"Error in {e}")
        return None, None, None

