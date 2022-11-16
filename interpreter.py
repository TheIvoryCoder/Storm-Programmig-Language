import regex as re

def inD(i,d):
    if i in d:
        return True
    else:
        return False

def lns(c):
    c = re.sub(r"([--]).*?\1(.*)", "", c)
    c = c.replace("    ", "")
    c = c.split("\n")
    c = [l for l in c if l]
    return c

def lexer(c):
    c = list(c)
    tokens = []
    curr = ""
    q_count = 0
    x = 0
    prev = ""
    while x < len(c):
        char = c[x]

        if char == '"' or char == "'":
            q_count += 1
        if q_count % 2 == 0:
            in_q = False
        else:
            in_q = True

        if char == ' ' and in_q == False:
            tokens.append(curr)
            curr = ""
        elif char == ')' or prev == ")" or char == "(" or prev == "(":
            tokens.append(curr)
            curr = char
        else:
            curr += char

        prev = char
        x += 1
    tokens.append(curr)
    return tokens

def parser(fl):
    fl = open(fl).read()
    lines = lns(fl)
    l = 0

    STfunc = {
        "print": {
            "output_type": "run",
            "output": "print($params)"
        }
    }
    TempVars = {}
    Vars = {}
    Funcs = {}
    while l < len(lines):
        line = lines[l]
        l += 1
        if line[0] != "#":
            tokens = lexer(line)

            # parse tokens

            t = 0
            while t < len(tokens):
                token = tokens[t]
                if token[0] == "@":        
                    params = tokens[t+1:]
                    token = token[1:len(token)]
                    if inD (token, STfunc):
                        fparams = ""
                        for param in params:
                            param = param.replace("$", "")
                            if inD(param, Vars):
                                param = Vars[param]["value"]
                            fparams += param
                        fn_output = STfunc[token]["output"].replace("$params", fparams)
                        if "$parent" in fn_output:
                            fn_output = fn_output.replace("$parent", param_list)
                        exec(fn_output)
                    else:
                        if line[-1] == "{":
                            name = token.replace("@","")
                            params = tokens[t + 2]
                            print(params)
                            Funcs[name] = {
                                "line": l
                        }


                elif token[0] == "$":
                    val = tokens[t+1:]
                    val = " ".join(val).replace("=","")
                    name = token.replace("$", "")
                    Vars[name] = {
                        "value": val
                    }
                t += 1
    
        # parse tokens
    print(Funcs)