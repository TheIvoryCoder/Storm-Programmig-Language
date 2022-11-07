import regex
import TIC

# Checks if item is in array
def contains(item, array):
    for i in array:
        if i == item:
            return True
    return False

# Checks if item is in dictionary
def dictContains(item, dictionary):
    if item in dictionary:
        return True
    else:
        return False

def evaluable(x):
    try:
        eval(x)
        return True
    except:
        return False

def parse_file(fl):
    Output = ""
    Syntax = ["=","print"]
    Special = regex.compile('[@_!#$%^&*()<>?/\|}{~:]')
    Vars = {
    }
    
    lines = open(fl).readlines()
    for l in range(len(lines)):
        line = lines[l]
        line = line.replace('\n','').replace('\t','')
        tokens = regex.split(r"""\s+(?=(?:[^"]*"[^"]*")*[^"]*$)(?=(?:[^"]*'[^']*')*[^']*$)(?=[^()]*(?:\(|$))""", line)

        for t in range(len(tokens)):
            token = tokens[t]

            if token == "=":
                var_name = tokens[t - 1]
                var_val = tokens[tokens.index(token)+1:]
                var_val = " ".join(var_val)
                if var_name == "":
                    return "Syntax Error: on line "+str(l)+" near '"+token+" "+tokens[t+1]+"'"
                elif contains(var_name, Syntax):
                    return "Syntax Error: on line "+str(l)+" near '"+token+" "+tokens[t+1]+"'\n Cannot name variable '"+var_name+"'"
                elif Special.search(var_name) != None:
                    return "Syntax Error: on line "+str(l)+" near '"+tokens[t-1]+" "+token+" "+tokens[t+1]+"'\n Variable name cannot include '"+Special.search(var_name).group()+"'"
                elif var_val == "":
                    return "Syntax Error: on line "+str(l)+" near '"+tokens[t-1]+" "+token+"'"
                elif contains(var_val, Syntax):
                    return "Syntax Error: on line "+str(l)+" near '"+token+" "+tokens[t+1]+"'\n Cannot set value of variable to '"+var_name+"'"
                else:
                    if list(var_val)[0] == '"' and list(var_val)[-1] == '"':
                        var_type = "string"
                    elif var_val.isdigit():
                        var_type = "int"
                    elif "." in var_val:
                        var_type = "float"
                    elif dictContains(var_val, Vars):
                        var_type = "var"
                    elif evaluable(var_val):
                        var_val = str(eval(str(var_val)))
                        if str(var_val).isdigit():
                            var_type = "int"
                        else:
                            var_type = "float"
                    else:
                        return "Syntax Error: on line "+str(l)+" near '"+token+"'\n Variable must be of type String, Int, Float, Or Var"
                    
                    Vars[var_name] = {
                        "name": var_name,
                        "value": var_val,
                        "type": var_type
                    }

            elif "print(" in token or token == "print":
                if "(" in token and ")" in token:
                    print_val = token.replace("print(", "")
                    print_val = print_val[:-1]
                elif t + 1 < len(tokens) and "(" in tokens[t+1]:
                    print_val = tokens[t + 1][1:len(tokens[t+1])]
                    print_val = print_val[:-1]
                else:
                    return "Syntax Error: on line "+str(l)+" near '"+token+"'"
                if (list(print_val)[0] == '"' and list(print_val)[-1] == '"'):
                    Output = Output + print_val.replace('"', '')
                else:
                    print_stmt = regex.split(r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)(?=[^()]*(?:\(|$))', print_val)
                    print_sub = ""

                    # replace variables with their values

                    for pt in print_stmt:
                        if dictContains(pt, Vars):
                            pt = Vars[pt]["value"]
                        print_sub += pt
                        
                    print_val = eval(print_sub)
                    Output = Output + str(print_val)
                    
    return Output
    
