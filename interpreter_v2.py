import regex

def dictContains(item, dictionary):
    if item in dictionary:
        return True
    else:
        return False

def canEval(x):
    try:
        eval(x)
        return True
    except:
        return False

def set_tokens(fl):
    tokens = []
    current_token = ""
    prev = ""
    quote_count = 0
    par_count = 0
    for l in range(len(fl)):
        line = fl[l].replace('\n', '')
        line = list(line);

        for t in range(len(line)):
            c = line[t]

            if c == '"' or c == "'":
                quote_count += 1
            if quote_count % 2 == 0:
                inside_quotes = False
            else:
                inside_quotes = True

            if c == '(' or c == ")":
                par_count += 1
            if par_count % 2 == 0:
                inside_par = False
            else:
                inside_par = True

            if prev == "}" or prev == "{" or c == ";" or prev == ";" or prev=="(" or prev==")" or c == "(" or c == ")" or c == '"' or prev == '"':
                tokens.append(current_token)
                current_token = ""
            current_token = current_token + str(c)

            if c == " " and inside_quotes == False and inside_par == False:
                tokens.append(current_token[:-1])
                current_token = ""

            prev = c

    tokens.append(current_token)
    return tokens

def parse_file(fl):
    Output = ""

    fl = open(fl).readlines()
    fl = [ele for ele in fl if ele.strip()]
    tokens = set_tokens(fl)
    tokens = [ele for ele in tokens if ele.strip()]
    Vars = {}
    for t in range(len(tokens)):
        token = tokens[t]
        if token == "=":
            # variable
            var_name = tokens[t-1]
            var_type = tokens[t-2]
            if var_type == "string":
                var_val = tokens[t+3]
            elif var_type == "calc":
                if " " in tokens[t+2]:
                    this_t = tokens[t+2].split(" ")
                    str_finish = ""
                    for a in this_t:
                        if dictContains(a, Vars):
                            str_finish = str_finish + str(Vars[a]["value"])
                        else:
                            str_finish = str_finish + a
                var_val = str(eval(str(str_finish)))
            elif var_type == "ref":
                var_val = tokens[t+1]
                if dictContains(var_val, Vars):
                    var_val = Vars[var_val]["value"]
            else:
                var_val = tokens[t+1]
            if tokens[t-3] == "const":
                var_locked = True
            else:
                var_locked = False
            Vars[var_name] = {
                "type": var_type,
                "value": var_val,
                "locked": var_locked
            }

        elif token == "prt":
            if " " in tokens[t+2]:
                this_t = tokens[t+2].split(" ")
                str_finish = ""
                for a in this_t:
                    if dictContains(a, Vars):
                        str_finish = str_finish + str(Vars[a]["value"])
                    else:
                        str_finish = str_finish + a
                prt_val = str(eval(str_finish))
            elif tokens[t+2] == '"':
                prt_type = "string"
                prt_val = tokens[t+3]
            elif tokens[t+2].isdigit():
                prt_type = "int"
                prt_val = tokens[t+2]
            elif dictContains(tokens[t+2], Vars):
                prt_type = "ref"
                prt_val = Vars[tokens[t+2]]["value"]
            elif canEval(str(tokens[t+2])):
                prt_type = "float"
                prt_val = str(eval(str(tokens[t+2])))
            else:
                prt_val = "None"

            Output = Output + prt_val + "\n"

    return Output

"""
const int myInt = 100;
string myString = "my name";

prt(myInt);
prt("hello world!");
prt(myString)
prt(2 + 5)

main();

...

['const','int','myInt','=','100',';','string','myString','=','','"','my name','"',';', 'prt','(', 'myInt', ')',';','prt','(','"','hello world!','"',')',';','prt','(','myString',')','prt','(','2','+','5',')','main','(',')',';'] // {'myInt': {'type': 'int', 'value': '100', 'locked': True}, 'myString': {'type': 'string', 'value': 'my name', 'locked': False}}


int x = 5;
int y = 7;

fn add (a, b) 
    calc return a + b;
}

int z = add(x,y);
prt(z);
"""

