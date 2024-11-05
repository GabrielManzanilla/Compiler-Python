import ast

def extract_if_else_statements(code):
    # Parsear el código y generar el árbol de sintaxis
    tree = ast.parse(code)
    
    # Función para recorrer nodos y extraer if-else
    if_else_statements = []

    for node in ast.walk(tree):
        if isinstance(node, ast.If):  # Detecta el nodo if
            # Extraer condición
            condition = ast.dump(node.test)
            
            # Extraer el cuerpo del if
            if_body = [ast.dump(stmt) for stmt in node.body]
            
            # Extraer el cuerpo del else (si existe)
            else_body = [ast.dump(stmt) for stmt in node.orelse] if node.orelse else None
            
            # Guardar la estructura if-else
            if_else_statements.append({
                'condition': condition,
                'if_body': if_body,
                'else_body': else_body
            })
    
    return if_else_statements

# Ejemplo de uso
code = """
x = 10
if x > 5:
    print("x is greater than 5")
else:
    print("x is 5 or less")
"""

if_else_statements = extract_if_else_statements(code)

# Imprimir los resultados
for idx, stmt in enumerate(if_else_statements):
    print(f"IF-ELSE Structure {idx + 1}")
    print("Condition:", stmt['condition'])
    print("If Body:", stmt['if_body'])
    print("Else Body:", stmt['else_body'])
    print()
