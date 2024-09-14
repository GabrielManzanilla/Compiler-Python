import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
)

class CompilerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.setWindowTitle('Compilador')
        self.setGeometry(100, 100, 800, 400)

        # Crear el layout principal
        main_layout = QHBoxLayout()

        # Crear el área de texto para el código
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("El código del texto irá aquí")

        # Crear el botón de "COMPILAR"
        compile_button = QPushButton("COMPILAR")
        compile_button.clicked.connect(self.compile_code)  # Conecta el botón con la función de compilación

        # Crear el layout para la parte izquierda (cuadro de texto y botón)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.text_edit)
        left_layout.addWidget(compile_button)

        # Crear el widget de pestañas
        self.tab_widget = QTabWidget()

        # Pestaña de "Lexemas"
        self.lexemas_tab = QWidget()
        self.tab_widget.addTab(self.lexemas_tab, "Lexemas")
        self.create_lexemas_tab()

        # Pestaña de "Errores"
        self.errores_tab = QWidget()
        self.tab_widget.addTab(self.errores_tab, "Errores")
        self.create_errores_tab()

        # Añadir los layouts al layout principal
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.tab_widget)

        # Crear un widget central y establecer el layout principal
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_lexemas_tab(self):
        """Crea la tabla de Lexemas en la pestaña."""
        layout = QVBoxLayout()
        lexemas_table = QTableWidget()
        lexemas_table.setRowCount(10)  # Número de filas
        lexemas_table.setColumnCount(3)  # Número de columnas
        lexemas_table.setHorizontalHeaderLabels(['Lexema', 'Tipo', 'Valor'])
        
        # Ejemplo: Añadir una fila con datos
        lexemas_table.setItem(0, 0, QTableWidgetItem("_variable"))
        lexemas_table.setItem(0, 1, QTableWidgetItem("String"))
        lexemas_table.setItem(0, 2, QTableWidgetItem("Hola"))

        layout.addWidget(lexemas_table)
        self.lexemas_tab.setLayout(layout)

    def create_errores_tab(self):
        """Crea la tabla de Errores en la pestaña."""
        layout = QVBoxLayout()
        errores_table = QTableWidget()
        errores_table.setRowCount(10)  # Número de filas
        errores_table.setColumnCount(4)  # Número de columnas
        errores_table.setHorizontalHeaderLabels(['Error', 'Lexema', 'Línea', 'Descripción'])
        
        # Ejemplo: Añadir una fila con datos
        errores_table.setItem(0, 0, QTableWidgetItem("SyntaxError"))
        errores_table.setItem(0, 1, QTableWidgetItem("_variable"))
        errores_table.setItem(0, 2, QTableWidgetItem("1"))
        errores_table.setItem(0, 3, QTableWidgetItem("Caracter inesperado"))

        layout.addWidget(errores_table)
        self.errores_tab.setLayout(layout)

    def compile_code(self):
        """Función de ejemplo para manejar la compilación del código."""
        code = self.text_edit.toPlainText()
        print(f"Código compilado:\n{code}")
        # Aquí iría la lógica de compilación real

# Inicializar la aplicación
app = QApplication(sys.argv)
window = CompilerWindow()
window.show()
sys.exit(app.exec_())
