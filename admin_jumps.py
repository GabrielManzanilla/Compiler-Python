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
    global jmp_beginif, jmp_endif, jmp_endelse
    jmp_beginif, jmp_endif, jmp_endelse = None, None, None
    i = 0  # Para detectar donde inicia el cuerpo del if
    while i < len(triplo_original):
        fila = triplo_original[i]
        if fila[1]=="BEGINIF" and fila[3]==config.CONTADOR_IF:
            jmp_beginif=i+1-((config.CONTADOR_IF-1))
            del triplo_original[i]
            i=0
            continue
        i+=1

    #Para detectar donde termina el cuerpo del if
    for i, fila in enumerate(triplo_original):
        if fila[1]=="ENDIF" and fila[3]==config.CONTADOR_IF:
            jmp_endif=i+1-((config.CONTADOR_IF-1))


    
    #Detectar donde termina el else
    i = 0 
    while i < len(triplo_original):
        fila = triplo_original[i]
        if fila[1]=="ENDELSE" and fila[3]==config.CONTADOR_IF:
            jmp_endelse=i+1-((config.CONTADOR_IF-1))
            del triplo_original[i]
            i=0
            continue
        i+=1




    for i, fila in enumerate(triplo_original):
        if fila[2]=="SI" and fila[3]==config.CONTADOR_IF and i<= jmp_endif:
            fila[2]=str(jmp_beginif)
            fila.pop(3)


        if fila[1]=="ENDELSE" and fila[3]==config.CONTADOR_IF and i<= jmp_endelse:
            del fila
        if jmp_endelse:
            if fila[1]=="ENDIF" and fila[3]==config.CONTADOR_IF and jmp_endelse:
                fila[1]=str(jmp_endelse+1)
                fila.pop(3)
            if fila[2]=="SINO" and fila[3]==config.CONTADOR_IF and i<= jmp_endif:
                fila[2]=str(jmp_endif)
                fila.pop(3)
        else:
            if fila[1]=="ENDIF" and fila[3]==config.CONTADOR_IF:
                del triplo_original[i]
            if fila[2]=="SINO" and fila[3]==config.CONTADOR_IF:
                fila[2]=str(jmp_endif)
                fila.pop(3)
    return triplo_original



def add_jumps_in_triplo(triplo):
    triplo=add_jumps_in_Logic_Operators(triplo)
    # triplo=add_jumps_in_If(triplo)