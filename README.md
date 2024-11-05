# How to execute this code?
1. need to change in directory Compiler-Python
2. use command `source .venv/bin/activate` to activate virtual enviroment python
3. use command `python3 main.py` to excecute the compiler
If you want to change te target code, you need enter in code.txt and write your code

# Execute ui
>[!Warning] UI is comming soon
>The ui version is in dev, but you can check using this design
>1. Enter in you virtual enviroment `source .venv/bin/activate`
>2. Use `python3 ui.py` to view the design
>
# == Comming son are linked the logical tp the ui ==

# LOGICAL
1. ui.py es la interfaz grafica del programa, al dar click en el boton COMPILAR extrae el texto del campo de texto "code_to compile"
2. dentro de esta misma se importa la funcion compile, perteneciente al archivo main.py; esta funcion se le pasa como argumento el texto y el esquema de las tablas de lexemas y errores
3. dentro del metodo, el texto se divide por cada linea a traves