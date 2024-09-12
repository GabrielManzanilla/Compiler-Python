from split_lines import * 
from asiggnment_variables import *
def main():
    vars={} # variable={datatype, value}
    code_lines=select_text()
    for line in code_lines:
        variable,type,dato =define_vars(line, vars)
        vars[variable]=(type, dato)
    print(vars)

if __name__=="__main__":
    main()
