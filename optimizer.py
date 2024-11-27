import ast
from typing import Optional, Dict

class CodeOptimizer:
    def __init__(self):
        self.known_values: Dict[str, int] = {}

    def _optimize_if(self, node: ast.If, indent_level: int = 0) -> str:
        """
        Optimiza una estructura if-else incluyendo anidados.
        indent_level: nivel de indentación actual
        """
        # Crear la indentación base
        base_indent = "    " * indent_level
        inner_indent = "    " * (indent_level + 1)
        
        # Optimizar la condición
        test = ast.unparse(node.test)
        
        # Optimizar el cuerpo del if
        body_lines = []
        for n in node.body:
            if isinstance(n, ast.If):
                # Recursivamente optimizar if anidados con un nivel más de indentación
                body_lines.append(self._optimize_if(n, indent_level + 1))
            elif isinstance(n, ast.Assign):
                opt = self._optimize_assignment(n)
                line = opt if opt else ast.unparse(n)
                body_lines.append(inner_indent + line)
            else:
                body_lines.append(inner_indent + ast.unparse(n))
        
        # Optimizar el cuerpo del else si existe
        else_lines = []
        if node.orelse:
            for n in node.orelse:
                if isinstance(n, ast.If):
                    # Recursivamente optimizar if anidados en el else
                    else_lines.append(self._optimize_if(n, indent_level + 1))
                elif isinstance(n, ast.Assign):
                    opt = self._optimize_assignment(n)
                    line = opt if opt else ast.unparse(n)
                    else_lines.append(inner_indent + line)
                else:
                    else_lines.append(inner_indent + ast.unparse(n))
        
        # Construir la estructura if-else optimizada
        if_str = f"{base_indent}if {test}:\n" + "\n".join(body_lines)
        if else_lines:
            if_str += f"\n{base_indent}else:\n" + "\n".join(else_lines)
        
        return if_str

    # También necesitamos modificar optimize() para iniciar con indentación 0
    def optimize(self, code: str) -> str:
        try:
            tree = ast.parse(code)
            self.known_values.clear()
            
            # Primera pasada: identificar variables con valores 0 o 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    self._identify_known_values(node)
            
            # Optimizar todo el árbol
            optimized_lines = []
            for node in tree.body:
                if isinstance(node, ast.If):
                    optimized = self._optimize_if(node, 0)
                elif isinstance(node, ast.Assign):
                    optimized = ast.unparse(node)
                    opt = self._optimize_assignment(node)
                    if opt:
                        optimized = opt
                else:
                    optimized = ast.unparse(node)
                optimized_lines.append(optimized)
            
            return '\n'.join(optimized_lines)
        except Exception as e:
            print(f"Error en optimización: {e}")
            return code
        
    def _identify_known_values(self, node: ast.Assign):
        if isinstance(node.targets[0], ast.Name):
            target = node.targets[0].id
            # Valor directo
            if isinstance(node.value, ast.Constant):
                if node.value.value in (0, 1):
                    self.known_values[target] = node.value.value
            # Variable que ya conocemos
            elif isinstance(node.value, ast.Name):
                if node.value.id in self.known_values:
                    self.known_values[target] = self.known_values[node.value.id]

    def _optimize_assignment(self, node: ast.Assign) -> Optional[str]:
        if not isinstance(node.targets[0], ast.Name):
            return None

        target = node.targets[0].id
        
        # Si es una asignación simple, mantenerla
        if isinstance(node.value, ast.Constant):
            if node.value.value in (0, 1):
                self.known_values[target] = node.value.value
            return None
            
        # Si es una operación, optimizarla
        optimized = self._optimize_operation(node.value)
        if optimized is not None:
            return f"{target} = {ast.unparse(optimized)}"
            
        return None

    def _optimize_operation(self, node: ast.AST) -> Optional[ast.AST]:
        if isinstance(node, ast.BinOp):
            # Primero optimizar recursivamente las subexpresiones
            node = self._optimize_recursive(node)
            
            # Aplicar reglas de optimización según el tipo de operación
            return self._apply_optimization_rules(node)
            
        return None

    def _optimize_recursive(self, node: ast.BinOp) -> ast.BinOp:
        # Optimizar lado izquierdo si es una operación
        if isinstance(node.left, ast.BinOp):
            node.left = self._optimize_operation(node.left)
        
        # Optimizar lado derecho si es una operación
        if isinstance(node.right, ast.BinOp):
            node.right = self._optimize_operation(node.right)

        return node

    def _apply_optimization_rules(self, node: ast.BinOp) -> Optional[ast.AST]:
        left_val = self._get_value(node.left)
        right_val = self._get_value(node.right)

        # Reglas para potencia
        if isinstance(node.op, ast.Pow):
            if left_val == 0 or left_val == 1:
                return node.left  # Eliminar la potencia
            if right_val == 1:
                return node.left

        # Reglas para multiplicación
        elif isinstance(node.op, ast.Mult):
            # Solo eliminar si el factor es 1
            if right_val == 1:
                return node.left
            if left_val == 1:
                return node.right
            # No simplificar multiplicaciones por 0

        # Reglas para división
        elif isinstance(node.op, ast.Div):
            if right_val == 1:
                return node.left
            # No simplificar divisiones por 0

        # Reglas para suma
        elif isinstance(node.op, ast.Add):
            if left_val == 0:
                return node.right
            if right_val == 0:
                return node.left

        # Reglas para resta
        elif isinstance(node.op, ast.Sub):
            if right_val == 0:
                return node.left
            if left_val == 0:
                return ast.UnaryOp(op=ast.USub(), operand=node.right)

        return node

    def _get_value(self, node: ast.AST) -> Optional[int]:
        """Obtiene el valor si es 0 o 1"""
        if isinstance(node, ast.Constant):
            return node.value if node.value in (0, 1) else None
        elif isinstance(node, ast.Name):
            return self.known_values.get(node.id)
        return None