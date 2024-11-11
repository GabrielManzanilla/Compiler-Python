import ast
import re
import config
from handler_error import append_error



def Asignation(operation, index):
	var_id=operation.targets[0].id
	if re.match(config.REGEX, var_id):
		result=INSTATNCES[type(operation.value)](operation.value, index)

		if result is None:
			append_error(var_id, index, f"Tipos incompatibles {config.INCOMPATIBLE_TYPES}")
			config.INCOMPATIBLE_TYPES.clear()
		config.lexemas[var_id]=(type(result), result)
	else:
		append_error(var_id, index, "REGEX incorrecto")



def BinOp(operation, index):
	left = INSTATNCES[type(operation.left)](operation.left, index)
	right = INSTATNCES[type(operation.right)](operation.right, index)
	op_type = type(operation.op)
	try:
		result = config.OPERATORS[op_type](left, right)
	except:
		result = None
		if not config.INCOMPATIBLE_TYPES:
			try:
				config.INCOMPATIBLE_TYPES.append(operation.right.id)
			except:
				config.INCOMPATIBLE_TYPES.append(right)
	return result
def Constant(operation, _):
	return operation.value



def Name(operation, index):
	if re.match(config.REGEX, operation.id):
		try:
			(_, result)=config.lexemas[operation.id]
			return result
		except:
			append_error(operation.id, index, "Variable indefinida")
	else:
		append_error(operation.id, index, "REGEX incorrecto")
	


INSTATNCES={
		ast.Assign: Asignation,
		ast.BinOp: BinOp,
		ast.Constant: Constant,
		ast.Name: Name,
}

def evaluate(code):
	operations = ast.parse(code, mode='exec') #convierte el codigo a un arbol de operaciones

	for index, operation in enumerate(operations.body):
		operation_type = type(operation)
		INSTATNCES[operation_type](operation, index)

		#Itera cada linea de codigo y evalua su tipo de operacion



"""   ---SECCION PARA HACER PRUEBAS CON CONSOLA---   """

code="""
_Cadena="hola"
_FLOTANTE=2.0+1
_Var = "hi"+_Cadena+2.0
a=0
"""
evaluate(code)

for key, value in config.lexemas.items():
	print(key, value)

print("--------------------")
for key, value in config.errors.items():
	print(key, value)
