import sympy
import matplotlib.pyplot as plt
import copy as cp


def find_lat(expr, st_symb, end_symb):
    if expr.find(st_symb) != -1:
        start = expr.find(st_symb)
        end = expr[start+len(st_symb):].find(end_symb)

        if end != -1:
            lat = cp.deepcopy(expr[start+len(st_symb): start+len(st_symb)+end])
            return True, (start, start+len(st_symb)+end+len(end_symb)), lat

    return False, (0, 0), None


def find_next_line(lat, next_line_expr, lat_list):
    start = 0
    size = len(lat)

    while start < size:
        end = len(lat)
        expr_size = 0

        for expr in next_line_expr:
            ind = lat[start:].find(expr)

            if ind != -1 and ind < end:
                end = ind + start
                expr_size = len(expr)

        lat_list.append(cp.deepcopy(lat[start: end]))
        start = end + expr_size


def find_lat_list(tex_command, st_symb, end_symb, new_line, next_line_expr, lat_dict):
    pos = 0
    bool = True

    while bool:
        bool, ind, lat = find_lat(tex_command[pos:], st_symb, end_symb)
        ind = (ind[0]+pos, ind[1]+pos)
        pos = ind[1]

        if bool:
            lat_list = list()

            if new_line:
                lat_list.append("")

            find_next_line(lat, next_line_expr, lat_list)
            lat_dict[ind] = lat_list


def cnt_size(str_list):
    max_size = 50
    max_len = max(len(str) for str in str_list)
    cnt = len(str_list)
    hor_size = 800 / max_len
    ver_size = 300 / (cnt*2)

    return min(hor_size, ver_size, max_size)


def convert_lat(lat):
    non_expr = dict({"\le" :"\leq", "\ge": "\geq", "\owns": "\ni",
                "\gggtr": "\ggg", "\llless": "\lll", "\Hat": "\hat",
                "\Vec": "\vec", "\mathstrut": "", "\displaystyle": "",
                "\tfrac": "\frac", "\nolimits": "\limits", "\idotsint": "\int\dots\int",
                "\mathop": "", "\text": "", "\lvert": "|",
                "\rvert": "|", "\lVert": "\Vert", "\rVert": "\Vert",
                "\bigl": "", "\Bigl": "", "\biggl": "",
                "\Biggl": "", "\bigr": "", "\Bigr": "",
                "\biggr": "", "\Biggr": "", "\bigm": "",
                "\Bigm": "", "\biggm": "", "\Biggm": "",
                "\big": "", "\Big": "", "\bigg": "",
                "\Bigg": "", "\gets": "\leftarrow", "\mod": "\quad mod \quad",
                "\tbinom": "\binom", "\dbinom": "\binom",
                "\smash[b]": "", "\smash[t]": "", "\tag": "",
                "&": "\quad", "\mathop": "", "\pmb": "",
                "\bmod": "\quad mod \quad", "\pmod": "\quad mod \quad"})

    list_keys = list(non_expr.keys())

    for key in list_keys:
        if key == "\le" or key == "\ge":
            lat = lat.replace(non_expr[key], key)
        lat = lat.replace(key, non_expr[key])

    return sympy.latex(lat)


def parse_command(tex_command):
    lat_dict = dict()

    find_lat_list(tex_command, "$", "$", False, ["\*", "\allowbreak"], lat_dict)
    find_lat_list(tex_command, "\(", "\)", False, ["\*", "\allowbreak"], lat_dict)
    find_lat_list(tex_command, "\begin{math}", "\end{math}", False, ["\*", "\allowbreak"], lat_dict)
    find_lat_list(tex_command, "\[", "\]", True, ["\*", "\allowbreak"], lat_dict)
    find_lat_list(tex_command, "\begin{equation}", "\end{equation}", True, ["\*", "\allowbreak"], lat_dict)
    find_lat_list(tex_command, "\begin{eqnarray}", "\end{eqnarray}", True, ["\\"], lat_dict)

    if (len(lat_dict) != 0):
        lat_str = list()
        list_keys = list(lat_dict.keys())
        list_keys.sort()
        start = 0

        for key in list_keys:
            if len(lat_str) == 0:
                lat_str.append(tex_command[start:key[0]])
            else:
                lat_str[len(lat_str)-1] = lat_str[len(lat_str)-1] + tex_command[start:key[0]]

            for id, lat in enumerate(lat_dict[key]):
                expr = convert_lat(lat)
                if len(expr) > 0:
                    str = r"$%s$" % expr
                    if id == 0:
                        lat_str[len(lat_str) - 1] = lat_str[len(lat_str) - 1] + str + " "
                    else:
                        lat_str.append(str + " ")

            start = key[1]

        if start != len(tex_command):
            lat_str[len(lat_str) - 1] = lat_str[len(lat_str) - 1] + tex_command[start:]

        fontsize = cnt_size(lat_str)

        return lat_str, fontsize
    else:
        lat_list = list()
        lat_str = list()
        find_next_line(tex_command, ["\*", "\allowbreak"], lat_list)

        for lat in lat_list:
            expr = convert_lat(lat)
            str = r"$%s$" % expr
            lat_str.append(str)

        fontsize = cnt_size(lat_str)

        return lat_str, fontsize
