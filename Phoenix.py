from curses.ascii import isdigit
import re

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
    return dict(typess=types,values=value)

def read(path):
    with open(path) as f:
        return f.readlines()

def check_call(token):
    if len(token) < 2:
        return False
    if token[1] == "(" and token[len(token) - 2] == ")":
        return True
    else:
        return False

def run(path):
    code = read(path)
    for b in code:
        token = re.split('([();])', b)
        if token[0] == "print":
            if check_call(token):
                print(get_types(token[2])['typess'])
            else:
                error(" 呼び出されると期待していましたが、呼び出されませんでした expect '()'")

run('./test.phe')