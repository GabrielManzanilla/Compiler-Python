
def add_jumps_in_triplo(triplo_original):
    for i, fila in enumerate(triplo_original):
        if fila[2]=="AND":
            triplo_original[i][2]=str(i+3)
        if fila[2]=="OR":
            triplo_original[i][2]=str(i+2)
        if fila[2]=="CONTINUE":
            triplo_original[i][2]=str(i+3)