import sys
#este modulo sirve para unica y exclusivamente cerrar el programa cuando se detecte una variable con sintaxis correcta
def break_error_regex(var):
    print(f"--DETENIDO--\nLa variable{var} no cumple con la sintaxis adecuada")
    sys.exit()
