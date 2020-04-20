import sympy
import math
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

            if new_line:
                lat_list.append("")

            lat_dict[ind] = lat_list


def cnt_fontsize(len_list):
    max_size = 50
    max_len = max(str_len for str_len in len_list)
    cnt = len(len_list)
    hor_size = 600 / max_len
    ver_size = 300 / (cnt*2)

    size = min(hor_size, ver_size, max_size)

    if size < 15:
        size = 15

    return size


def convert_lat(expr):
    if len(expr) != 0:
        lat = sympy.latex(expr)
        str = r"$%s$" % lat
    else:
        str = ""

    return str


def func_replace(lat):
    non_expr = dict({r"\leftidx": " ", r"\left": " ", r"\ge": r"\geq ", r"\owns": r"\ni ",
                r"\gggtr": r"\ggg", r"\llless": r"\lll", r"\Hat": r"\hat",
                r"\Vec": r"\vec", r"\mathstrut": "", r"\displaystyle": "",
                r"\tfrac": r"\frac", r"\nolimits": r"\limits", r"\idotsint": r"\int\dots\int",
                r"\mathop": "", r"\text": "", r"\lvert": "|",
                r"\rvert": "|", r"\lVert": r"\Vert", r"\rVert": r"\Vert",
                r"\bigl": "", r"\Bigl": "", r"\biggl": "",
                r"\Biggl": "", r"\bigr": "", r"\Bigr": "",
                r"\biggr": "", "\Biggr": "", r"\bigm": "",
                "\Bigm": "", r"\biggm": "", r"\Biggm": "", r"\nolimits": "",
                r"\big": "", r"\Big": "", r"\bigg": "", r"\limits": "",
                r"\Bigg": "", r"\gets": r"\leftarrow", r"\mod": r"\quad mod \quad",
                r"\tbinom": r"\binom", r"\dbinom": r"\binom",
                r"\smash[b]": "", r"\smash[t]": "", r"\tag": "",
                "&": r"\quad", r"\mathop": "", r"\pmb": "",
                r"\bmod": r"\quad mod \quad", r"\pmod": r"\quad mod \quad",
                r"\le": r"\leq", r"\right": "", r"\nonumber": ""})

    list_keys = list(non_expr.keys())

    for key in list_keys:
        if key == r"\le" or key == r"\ge":
            lat = lat.replace(non_expr[key], key)
        lat = lat.replace(key, non_expr[key])

    return lat


def is_index_symb(symb):
    index_symb_list = ['_', '^']

    if symb in index_symb_list:
        return True

    return False


def cnt_symb_len(expr, pos, cnt, indiv_index):
    if expr[pos] == ' ':
        pos += 1
        return pos, cnt

    if is_double_symb(expr[pos]):
        cnt += 2
        pos += 1
    elif is_index_symb(expr[pos]):
        index_len, pos = cnt_index_len(expr, pos, indiv_index)
        cnt += index_len
    elif is_func(expr[pos]):
        func_len, pos = cnt_func_len(expr, pos, indiv_index)
        cnt += func_len
    else:
        cnt += 1
        pos += 1

    return pos, cnt


def cnt_expr_len(expr):
    pos = 0
    cnt = 0
    indiv_index = list()

    while True:
        pos, cnt = cnt_symb_len(expr, pos, cnt, indiv_index)

        if pos == len(expr):
            break

    return cnt


def find_brac_expr(expr, pos, indiv_index):
    first = pos
    pos += 1

    while pos < len(expr) and expr[first: pos].count('{') != expr[first: pos].count('}'):
        pos += 1

    index = (first, pos - 1)

    indiv_index.append(index)
    cnt = cnt_expr_len(expr[first+1: pos-1])

    return cnt, pos


def cnt_index_len(expr, pos, indiv_index):
    index_len = 1
    first = pos
    pos += 1

    if expr[pos] == "{":
        index_len, pos = find_brac_expr(expr, pos, indiv_index)
    else:
        pos += 1

    if pos != len(expr) and expr[pos] == '^' and expr[first-1] == '_':
        up_index_len, pos = find_brac_expr(expr, pos, indiv_index)
        index_len = max(index_len, up_index_len)

    index_len = math.ceil(0.75*index_len)

    return index_len, pos


def is_double_symb(symb):
    doub_symb_list = ['+', '-', '*', '=', '<', '>']

    if symb in doub_symb_list:
        return True

    return False


def is_func(symb):
    func_symb = r"\ "[0]

    if symb == func_symb:
        return True

    return False


def cnt_frac(expr, pos, indiv_index):
    numer_len, pos = find_brac_expr(expr, pos, indiv_index)
    denom_len, pos = find_brac_expr(expr, pos, indiv_index)

    func_len = math.ceil(0.75*max(numer_len, denom_len))

    return func_len, pos


def cnt_func_len(expr, pos, indiv_index):
    letter_func = [r"\arccos", r"\cos", r"\csc", r"\hom", r"\log", r"\tan",
                   r"\arcsin", r"\cosh", r"\deg", r"\ker", r"\sec", r"\tanh",
                   r"\arctan", r"\cot", r"\dim", r"\lg", r"\sin",
                   r"\arg", r"\coth", r"\exp", r"\ln", r"\sinh"]

    first = pos
    pos += 1
    func_len = 2

    while pos < len(expr) and expr[pos].isalpha():
        pos += 1

    last = pos

    if last == first + 1:
        pos += 1
        func_len = 1
        return func_len, pos

    func = cp.deepcopy(expr[first:last])

    if func in letter_func:
        func_len = len(func) - 1
    elif func == r"\frac":
        func_len, pos = cnt_frac(expr, pos, indiv_index)

    return func_len, pos


