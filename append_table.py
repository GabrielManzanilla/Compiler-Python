from PyQt5.QtWidgets import QTableWidgetItem

def fill_table_lexemas(lexemas_table, lexemas):
        lexemas_table.setHorizontalHeaderLabels(['Lexema', 'Tipo', 'Valor'])
        for row, (lexema, (tipo, valor)) in enumerate(lexemas.items()):
            lexemas_table.setItem(row, 0, QTableWidgetItem(lexema))   # Columna Lexema
            lexemas_table.setItem(row, 1, QTableWidgetItem(tipo.__name__)) if not tipo==None else lexemas_table.setItem(row, 1, QTableWidgetItem(""))  # Columna Tipo
            lexemas_table.setItem(row, 2, QTableWidgetItem(str(valor))) if not valor==None else lexemas_table.setItem(row, 2, QTableWidgetItem(""))
        
        lexemas_table.resizeColumnsToContents()

def fill_table_errors(errors_table, errors):
        errors_table.setHorizontalHeaderLabels(['Error', 'Lexema', 'Línea', 'Descripción'])
        for row, (token, (lexema, index, description)) in enumerate(errors.items()):
            errors_table.setItem(row, 0, QTableWidgetItem(token))   # Columna Lexema
            errors_table.setItem(row, 1, QTableWidgetItem(lexema)) if not type(lexema)==list else errors_table.setItem(row, 1, QTableWidgetItem(" ".join(str(lexema))))      # Columna Tipo
            errors_table.setItem(row, 2, QTableWidgetItem(str(index)))
            errors_table.setItem(row, 3, QTableWidgetItem(description))
        errors_table.resizeColumnsToContents()

