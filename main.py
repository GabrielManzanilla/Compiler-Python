from split_lines import * 
from asiggnment_variables import *
import config
def main():
    
    code_lines=select_text()
    for index, line in enumerate(code_lines):
        identify_operation(line, index+1)
    print(config.lexemas)
    print(config.errors)
if __name__=="__main__":
    main()