def pos_in_indiv_index(cur_pos, indiv_index):
    for index in indiv_index:
        if cur_pos >= index[0] and cur_pos <= index[1]:
            return True

    return False


def split_expr(expr, pos, indiv_index):
    separ_expr_list = ["+", "-", "*", "/", "=", "<", ">", ",", r"\approx", r"equiv", r"\geq", r"\leq"]
    last_symb = 0
    separ_pos = 0

    for separ_expr in separ_expr_list:
        cur_pos = expr[:pos].rfind(separ_expr)

        while pos_in_indiv_index(cur_pos, indiv_index):
            cur_pos = expr[:cur_pos].rfind(separ_expr)

        if cur_pos > separ_pos:
            separ_pos = cur_pos
            if separ_expr == ",":
                separ_pos += 1
            last_symb = cur_pos + len(separ_expr)

    cur_expr = cp.deepcopy(expr[:last_symb])
    expr = expr[separ_pos:]

    return cur_expr, expr


def parse_expr(expr, cur_len):
    expr_list = list()
    expr_len = list()
    indiv_index = list()
    cnt = 0

    if cur_len >= 40:
        expr_list.append("")
        expr_len.append(0)
        cur_len = 0

    max_len = 40 - cur_len
    pos = 0

    while True:
        pos, cnt = cnt_symb_len(expr, pos, cnt, indiv_index)

        if cnt >= max_len:
            cur_expr, expr = split_expr(expr, pos, indiv_index)
            pos = 0
            cnt = 0

            if len(cur_expr) == 0 and cur_len == 0:
                str = convert_lat(expr)
                expr_list.append(str)
                expr_len.append(max_len)
                break

            str = convert_lat(cur_expr)
            expr_list.append(str)
            expr_len.append(max_len)

            max_len = 40

        if pos == len(expr):
            str = convert_lat(expr)
            expr_list.append(str)
            expr_len.append(cnt)
            break

    return expr_list, expr_len


def parse_str(cur_str, cur_len):
    str_list = list()
    str_len = list()
    str = cp.deepcopy(cur_str)

    if cur_len >= 40:
        str_list.append("")
        str_len.append(0)
        cur_len = 0

    max_len = 40 - cur_len

    while True:
        if len(str) <= max_len:
            str_list.append(str)
            str_len.append(len(str))
            break

        for id in reversed(range(max_len)):
            if not str[id].isalpha() and str[id] != "(" and str[id] != ")":
                str_list.append(cp.deepcopy(str[:id+1]))
                str_len.append(id+1)
                str = cp.deepcopy(str[id+1:])
                break
            if id == 0:
                if cur_len != 0:
                    str_list.append(" ")
                    str_len.append(0)
                else:
                    str_list.append(str)
                    str_len.append(len(str))

        if cur_len != 0:
            max_len = 40
            cur_len = 0

    return str_list, str_len


def split_str(str, cur_len, lat_str, len_list, is_next_line):
    str_len = len(str) + cur_len

    if str_len > 40:
        str_list, str_len = parse_str(str, cur_len)

        for id in range(len(str_list)):
            if not is_next_line:
                if id == 0:
                    lat_str[len(lat_str) - 1] = lat_str[len(lat_str) - 1] + str_list[id]
                    len_list[len(lat_str) - 1] = len_list[len(lat_str) - 1] + str_len[id]
                    continue
                lat_str.append(str_list[id])
                len_list.append(str_len[id])
            else:
                lat_str.append(str_list[id])
                len_list.append(str_len[id])
    else:
        if not is_next_line:
            lat_str[len(lat_str) - 1] = lat_str[len(lat_str) - 1] + str
            len_list[len(lat_str) - 1] = str_len
        else:
            lat_str.append(str)
            len_list.append(str_len)


def parse_command(tex_command):
    lat_dict = dict()
    len_list = list()

    next_line_expr = [r"\*", r"\allowbreak", r"\\"]

    find_lat_list(tex_command, "$", "$", False, next_line_expr, lat_dict)
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
                str = cp.deepcopy(tex_command[start:key[0]])
                split_str(str, 0, lat_str, len_list, True)
            else:
                str = cp.deepcopy(tex_command[start:key[0]])
                split_str(str, len_list[len(lat_str) - 1], lat_str, len_list, False)

            for id, lat in enumerate(lat_dict[key]):
                expr = func_replace(lat)
                if len(expr) > 0:
                    if id == 0:
                        expr_list, expr_len = parse_expr(expr, len_list[len(lat_str)-1])

                        for id in range(len(expr_list)):
                            if id == 0:
                                lat_str[len(lat_str) - 1] = lat_str[len(lat_str) - 1] + expr_list[id]
                                len_list[len(lat_str) - 1] = len_list[len(lat_str) - 1] + expr_len[id]
                                continue
                            lat_str.append(expr_list[id])
                            len_list.append(expr_len[id])

                    else:
                        expr_list, expr_len = parse_expr(expr, 0)

                        for id in range(len(expr_list)):
                            lat_str.append(expr_list[id])
                            len_list.append(expr_len[id])

            start = key[1]

        if start != len(tex_command):
            str = cp.deepcopy(tex_command[start:])
            split_str(str, len_list[len(lat_str) - 1], lat_str, len_list, False)

        fontsize = cnt_fontsize(len_list)

        return lat_str, fontsize
    else:
        lat_list = list()
        lat_str = list()
        find_next_line(tex_command, next_line_expr, lat_list)

        for lat in lat_list:
            expr = func_replace(lat)
            expr_list, expr_len = parse_expr(expr, 0)

            for id in range(len(expr_list)):
                lat_str.append(expr_list[id])
                len_list.append(expr_len[id])

        fontsize = cnt_fontsize(len_list)

        return lat_str, fontsize

    return None, 0
