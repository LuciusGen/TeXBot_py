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

    size = min(hor_size, ver_size, max_size)

    if size < 15:
        size = 15

    return size


def convert_lat(lat):
    non_expr = dict({r"\left": "", r"\ge": r"\geq", r"\owns": r"\ni",
                r"\gggtr": r"\ggg", r"\llless": r"\lll", r"\Hat": r"\hat",
                r"\Vec": r"\vec", r"\mathstrut": "", r"\displaystyle": "",
                r"\tfrac": r"\frac", r"\nolimits": r"\limits", r"\idotsint": r"\int\dots\int",
                r"\mathop": "", r"\text": "", r"\lvert": "|",
                r"\rvert": "|", r"\lVert": r"\Vert", r"\rVert": r"\Vert",
                r"\bigl": "", r"\Bigl": "", r"\biggl": "",
                r"\Biggl": "", r"\bigr": "", r"\Bigr": "",
                r"\biggr": "", "\Biggr": "", r"\bigm": "",
                "\Bigm": "", r"\biggm": "", r"\Biggm": "",
                r"\big": "", r"\Big": "", r"\bigg": "",
                r"\Bigg": "", r"\gets": r"\leftarrow", r"\mod": r"\quad mod \quad",
                r"\tbinom": r"\binom", r"\dbinom": r"\binom",
                r"\smash[b]": "", r"\smash[t]": "", r"\tag": "",
                "&": r"\quad", r"\mathop": "", r"\pmb": "",
                r"\bmod": r"\quad mod \quad", r"\pmod": r"\quad mod \quad",
                r"\le": r"\leq", r"\right": "", r"\nonumber": ""})

    list_keys = list(non_expr.keys())

    for key in list_keys:
        if key == "\le" or key == "\ge":
            lat = lat.replace(non_expr[key], key)
        lat = lat.replace(key, non_expr[key])

    return sympy.latex(lat)


def parse_command(tex_command):
    lat_dict = dict()

    next_line_expr = [r"\*", r"\allowbreak", r"\\"]

    find_lat_list(tex_command, r"$", r"$", False, next_line_expr, lat_dict)
    find_lat_list(tex_command, r"\(", r"\)", False, next_line_expr, lat_dict)
    find_lat_list(tex_command, r"\begin{math}", r"\end{math}", False, next_line_expr, lat_dict)
    find_lat_list(tex_command, r"\[", r"\]", True, next_line_expr, lat_dict)
    find_lat_list(tex_command, r"\begin{equation}", r"\end{equation}", True, next_line_expr, lat_dict)
    find_lat_list(tex_command, r"\begin{eqnarray}", r"\end{eqnarray}", True, next_line_expr, lat_dict)

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
        find_next_line(tex_command, next_line_expr, lat_list)

        for lat in lat_list:
            expr = convert_lat(lat)
            str = r"$%s$" % expr
            lat_str.append(str)

        fontsize = cnt_size(lat_str)

        return lat_str, fontsize
