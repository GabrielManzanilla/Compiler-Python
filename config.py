import ast
import operator
lexemas={}
errors={}
triplo = []
REGEX=r"^_[A-Z][a-zA-Z0-9_]*$"

CONTADOR={
    "temp": 1
}

#Diccionario de los operadores
OPERATORS={
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
OPERATORS_SYMBOLS={
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.Pow: "**",
    ast.Mod: "%",
    ast.Assign: "="
}