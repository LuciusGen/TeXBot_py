from telebot import types
import ans
from math import ceil


def generate_paged_list(topic, page):

    # numb of sections per page
    page_size = 9

    # numb of all sections in topic
    topic_len = Math.get_topic_size(topic)

    # numb of pages
    pages_numb = ceil(topic_len / page_size)

    back_button = types.InlineKeyboardButton("🔥 " + ans.Answers.back + "(" + str(page + 1) + "/" + str(pages_numb) + ")",
                                             callback_data=ans.Answers.back + "back to sections")

    if pages_numb > 1:
        if page == 0:
            where_left = pages_numb - 1
            where_right = page + 1
        elif page == pages_numb - 1:
            where_left = page - 1
            where_right = 0
        else:
            where_left = page - 1
            where_right = page + 1

        left_button = types.InlineKeyboardButton("⬅(" + str(where_left+1) + "/" + str(pages_numb) + ")",
                                                 callback_data=topic + "section." + str(where_left))

        right_button = types.InlineKeyboardButton("➡(" + str(where_right+1) + "/" + str(pages_numb) + ")",
                                                  callback_data=topic + "section." + str(where_right))
        if (page+1)*page_size <= topic_len:
            markup = generate_topic_markup(topic, page*page_size, (page+1)*page_size)
        else:
            markup = generate_topic_markup(topic, page*page_size, topic_len)
        markup.row(left_button, back_button, right_button)
    else:
        markup = generate_topic_markup(topic, page, topic_len)
        markup.add(back_button)
    return markup


def generate_topic_markup(topic, first_button, last_button):

    sect_list = list()
    markup = types.InlineKeyboardMarkup(row_width=1)

    if topic == Math.matan:
        sect_list = kb_for_matan(first_button, last_button)
    elif topic == Math.linal:
        sect_list = kb_for_linal(first_button, last_button)
    elif topic == Math.geom:
        sect_list = kb_for_geom(first_button, last_button)

    markup.add(*sect_list)
    return markup


def kb_for_matan(first_button, last_button):

    intr_button = types.InlineKeyboardButton(Math.intr,
                                             callback_data=Math.intr)
    lim_button = types.InlineKeyboardButton(Math.lim,
                                            callback_data=Math.lim)
    diff_button = types.InlineKeyboardButton(Math.diff,
                                             callback_data=Math.diff)
    unc_int_button = types.InlineKeyboardButton(Math.unc_int,
                                                callback_data=Math.unc_int)
    cer_int_button = types.InlineKeyboardButton(Math.cer_int,
                                                callback_data=Math.cer_int)
    seq_ser_button = types.InlineKeyboardButton(Math.seq_ser,
                                                callback_data=Math.seq_ser)
    fourier_ser_button = types.InlineKeyboardButton(Math.fourier_ser,
                                                    callback_data=Math.fourier_ser)
    diff_few_var_button = types.InlineKeyboardButton(Math.diff_few_var,
                                                     callback_data=Math.diff_few_var)
    doub_int_button = types.InlineKeyboardButton(Math.doub_int,
                                                 callback_data=Math.doub_int)
    trip_int_button = types.InlineKeyboardButton(Math.trip_int,
                                                 callback_data=Math.trip_int)
    mult_int_button = types.InlineKeyboardButton(Math.mult_int,
                                                 callback_data=Math.mult_int)
    curv_int_button = types.InlineKeyboardButton(Math.curv_int,
                                                 callback_data=Math.curv_int)
    surf_int_button = types.InlineKeyboardButton(Math.lim,
                                                 callback_data=Math.lim)
    field_th_button = types.InlineKeyboardButton(Math.field_th,
                                                 callback_data=Math.field_th)
    # back_button = types.InlineKeyboardButton("🔥 " + ans.Answers.back,
    #                                         callback_data=ans.Answers.back + "back to sections")

    buttons_list = [intr_button, lim_button, diff_button, unc_int_button,
                    cer_int_button, seq_ser_button, fourier_ser_button,
                    diff_few_var_button, doub_int_button, trip_int_button,
                    mult_int_button, curv_int_button, surf_int_button, field_th_button]

    # matan_markup = types.InlineKeyboardMarkup(row_width=1)
    # matan_markup.add(lim_button, diff_button, integral_button)

    return buttons_list[first_button:last_button]


def kb_for_linal(first_button, last_button):

    matrix_button = types.InlineKeyboardButton(Math.matrix,
                                               callback_data=Math.matrix)
    determinant_button = types.InlineKeyboardButton(Math.determinant,
                                                    callback_data=Math.determinant)
    slough_button = types.InlineKeyboardButton(Math.slough,
                                               callback_data=Math.slough)
    quad_form_button = types.InlineKeyboardButton(Math.quad_form,
                                                  callback_data=Math.quad_form)
    lin_space_button = types.InlineKeyboardButton(Math.lin_space,
                                                  callback_data=Math.lin_space)
    eucl_space_button = types.InlineKeyboardButton(Math.eucl_space,
                                                   callback_data=Math.eucl_space)
    polynom_button = types.InlineKeyboardButton(Math.polynom,
                                                callback_data=Math.polynom)
    field_button = types.InlineKeyboardButton(Math.field,
                                              callback_data=Math.field)
    group_button = types.InlineKeyboardButton(Math.group,
                                              callback_data=Math.group)
    # back_button = types.InlineKeyboardButton("🔥 " + ans.Answers.back,
    #                                         callback_data=ans.Answers.back + "back to sections")

    buttons_list = [matrix_button, determinant_button, slough_button,
                    quad_form_button, lin_space_button, eucl_space_button,
                    polynom_button, field_button, group_button]

    # linal_markup = types.InlineKeyboardMarkup(row_width=1)
    # linal_markup.add(matrix_button, determinant_button, clay_button)

    return buttons_list[first_button:last_button]


