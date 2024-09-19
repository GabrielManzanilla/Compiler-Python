from handler_error import append_error
types={
    #int, float, str, None
    (True,False,False,False): int,
    (False,True,False,False): float,
    (False,False,True,False): str,
    (True,True,False,False): float,

}

def asign_types(contain_int, contain_float, contain_str, contain_none):
    type_result = types.get((contain_int, contain_float, contain_str, contain_none), None)
    return type_result


#----Funcion para identificar el tipo de dato de los operandos----
def lexemas_incompatible_types(operands):
    base_type=operands[0][1] #pasando la tipo del primer elemento
    diferent_elements=[]
    type_numeric_elements=[] 
    for element in operands:
        # print(element)
        if isinstance(base_type,(int,float)) and isinstance(element[1] ,(int,float)) and element[1] is not None: 
            type_numeric_elements.append(element[1])
            continue
        elif element[1] is not None and element[1]!= base_type:
            diferent_elements.append(element[0])

    return diferent_elements
    

#----Funcion para comparar tipos de datos----
def compare_types(operands, index, var_asignacion): #operands=[[id, type], [id, type], ...]
    len_int=False
    len_float=False
    len_str=False
    len_none=False
    array_int=[]
    array_float=[]
    array_str=[]

    for element in operands:
        if element[1]== int: 
            len_int=True
            array_int.append(element[0])
        elif element[1]== float: 
            len_float=True
            array_float.append(element[0])
        elif element[1]==str: 
            len_str=True
            array_str.append(element[0])
        elif element[1]==None: len_none=True

    array_number=array_int+array_float

    if asign_types(len_int, len_float, len_str,len_none) == None and len_none==False: 
        lexemas_error=array_str if len(array_str) < len(array_number) else array_number
        append_error(lexemas_error, index, f"Tipos de datos incompatibles en: \"{var_asignacion}\"")
    return asign_types(len_int, len_float, len_str, len_none) 
            

            #[valor, tipo]