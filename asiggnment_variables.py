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


def define_vars(code_line):
        tree =ast.parse(code_line)
        for node in tree.body:
            if isinstance(node, ast.Assign): #compruba que la linea sea de asignacion

                if isinstance(node.value, ast.BinOp):
                        left=node.value.left.id if isinstance(node.value.left, ast.Name) else None
                        print(left)
                        right=node.value.right.id  if isinstance(node.value.right, ast.Name) else None
                        print(right)
                        return None, None, None
                elif isinstance(node.value, ast.Constant):
                        #dany estuvo aqui sdsfddvcvcbvb
                        return assignment_var_details(node.targets[0], node.value)

        return None, None, None