def kb_for_geom(first_button, last_button):

    coord_plan_button = types.InlineKeyboardButton(Math.coord_plan,
                                                   callback_data=Math.coord_plan)
    line_equat_button = types.InlineKeyboardButton(Math.line_equat,
                                                   callback_data=Math.line_equat)
    line_plan_button = types.InlineKeyboardButton(Math.line_plan,
                                                  callback_data=Math.line_plan)
    seqt_th_button = types.InlineKeyboardButton(Math.seqt_th,
                                                callback_data=Math.seqt_th)
    coord_trans_button = types.InlineKeyboardButton(Math.coord_trans,
                                                    callback_data=Math.coord_trans)
    det_sec_thir_button = types.InlineKeyboardButton(Math.det_sec_thir,
                                                     callback_data=Math.det_sec_thir)
    coord_spac_button = types.InlineKeyboardButton(Math.coord_spac,
                                                   callback_data=Math.coord_spac)
    vect_alg_button = types.InlineKeyboardButton(Math.vect_alg,
                                                 callback_data=Math.vect_alg)
    geom_equat_button = types.InlineKeyboardButton(Math.geom_equat,
                                                   callback_data=Math.geom_equat)
    line_spac_button = types.InlineKeyboardButton(Math.line_spac,
                                                  callback_data=Math.line_spac)
    plan_spac_button = types.InlineKeyboardButton(Math.plan_spac,
                                                  callback_data=Math.plan_spac)
    surf_sec_button = types.InlineKeyboardButton(Math.surf_sec,
                                                 callback_data=Math.surf_sec)
    # back_button = types.InlineKeyboardButton("🔥 " + ans.Answers.back,
    #                                         callback_data=ans.Answers.back + "back to sections")

    buttons_list = [coord_plan_button, line_equat_button, line_plan_button,
                    seqt_th_button, coord_trans_button, det_sec_thir_button,
                    coord_spac_button, vect_alg_button, geom_equat_button,
                    line_spac_button, plan_spac_button, surf_sec_button]

    # geom_markup = types.InlineKeyboardMarkup(row_width=1)
    # geom_markup.add(scalar_button, plane_button, curves_button)

    return buttons_list[first_button:last_button]


# template of callback data: "[name-of-topic].[section].[page-number]"
def start_kb_for_high_school():
    # section - отвечает за кнопку "раздел"
    start_page = 0
    sect_1_button = types.InlineKeyboardButton("📈 " + Math.matan,
                                               callback_data=Math.matan + "section." + str(start_page))
    sect_2_button = types.InlineKeyboardButton("📓 " + Math.linal,
                                               callback_data=Math.linal + "section." + str(start_page))
    sect_3_button = types.InlineKeyboardButton("📐 " + Math.geom,
                                               callback_data=Math.geom + "section." + str(start_page))

    math_mark = types.InlineKeyboardMarkup(row_width=1)
    math_mark.add(sect_1_button, sect_2_button, sect_3_button)

    return math_mark


class Math:

    # разделы
    matan = "Математический анализ."
    linal = "Линейная алгебра."
    geom = "Аналитическя геометрия."

    # number of sections in every topic
    topic_sizes_dict = {matan: 14, linal: 9, geom: 12}

    # темы матана
    intr = "Введение."
    lim = "Пределы и непрерывность функции."
    diff = "Дифференцирование функций."
    unc_int = "Неопределенный интеграл."
    cer_int = "Определенный интеграл."
    seq_ser = "Бесконечные последовательности и ряды."
    fourier_ser = "Ряды Фурье."
    diff_few_var = "Дифференцирование функций нескольких переменных."
    doub_int = "Двойные интегралы."
    trip_int = "Тройные интегралы."
    mult_int = "Многократные интегралы."
    curv_int = "Криволинейные интегралы."
    surf_int = "Поверхностные интегралы."
    field_th = "Элементы теории поля."

    # темы линала
    matrix = "Матрицы."
    determinant = "Определитель."
    slough = "Системы линейных уравнений."
    quad_form = "Квадратичные формы."
    lin_space = "Линейные пространства."
    eucl_space = "Евклидово и унитарное пространства."
    polynom = "Многочлены."
    field = "Поля."
    group = "Группы."

    # темы геометрии
    coord_plan = "Системы координат на плоскости."
    line_equat = "Линии и их уравнения."
    line_plan = "Прямая на плоскости."
    seqt_th = "Теория конических сечений."
    coord_trans = "Преобразование координат."
    det_sec_thir = "Определители 2-го и 3-го порядка."
    coord_spac = "Системы координат в пространстве."
    vect_alg = "Элементы векторной алгебры."
    geom_equat = "Геометрическое значение уравнений."
    line_spac = "Прямая в пространстве."
    plan_spac = "Плоскость в пространстве."
    surf_sec = "Кривые и поверхности 2-го порядка."

    math_ans = "Выберите раздел:"

    @staticmethod
    def get_topic_size(topic):
        return Math.topic_sizes_dict[topic]
