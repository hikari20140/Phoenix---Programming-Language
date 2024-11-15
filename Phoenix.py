from curses.ascii import isdigit
import re

var = []
var_i = []
var_t = []

def error(strs):
    print("error!" + strs)

def get_types(strs):
    types = "null"
    value = "null"
    if (strs[0] == '"' or strs[len(strs) -1] == '"') or (strs[0] == "'" or strs[len(strs) -1] == "'"):
        types = "string"
        value = strs[1:len(strs) - 1]
    elif strs.isdigit():
        if '.' in strs:
            if int(strs) / 2 > 0 or int(strs) == 0.0:
                types = "int"
                value = strs

        elif int(strs) / 2 > 0 or int(strs) == 0:
            types = "int"
            value = strs
    elif strs[0] == "[" and strs[len(strs) - 1] == "]":
        if strs[1] == "~":
            types = "list"
            value = strs
        else:
            h = ""
            for i in range(1, len(strs) - 1):
                h += strs[i]
            b = get_types(list(h)[0])
            for bs in list(h):
                if(not b['typess'] == get_types(bs)['typess'] and not get_types(bs)['typess'] == "null"):
                    error(" " + b['typess'] + "型が期待されましたが、" + get_types(bs)['typess'] + "型が出力されました。")
            types = "array<" + str(b['typess']) + ">"
            value = strs
    elif strs in var:
        types = var_t[var.index(strs)]
        value = var_i[var.index(strs)]
    elif strs[len(strs) - 1] == "]":
        bb = strs.split('[')
        print(bb)
        varl = get_types(bb[0])
        print(var, var_i, var_t)
        if "array" in varl['typess'] or "list" in varl['typess']:
            if "list" in varl['typess']:
                m = list(strs[1:len(strs) - 1])[(bb[1])[0:len(bb[1]) - 1]]
                types = get_types(m)
                value = types['values']
                types = types['typess']
            else:
                m = list(strs)[(bb[1])[0:len(bb[1]) - 1]]
                types = get_types(m)
                value = types['values']
                types = types['typess']
    return dict(typess=types,values=value)

def read(path):
    with open(path) as f:
        return f.readlines()

def check_call(token):
    if len(token) < 2:
        return False
    if '(' in token and ')' in token:
        return True
    else:
        return False

def run(path):
    code = read(path)
    passed = False
    for b in code:
        token = re.split('([();]| )', b)
        m = 0
        for n in token:
            if not n == None:
                token[m] = n.replace('\n', '')
                m += 1
        print(token)
        if token[0] == "print":
            if check_call(token):
                b = token.index(')')
                strings = token[2:b]
                c = ""
                for m in strings:
                    c += m
                print(get_types(c)['values'])
            else:
                error(" 呼び出されると期待していましたが、呼び出されませんでした expect '()'")
        elif token[0] == "var" or token[0] == "let":
            var.append(token[2])
            if token[4] == "=":
                var_i.append(get_types(token[6])['values'])
                var_t.append(get_types(token[6])['typess'])
            else:
                var_i.append("null")
                var_t.append("any")
        elif b.startswith("//"):
            passed = True  
        else:
            if not passed:
                error(" 関数がありません")
            else:
                passed = False


run('./test.phe')
