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
        if fila[2]=="SINO":
            ifs.append(i)
            print(ifs)
        if fila[1]=="ENDIF":
            for j in ifs:
                triplo_original[j][2]=str(i+2)
                ifs.clear()
            
        if fila[1]=="ENDELSE":
            elses.append(i)
            for j in ifs:
                triplo_original[j][1]=str(i+1)
                elses.clear()
    return triplo_original



def add_jumps_in_triplo(triplo):
    triplo=add_jumps_in_Logic_Operators(triplo)
    triplo=add_jumps_in_If(triplo)