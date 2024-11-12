import config

#----Funcion para descomponer la operacion binaria----
def append_error(lexema, index, mensaje): #funcion para añadir errores a la tabla de errores (lexema donde esta el error, el index, tipo de error)
    tamanio=len(config.errors)
    token="ErrorSem"+str(tamanio+1)
    config.errors[token]=(lexema,index+1, mensaje)

