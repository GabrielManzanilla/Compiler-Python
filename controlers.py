import config
def comparator_append_triplo(left, right, left_operater, right_operater, result, op_type):
	if not left in config.TEMPORALS and not right in config.TEMPORALS:
		config.triplo.append([f"T{config.CONTADOR["temp"]}", left_operater, "="])
		config.triplo.append([f"T{config.CONTADOR["temp"]}",right_operater, config.OPERATORS_SYMBOLS[op_type]])
		config.TEMPORALS.append(result)
	
	elif left in config.TEMPORALS and not right in config.TEMPORALS:
		config.triplo.append([f"T{config.CONTADOR["temp"]}", right_operater, config.OPERATORS_SYMBOLS[op_type]])
		config.TEMPORALS.append(result)

	elif not left in config.TEMPORALS and right in config.TEMPORALS:
		right_temporal=f"T{config.CONTADOR["temp"]}"
		config.CONTADOR["temp"]+=1
		config.triplo.append([f"T{config.CONTADOR["temp"]}", left_operater, "="])	
		config.triplo.append([f"T{config.CONTADOR["temp"]}", right_temporal, config.OPERATORS_SYMBOLS[op_type]])
		config.TEMPORALS.append(result)

	elif left in config.TEMPORALS and right in config.TEMPORALS:
		config.triplo.append([f"T{config.CONTADOR["temp"]}", left_operater, config.OPERATORS_SYMBOLS[op_type]])
		config.TEMPORALS.append(result)

def append_triplo_initial(value_left, operator):
	config.triplo.append([f"T{config.CONTADOR["temp"]}", value_left, config.OPERATORS_SYMBOLS[operator]])
	config.is_First=False

def finalice_triplo(var_id):
	config.triplo.append([var_id, f"T{config.CONTADOR["temp"]}", "="])
	config.TEMPORALS.clear()



"""" ----------------------------------------"""

def append_comparators_triplo(left, comparator, operator):
	config.triplo.append([f"T{config.CONTADOR["temp"]}", left, "="])	
	config.triplo.append([f"T{config.CONTADOR["temp"]}", comparator, operator])

def append_TR_triplo(op=""):
	if(op=="And"):
		config.triplo.append([f"TR1", f"TRUE", "AND"])
		config.triplo.append([f"TR1", f"FALSE", "SINO", config.CONTADOR_IF])
	elif(op=="Or"):
		config.triplo.append([f"TR1", f"TRUE", "SI", config.CONTADOR_IF])
		config.triplo.append([f"TR1", f"FALSE", "OR"])
	else:
		config.triplo.append(["TR1", "TRUE", "CONTINUE"])
		config.triplo.append(["TR1", "FALSE", "SINO", config.CONTADOR_IF])


""" -------------------------------------- """

def append_symbols_lexemas(operator):
	if not operator in config.lexemas:
		config.lexemas[f"{config.OPERATORS_SYMBOLS[operator]}"]=("","")