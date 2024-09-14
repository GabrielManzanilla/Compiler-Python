from handler_error import append_error
types={
    (False,False,False): None,
    (True,False,False): int,
    (False,True,False): float,
    (False,False,True): str,
    (True,True,False): float,
    (True,False,True): None,
    (False,True,True): None,
    (True,True,True): None,
    
}

def asign_types(contain_int, contain_float, contain_str):
    type_result=types[(contain_int, contain_float, contain_str)]
    return type_result


#----Funcion para identificar el tipo de dato de los operandos----
def lexemas_incompatible_types(operands):
    base_type=operands[0][1] #pasando la tipo del primer elemento
    diferent_elements=[]
    type_numeric_elements=[] 
    for element in operands:
        if isinstance(base_type,(int,float)) & isinstance(element[1],(int,float)): 
            type_numeric_elements.append(element[1])
            continue
        elif element[1]!= base_type:
            diferent_elements.append(element[0])

    return diferent_elements
    

#----Funcion para comparar tipos de datos----
def compare_types(operands, index): #operands=[[id, type], [id, type], ...]
    len_int=False
    len_float=False
    len_str=False
    lexemas_error=lexemas_incompatible_types(operands)
    for element in operands:
        if element[1]== int: len_int=True
        elif element[1]== float: len_float=True
        elif element[1]==str: len_str=True
    return asign_types(len_int, len_float, len_str) if not asign_types(len_int, len_float, len_str) == None else append_error(lexemas_error, index, "Tipos de datos incompatibles")
            