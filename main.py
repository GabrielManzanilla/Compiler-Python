from split_lines import * 
from asiggnment_variables import *
import config
import time, os


def main():
    
    code_lines=select_text()
    for index, line in enumerate(code_lines):
        print("")
        print(config.lexemas)
        print("")
        print(config.errors)
        time.sleep(2)
        os.system("cls") if os.name=="nt" else os.system("clear")
        identify_operation(line, index+1)

if __name__=="__main__":
    main()
