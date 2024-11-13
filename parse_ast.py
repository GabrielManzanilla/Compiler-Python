import ast
import re
import config
from handler_error import append_error
from controlers import *



def Asignation(operation, index):
	var_id=operation.targets[0].id
	config.CONTADOR["temp"]=1
	if re.match(config.REGEX, var_id):
		result=INSTATNCES[type(operation.value)](operation.value, index)
		config.is_BinOp=False

		if result is None:
			append_error(var_id, index, f"Tipos incompatibles {config.INCOMPATIBLE_TYPES}")
			config.INCOMPATIBLE_TYPES.clear()

		finalice_triplo(var_id)
		config.lexemas[var_id]=(type(result).__name__, result)
	else:
		append_error(var_id, index, "REGEX incorrecto")



def BinOp(operation, index):
	config.is_BinOp=True 
	left = INSTATNCES[type(operation.left)](operation.left, index)
	right = INSTATNCES[type(operation.right)](operation.right, index)
	op_type = type(operation.op)


	right_operater=getattr(operation.right, 'id', right)
	left_operater=getattr(operation.left, 'id', left)
	try:
		result = config.OPERATORS[op_type](left, right)
	except:
		result = None
		if not config.INCOMPATIBLE_TYPES:
			config.INCOMPATIBLE_TYPES.append(right_operater)

	comparator_append_triplo(left,right, left_operater, right_operater, result, op_type)
	return result



def Constant(operation, _):
	result = operation.value
	if not config.is_BinOp:  #NO ESTOY SEGURO SI ES MEJOR AND U OR
		append_triplo_initial(result, ast.Assign)
	return result



def Name(operation, index):
	if re.match(config.REGEX, operation.id):
		try:
			(_, result)=config.lexemas[operation.id]
			if not config.is_BinOp:  #NO ESTOY SEGURO SI ES MEJOR AND U OR
				append_triplo_initial(operation.id, ast.Assign)
			return result
		except:
			append_error(operation.id, index, "Variable indefinida")
	else:
		append_error(operation.id, index, "REGEX incorrecto")
	


def If_Controler(node, index):
	config.CONTADOR["temp"]=1
	
	operation_type= type(node.test)
	INSTATNCES[operation_type](node.test, index)
	append_TR_triplo()


def BoolOp(condition, index):
	op= type(condition.op).__name__
	conditions = [INSTATNCES[type(value)](value, index) for value in condition.values]
	
	
def Compare(condition, index):
	print(ast.dump(condition))
	left=getattr(condition.left, 'id', getattr(condition.left, 'value',condition.left))
	
	operators=[config.OPERATORS_SYMBOLS[type(op)] for op in condition.ops]
	comparators=[getattr(comparator, 'id', getattr(comparator, 'value',comparator)) for comparator in condition.comparators]
	append_comparators_triplo(left, comparators[0], operators[0])




INSTATNCES={
		ast.Assign: Asignation,
		ast.BinOp: BinOp,
		ast.Constant: Constant,
		ast.Name: Name,
		ast.If: If_Controler,
		ast.Compare: Compare
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
_FLOTANTE=2.0+1+"hi"
_Var = 1+(2*5)+4
a=0
_Var2=100
if _Var <_Var2:
	_Varito=10
"""
evaluate(code)

print("\n -------------------")
for key, value in config.lexemas.items():
	print(key, value)
print("--------------------")
for key, value in config.errors.items():
	print(key, value)
print("--------------------")
for i in config.triplo:
	print(i)