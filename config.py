import ast
import operator
""" GLOBALS SINCE UNITY 1"""
lexemas={}
errors={}
REGEX=r"^_[A-Z][a-zA-Z0-9_]*$" #REGEX de nuestra variable

OPERATORS={                   #Diccionario de los operadores
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

INCOMPATIBLE_TYPES=[]

OPERATORS_SYMBOLS={
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.Pow: "**",
    ast.Mod: "%",
    ast.Assign: "="
}
CONTADOR={
    "temp": 1,
    "operator_comparator":None
}

triplo = []
JUMPS=[]
INDEX_JMP=[]