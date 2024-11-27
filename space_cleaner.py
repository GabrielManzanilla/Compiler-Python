class SpaceCleaner:
    def __init__(self):
        self.KEYWORDS = {'if', 'else:'}
        
    def clean_for_display(self, code: str) -> str:
        """
        Limpia el código para mostrar en la interfaz.
        Elimina TODOS los espacios y sangrías.
        """
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Eliminar todos los espacios excepto en strings
            cleaned = ""
            in_string = False
            quote_char = None
            
            for char in line.strip():
                if char in '"\'':
                    if not in_string:
                        in_string = True
                        quote_char = char
                    elif char == quote_char:
                        in_string = False
                    cleaned += char
                elif in_string:
                    cleaned += char
                elif not char.isspace():
                    cleaned += char
            
            if cleaned:
                cleaned_lines.append(cleaned)
        
        return '\n'.join(cleaned_lines)
    
    def clean_for_execution(self, code: str) -> str:
        """
        Prepara el código para ejecución manteniendo la estructura Python válida.
        """
        lines = code.split('\n')
        execution_lines = []
        indent_level = 0
        
        for line in lines:
            if not line.strip():
                continue
            
            cleaned_content = line.strip()
            
            # Reducir indent_level para else
            if cleaned_content.startswith('else:'):
                indent_level = max(0, indent_level - 1)
            
            # Aplicar indentación
            indented_line = '    ' * indent_level
            
            # Procesar la línea según su contenido
            if cleaned_content.startswith('if'):
                condition = cleaned_content[2:].strip()
                indented_line += 'if ' + ''.join(c for c in condition if not c.isspace())
                indent_level += 1
            elif cleaned_content.startswith('else:'):
                indented_line += 'else:'
                indent_level += 1
            else:
                # Para otras líneas, eliminar todos los espacios excepto en strings
                content = ""
                in_string = False
                quote_char = None
                
                for char in cleaned_content:
                    if char in '"\'':
                        if not in_string:
                            in_string = True
                            quote_char = char
                        elif char == quote_char:
                            in_string = False
                        content += char
                    elif in_string:
                        content += char
                    elif not char.isspace():
                        content += char
                
                indented_line += content
            
            execution_lines.append(indented_line)
        
        return '\n'.join(execution_lines)

def test_cleaner():
    cleaner = SpaceCleaner()
    
    test_code = """
_A     =     5    +    3
if    _A    >    2:
        _B    =    10
        if    _B    ==    10:
            _C    =    "PRUEBA"
        else:
            _C    =    "TEST"
else:
        _B    =    20
"""
    
    print("Original:")
    print(test_code)
    
    print("\nVersión para mostrar (sin espacios ni sangría):")
    display_version = cleaner.clean_for_display(test_code)
    print(display_version)
    
    print("\nVersión para ejecución (con estructura correcta):")
    execution_version = cleaner.clean_for_execution(test_code)
    print(execution_version)

if __name__ == "__main__":
    test_cleaner()