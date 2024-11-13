If(
	test=BoolOp(op=Or(), 
	values=[
	Compare(left=Name(id='_Var', ctx=Load()), ops=[Lt()],
	comparators=[Name(id='_Var2', ctx=Load())]), 
	Compare(left=Name(id='_Var1', ctx=Load()), ops=[Gt()], 
	comparators=[Constant(value=10)]), 
	Compare(left=Name(id='_Cadena', ctx=Load()), ops=[NotEq()], 
	comparators=[Constant(value='hola')])]), 
	body=[Assign(targets=[Name(id='_Varito', ctx=Store())], 
	value=Constant(value=10))], orelse=[])