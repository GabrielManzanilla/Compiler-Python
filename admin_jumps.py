import config
ifs = []    
elses=[]
def add_jumps_in_Logic_Operators(triplo_original):
    for i, fila in enumerate(triplo_original):
        if fila[2]=="AND":
            triplo_original[i][2]=str(i+3)
        if fila[2]=="OR":
            triplo_original[i][2]=str(i+2)
        if fila[2]=="CONTINUE":
            triplo_original[i][2]=str(i+3)
    return triplo_original

def add_jumps_in_If(triplo_original):
    for i, fila in enumerate(triplo_original):
        if fila[1]=="ENDIF" and fila[3]==config.CONTADOR_IF:
            global jmp_endif
            jmp_endif=i+2

    
    
    i = 0  # Inicializamos el índice manualmente
    while i < len(triplo_original):
        fila = triplo_original[i]
        if fila[1]=="ENDELSE" and fila[3]==config.CONTADOR_IF:

            jmp_endelse=i+config.CONTADOR_IF
            del triplo_original[i]
            i=0
            continue
        i+=1


    for i, fila in enumerate(triplo_original):
        if fila[2]=="SINO" and fila[3]==config.CONTADOR_IF and i<= jmp_endif:
            fila[2]=str(jmp_endif)
            fila.pop(3)
        if fila[1]=="ENDIF" and fila[3]==config.CONTADOR_IF and i<= jmp_endelse:
            fila[1]=str(jmp_endelse)
            fila.pop(3)

    return triplo_original


def jmp_only_If(triplo_original):
    tamaño=len(triplo_original)
    for i, fila in enumerate(triplo_original):
        if fila[2]=="SINO" and fila[3]==config.CONTADOR_IF:
            fila[2]=str(tamaño+1)
            fila.pop(3)
        if fila[2]=="CONTINUE":
            fila[2]=str(i+3)

def add_jumps_in_triplo(triplo):
    triplo=add_jumps_in_Logic_Operators(triplo)
    # triplo=add_jumps_in_If(triplo)