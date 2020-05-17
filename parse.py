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


def verify_expr(expr):
    str = convert_lat(expr)
    fig = plt.gca(frame_on=False)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    plt.text(0.5, 0.5, str, fontsize=15, horizontalalignment='center',
                         verticalalignment='center')
    try:
        plt.savefig('check.png')
    except:
        plt.close()
        return False

    plt.close()

    return True



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
                r"\bigcup": r"\cup", r"\bigl": "", r"\Bigl": "", r"\biggl": "",
                r"\Biggl": "", r"\bigr": "", r"\Bigr": "", r"\&": "&",
                r"\biggr": "", "\Biggr": "", r"\bigm": "",
                "\Bigm": "", r"\biggm": "", r"\Biggm": "", r"\nolimits": "",
                r"\big": "", r"\Big": "", r"\bigg": "", r"\limits": "",
                r"\Bigg": "", r"\gets": r"\leftarrow", r"\mod": r"\quad mod \quad",
                r"\tbinom": r"\binom", r"\dbinom": r"\binom",
                r"\smash[b]": "", r"\smash[t]": "", r"\tag": "",
                r"\mathop": "", r"\pmb": "", r"\bmod": r"\quad mod \quad",
                r"\pmod": r"\quad mod \quad", r"\le": r"\leq", r"\right": "", r"\nonumber": ""})

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
    error = ""

    if expr[pos] == ' ':
        pos += 1
        return pos, cnt, error

    if is_double_symb(expr[pos]):
        cnt += 2
        pos += 1
    elif is_index_symb(expr[pos]):
        index_len, pos, error = cnt_index_len(expr, pos, indiv_index)
        cnt += index_len
    elif is_func(expr[pos]):
        func_len, pos, error = cnt_func_len(expr, pos, indiv_index)
        cnt += func_len
    else:
        if not expr[pos].isalpha():
            if not verify_expr(expr[pos]):
                error = "Ошибка: символ %s не поддерживается" % expr[pos]

        cnt += 1
        pos += 1

    return pos, cnt, error


def cnt_expr_len(expr):
    pos = 0
    cnt = 0
    indiv_index = list()

    while True:
        pos, cnt, error = cnt_symb_len(expr, pos, cnt, indiv_index)

        if pos == len(expr) or len(error) != 0:
            break

    return cnt, error


def find_brac_expr(expr, pos, indiv_index):
    expr_len = len(expr)

    first = pos
    pos += 1

    while expr[first: pos].count('{') != expr[first: pos].count('}'):
        if pos == expr_len:
            error = "Ошибка: пропущена закрывающая скобка }"
            return 0, pos, error

        pos += 1

    if first == pos-2:
        error = "Ошибка: пустые скобки {}"
        return 0, pos, error

    index = (first, pos - 1)

    for id, symb in enumerate(expr[first+1: pos-1]):
        if symb != ' ':
            break

        if id == (pos-first-2)-1:
            error = "Ошибка: пустые скобки {}"
            return 0, pos, error

    indiv_index.append(index)
    cnt, error = cnt_expr_len(expr[first+1: pos-1])

    return cnt, pos, error


def cnt_index_val(expr, pos, indiv_index):
    error = ""
    expr_len = len(expr)
    pos += 1

    if pos == expr_len:
        error = r"Ошибка: отсутствует значение индекса"
        return 0, pos, error

    while expr[pos] == ' ':
        pos += 1
        if pos == expr_len:
            error = r"Ошибка: отсутствует значение индекса"
            return 0, pos, error

    if expr[pos] == "{":
        index_len, pos, error = find_brac_expr(expr, pos, indiv_index)
    elif expr[pos] == '^' or expr[pos] == '_' or is_func(expr[pos]):
        error = r"Ошибка: отсутствует значение индекса"
        return 0, pos, error
    else:
        index_len = 1
        pos += 1

    return index_len, pos, error


def cnt_index_len(expr, pos, indiv_index):
    expr_len = len(expr)
    first = pos

    index_len, pos, error = cnt_index_val(expr, pos, indiv_index)

    if len(error) != 0:
        return 0, pos, error

    if pos != expr_len:
        while expr[pos] == ' ':
            pos += 1
            if pos == expr_len:
                break

    if pos != expr_len and ((expr[pos] == '^' and expr[first] == '_') or
                            (expr[pos] == '_' and expr[first] == '^')):
        up_index_len, pos, error = cnt_index_val(expr, pos, indiv_index)

        index_len = max(index_len, up_index_len)

    if pos != expr_len and ((expr[pos] == '_' and expr[first] == '_') or
                            (expr[pos] == '^' and expr[first] == '^')):
        error = r"Ошибка: указано несколько индексов одного типа"
        return 0, pos, error

    index_len = math.ceil(0.75*index_len)

    return index_len, pos, error


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


def cnt_frac_arg(expr, pos, indiv_index):
    expr_len = len(expr)

    if pos == expr_len:
        error = r"Ошибка: отсутствуют аргументы функции \frac"
        return 0, pos, error

    while expr[pos] == ' ':
        pos += 1
        if pos == expr_len:
            error = r"Ошибка: отсутствуют аргументы функции \frac"
            return 0, pos, error

    if expr[pos] != "{":
        error = r"Ошибка: отсутствуют аргументы функции \frac"
        return 0, pos, error

    return find_brac_expr(expr, pos, indiv_index)


