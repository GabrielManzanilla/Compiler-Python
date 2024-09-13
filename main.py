from split_lines import * 
from asiggnment_variables import *
def main():
    vars={} # variable={datatype, value}
    code_lines=select_text()
    for line in code_lines:
        identify_operation(line)
    print(vars)

if __name__=="__main__":
    main()
