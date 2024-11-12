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
	config.triplo.append([f"T{config.CONTADOR["temp"]}", config.OPERATORS_SYMBOLS[operator], value_left])
	config.is_First=False

def finalice_triplo(var_id):
	config.triplo.append([var_id, f"T{config.CONTADOR["temp"]}", "="])
	config.TEMPORALS.clear()