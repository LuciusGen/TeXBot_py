from telebot import types



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
    lim = "Пределы и непр-ые функции."
    diff = "Дифф-ие функций."
    unc_int = "Неопределенный интеграл."
    cer_int = "Определенный интеграл."
    seq_ser = "Бесконечные посл-ти и ряды."
    fourier_ser = "Ряды Фурье."
    diff_few_var = "Дифф ф-й неск п-ых."
    doub_int = "Двойные интегралы."
    trip_int = "Тройные интегралы."
    mult_int = "Многократные интегралы."
    curv_int = "Криволинейные интегралы."
    surf_int = "Поверхностные интегралы."
    field_th = "Элементы теории поля."
    math_theme_list = [intr, lim, diff, unc_int, cer_int, seq_ser, fourier_ser, diff_few_var,
                       doub_int, trip_int, mult_int, curv_int, surf_int, field_th]

    # темы линала
    matrix = "Матрицы."
    determinant = "Определитель."
    slough = "СЛАУ."
    quad_form = "Квадратичные формы."
    lin_space = "Линейные пространства."
    eucl_space = "Евклидово пространство."
    polynom = "Многочлены."
    field = "Поля."
    group = "Группы."
    linal_theme_list = [matrix, determinant, slough, quad_form, lin_space,
                        eucl_space, polynom, field, group]

    # темы геометрии
    coord_plan = "С-мы координат на пл-ти."
    line_equat = "Линии и их уравнения."
    line_plan = "Прямая на плоскости."
    seqt_th = "Теория конических сечений."
    coord_trans = "Преобразование координат."
    det_sec_thir = "Опр-ли 2 и 3 пор-ка."
    coord_spac = "С-мы координат в пр-ве."
    vect_alg = "Векторная алгебра."
    geom_equat = "Геом-ое значение ур-ний."
    line_spac = "Прямая в пространстве."
    plan_spac = "Плоскость в пространстве."
    surf_sec = "Поверхности 2-го порядка."
    geom_theme_list = [coord_plan, line_equat, line_plan, seqt_th, coord_trans,
                       det_sec_thir, coord_spac, vect_alg, geom_equat, line_spac,
                       plan_spac, surf_sec]

    math_ans = "Выберите раздел:"

    @staticmethod
    def give_need_section(theme):
        if theme in Math.math_theme_list:
            return Math.matan
        elif theme in Math.linal_theme_list:
            return Math.linal
        elif theme in Math.geom_theme_list:
            return Math.geom

    @staticmethod
    def get_topic_size(topic):
        return Math.topic_sizes_dict[topic]