def cnt_frac(expr, pos, indiv_index):
    numer_len, pos, error = cnt_frac_arg(expr, pos, indiv_index)

    if len(error) != 0:
        return 0, pos, error

    denom_len, pos, error = cnt_frac_arg(expr, pos, indiv_index)

    func_len = math.ceil(0.75*max(numer_len, denom_len))

    return func_len, pos, error


def cnt_func_len(expr, pos, indiv_index):
    error = ""
    letter_func = [r"\arccos", r"\cos", r"\csc", r"\hom", r"\log", r"\tan",
                   r"\arcsin", r"\cosh", r"\deg", r"\ker", r"\sec", r"\tanh",
                   r"\arctan", r"\cot", r"\dim", r"\lg", r"\sin",
                   r"\arg", r"\coth", r"\exp", r"\ln", r"\sinh"]

    first = pos
    pos += 1

    if pos == len(expr):
        error = r"Ошибка: символ \ неверно использован"

        return 0, pos, error

    func_len = 2

    while pos < len(expr) and expr[pos].isalpha():
        pos += 1

    last = pos

    if last == first + 1:
        pos += 1
        func = cp.deepcopy(expr[first:pos])

        if not verify_expr(func):
            error = "Ошибка: функция %s не поддерживается или написана неверно" % func

        func_len = 1
        return func_len, pos, error

    func = cp.deepcopy(expr[first:last])

    if func != r"\frac":
        if not verify_expr(func):
            error = "Ошибка: функция %s не поддерживается или написана неверно" % func

    if func in letter_func:
        func_len = len(func) - 1
    elif func == r"\frac":
        func_len, pos, error = cnt_frac(expr, pos, indiv_index)

    return func_len, pos, error


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
        pos, cnt, error = cnt_symb_len(expr, pos, cnt, indiv_index)

        if len(error) != 0:
            return expr_list, expr_len, error

        if cnt >= max_len:
            cur_expr, expr = split_expr(expr, pos, indiv_index)

            pos = 0
            cnt = 0

            if len(cur_expr) == 0 and cur_len == 0:
                error = "Ошибка: слишком длинная формула"
                return expr_list, expr_len, error

            str = convert_lat(cur_expr)
            expr_list.append(str)
            expr_len.append(max_len)

            max_len = 40

        if pos == len(expr):
            str = convert_lat(expr)
            expr_list.append(str)
            expr_len.append(cnt)
            break

    return expr_list, expr_len, error


def parse_str(cur_str, cur_len):
    error = ""
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
                    error = "Ошибка: слишком длинная строка"
                    return str_list, str_len, error

        if cur_len != 0:
            max_len = 40
            cur_len = 0

    return str_list, str_len, error


def split_str(str, cur_len, lat_str, len_list, is_next_line):
    error = ""
    str_len = len(str) + cur_len

    if str_len > 40:
        str_list, str_len, error = parse_str(str, cur_len)

        if len(error) != 0:
            return error

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

    return error


def parse_command(tex_command):
    error = ""
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
                error = split_str(str, 0, lat_str, len_list, True)

                if len(error) != 0:
                    return None, 0, error
            else:
                str = cp.deepcopy(tex_command[start:key[0]])
                error = split_str(str, len_list[len(lat_str) - 1], lat_str, len_list, False)

                if len(error) != 0:
                    return None, 0, error

            for id, lat in enumerate(lat_dict[key]):
                expr = func_replace(lat)
                if len(expr) > 0:
                    if id == 0:
                        expr_list, expr_len, error = parse_expr(expr, len_list[len(lat_str)-1])

                        if len(error) != 0:
                            return None, 0, error

                        for id in range(len(expr_list)):
                            if id == 0:
                                lat_str[len(lat_str) - 1] = lat_str[len(lat_str) - 1] + expr_list[id]
                                len_list[len(lat_str) - 1] = len_list[len(lat_str) - 1] + expr_len[id]
                                continue
                            lat_str.append(expr_list[id])
                            len_list.append(expr_len[id])

                    else:
                        expr_list, expr_len, error = parse_expr(expr, 0)

                        if len(error) != 0:
                            return None, 0, error

                        for id in range(len(expr_list)):
                            lat_str.append(expr_list[id])
                            len_list.append(expr_len[id])

            start = key[1]

        if start != len(tex_command):
            str = cp.deepcopy(tex_command[start:])
            error = split_str(str, len_list[len(lat_str) - 1], lat_str, len_list, False)

            if len(error) != 0:
                return None, 0, error

        fontsize = cnt_fontsize(len_list)

        return lat_str, fontsize, error
    else:
        lat_list = list()
        lat_str = list()
        find_next_line(tex_command, next_line_expr, lat_list)

        for lat in lat_list:
            expr = func_replace(lat)
            expr_list, expr_len, error = parse_expr(expr, 0)

            if len(error) != 0:
                return None, 0, error

            for id in range(len(expr_list)):
                lat_str.append(expr_list[id])
                len_list.append(expr_len[id])

        fontsize = cnt_fontsize(len_list)

        return lat_str, fontsize, error

    return None, 0, error
