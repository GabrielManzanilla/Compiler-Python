import ast

def extract_conditions(node):
    """Extrae condiciones individuales, incluyendo operadores lógicos."""
    conditions = []
    if isinstance(node, ast.BoolOp):  # Para operaciones lógicas como `and` y `or`
        op_type = type(node.op).__name__  # Nombre del operador (`And` o `Or`)
        for value in node.values:
            conditions.append((op_type, extract_conditions(value)))
    elif isinstance(node, ast.Compare):  # Para comparaciones simples como `x > 5`
        left = ast.dump(node.left)
        comparators = [ast.dump(c) for c in node.comparators]
        operators = [type(op).__name__ for op in node.ops]
        conditions.append((operators, left, comparators))
    print(conditions)
    return conditions

def extract_if_conditions(code):
    tree = ast.parse(code)
    conditions_data = []

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            condition = extract_conditions(node.test)
            body = [ast.dump(stmt) for stmt in node.body]
            conditions_data.append({'condition': condition, 'body': body})
    return conditions_data

# Ejemplo de uso
code = """
if x > 5 and y < 10 :
    print("Complex condition met")
"""

conditions_data = extract_if_conditions(code)

# Imprimir resultados
"""for idx, stmt in enumerate(conditions_data):
    print(f"IF Structure {idx + 1}")
    print("Condition:", stmt['condition'])
    print("Body:", stmt['body'])"""
