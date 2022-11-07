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
            "params": {
                "length": 1,
                "type": {'1': ["string", "int", "float", "bool"]},
            },
            "output_type": "run",
            "output": "print('$params[0]')"
        },
        "replace": {
            "params": {
                "length": 2,
                "type": {'1': 'string', '2': 'string'}
            },
            "output_type": "return",
            "output": "$parent.replace($params[0], $params[1])"
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
                token = token[1:len(token)]
                if inD (token, STfunc):
                    exec(STfunc[token]["output"])
            t += 1

        # parse tokens

        l += 1

    return output