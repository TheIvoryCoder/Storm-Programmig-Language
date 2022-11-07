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
        else:
            curr += char
        x += 1
    tokens.append(curr)
    return tokens

def parser(fl):
    output = ""
    fl = open(fl).read()
    lines = lns(fl)
    l = 0

    STfunc = {
        "print": {
            "output_type": "run",
            "output": "print($params)"
        },
        "replace": {
            "output_type": "return",
            "output": "$parent.replace($params)"
        }
    }
    while l < len(lines):
        line = lines[l]
        tokens = lexer(line)

        # parse tokens

        t = 0
        while t < len(tokens):
            token = tokens[t]

            if token[0] == "@":
                params = " ".join(tokens[t+1:])
                token = token[1:len(token)]
                if inD (token, STfunc):
                    fn_output = STfunc[token]["output"].replace("$params", params)
                    if STfunc[token]["output_type"] == "run":
                        exec(fn_output)
            t += 1

        # parse tokens

        l += 1

    return output