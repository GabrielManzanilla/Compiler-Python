import ast
import re
import config
from handler_error import append_error
from controlers import *
from admin_jumps import *


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
	if not (config.is_BinOp or config.is_Comparator):  #NO ESTOY SEGURO SI ES MEJOR AND U OR
		append_triplo_initial(str(result), ast.Assign)
	return result



def Name(operation, index):
	if re.match(config.REGEX, operation.id):
		try:
			(_, result)=config.lexemas[operation.id]
			if not (config.is_BinOp or config.is_Comparator):  #NO ESTOY SEGURO SI ES MEJOR AND U OR
				append_triplo_initial(operation.id, ast.Assign)
			return result
		except:
			append_error(operation.id, index, "Variable indefinida")
	else:
		append_error(operation.id, index, "REGEX incorrecto")
	


def If_Controler(node, index):
	config.CONTADOR["temp"]=1
	config.CONTADOR_IF+=1
	#Parte de la condicion del if
	config.is_Comparator=True
	operation_type= type(node.test)
	INSTATNCES[operation_type](node.test, index)
	append_TR_triplo()
	#Parte del cuerpo del if
	config.is_Comparator=False
	config.triplo.append([f"", "BEGINIF", "JR", config.CONTADOR_IF])
	for index_if,value in enumerate(node.body):
		INSTATNCES[type(value)](value, index+index_if)
	
	#Parte del cuerpo del else
	if node.orelse:
		config.triplo.append([f"", "ENDIF", "JR", config.CONTADOR_IF])
		for index_else,value in enumerate(node.orelse):
			INSTATNCES[type(value)](value, index+index_else)
		config.triplo.append([f"", "ENDELSE", "JR", config.CONTADOR_IF])

		add_jumps_in_If(config.triplo)
		add_jumps_in_Logic_Operators(config.triplo)
	else:
		jmp_only_If(config.triplo)

	config.CONTADOR_IF-=1




def BoolOp(condition, index):
	config.is_BoolOp=True
	op= type(condition.op).__name__ #Obtiene el tipo de operador
	[INSTATNCES[type(value)](value, index) for value in condition.values]
	for i in range(len(condition.values)):
		append_comparators_triplo(config.CONDITIONS[i][0], config.CONDITIONS[i][1], config.CONDITIONS[i][2])
		print(config.CONDITIONS[i])
		if i+1 < len(condition.values):
			append_TR_triplo(op)
		config.is_BoolOp=False
	config.CONDITIONS.clear()
		
	
	
	
def Compare(condition, index):
	left=getattr(condition.left, 'id', getattr(condition.left, 'value',condition.left))
	INSTATNCES[type(condition.left)](condition.left, index)
	
	operators=[config.OPERATORS_SYMBOLS[type(op)] for op in condition.ops]
	comparators=[]
	for comparator in condition.comparators:
		INSTATNCES[type(comparator)](comparator, index)
		nodo=getattr(comparator, 'id', getattr(comparator, 'value',comparator))
		comparators.append(nodo)
	
	if config.is_BoolOp:
		config.CONDITIONS.append([left, comparators[0], operators[0]])
	else:
		append_comparators_triplo(left, comparators[0], operators[0])

		




INSTATNCES={
		ast.Assign: Asignation,
		ast.BinOp: BinOp,
		ast.Constant: Constant,
		ast.Name: Name,
		ast.If: If_Controler,
		ast.BoolOp: BoolOp,
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

_Var = 4
_Var2=100
if _Var <_Var2 or _Var<10:
	if _Var1<10:
		_Varito=10
	else:
		_Varito=5
else:
	_Varito=20

if _Varito<4:
	_Varito=10

_Jamon=10
_Papilla=10+1

"""
evaluate(code)

print("\n -------------------")
for key, value in config.lexemas.items():
	print(key, value)
print("--------------------")
for key, value in config.errors.items():
	print(key, value)
print("--------------------")
for i,triplo in enumerate(config.triplo):
	print(i+1, "--------", triplo)