import sys
from main import compile
from space_cleaner import SpaceCleaner
from optimizer import CodeOptimizer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QDialog
)

class OptimizedCodeWindow(QDialog):
    """Ventana para mostrar el código optimizado"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Código Optimizado')
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()
        
        # Área de texto para el código optimizado
        self.optimized_code = QTextEdit()
        self.optimized_code.setReadOnly(True)
        layout.addWidget(self.optimized_code)
        
        self.setLayout(layout)
    
    def set_code(self, code):
        self.optimized_code.setPlainText(code)
        self.show()

class CompilerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cleaner = SpaceCleaner()
        self.optimizer = CodeOptimizer()
        self.optimized_window = OptimizedCodeWindow(self)

        # Configurar la ventana principal
        self.setWindowTitle('Compilador')
        self.setGeometry(100, 100, 800, 400)

        # Crear el layout principal
        main_layout = QHBoxLayout()

        # Crear el área de texto para el código
        self.code_to_compile= QTextEdit()
        self.code_to_compile.setPlaceholderText("El código del texto irá aquí ")

        # Crear el botón de "COMPILAR"
        compile_button = QPushButton("COMPILAR")
        compile_button.clicked.connect(self.compile_code)  # Conecta el botón con la función de compilación

        # Crear el layout para la parte izquierda (cuadro de texto y botón)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.code_to_compile)
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

        # Pestaña del "TRIPLO"
        self.triplo_tab=QWidget()
        self.tab_widget.addTab(self.triplo_tab, "TRIPLO")
        self.create_triplo_tab()

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
        self.lexemas_table = QTableWidget()
        self.lexemas_table.setRowCount(10)  # Número de filas
        self.lexemas_table.setColumnCount(3)  # Número de columnas
        self.lexemas_table.setHorizontalHeaderLabels(['Lexema', 'Tipo', 'Valor'])

        layout.addWidget(self.lexemas_table)
        self.lexemas_tab.setLayout(layout)

    def create_errores_tab(self):
        """Crea la tabla de Errores en la pestaña."""
        layout = QVBoxLayout()
        self.errores_table = QTableWidget()
        self.errores_table.setRowCount(10)  # Número de filas
        self.errores_table.setColumnCount(4)  # Número de columnas
        self.errores_table.setHorizontalHeaderLabels(['Error', 'Lexema', 'Línea', 'Descripción'])
        


        layout.addWidget(self.errores_table)
        self.errores_tab.setLayout(layout)

    def create_triplo_tab(self):
        """Crea la tabla de Triplo en la pestaña."""
        layout = QVBoxLayout()
        self.triplo_table = QTableWidget(   )
        self.triplo_table.setRowCount(30)  # Número de filas
        self.triplo_table.setColumnCount(3)  # Número de columnas
        self.triplo_table.setHorizontalHeaderLabels(['Dato Objeto', 'Dato Fuente', 'Operador'])
        


        layout.addWidget(self.triplo_table)
        self.triplo_tab.setLayout(layout)

    def compile_code(self):
        # 1. Obtener el código original
        code = self.code_to_compile.toPlainText()
        
        # 2. Optimizar el código
        optimized_code = self.optimizer.optimize(code)
        
        # 3. Rama de visualización: Limpiar espacios y mostrar
        display_code = self.cleaner.clean_for_display(optimized_code)
        self.optimized_window.set_code(display_code)
        
        # 4. Rama de compilación: Usar el código optimizado directamente
        compile(optimized_code, self.lexemas_table, self.errores_table, self.triplo_table)
app = QApplication(sys.argv)
window = CompilerWindow()
window.show()
sys.exit(app.exec_())
