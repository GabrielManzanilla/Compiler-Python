import ast
def select_text():
    file = open('./code.txt', 'r')
    code = file.read()
    lines_code=code.split("\n")
    
    return lines_code