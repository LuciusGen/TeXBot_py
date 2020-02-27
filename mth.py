from telebot import types
import ans


def kb_for_matan():
    lim_button = types.InlineKeyboardButton(Math.lim,
                                            callback_data=Math.lim)
    integral_button = types.InlineKeyboardButton(Math.integral,
                                                 callback_data=Math.integral)
    diff_button = types.InlineKeyboardButton(Math.diff,
                                             callback_data=Math.diff)

    matan_markup = types.InlineKeyboardMarkup(row_width=1)
    matan_markup.add(lim_button, diff_button, integral_button)

    return matan_markup


def kb_for_linal():
    matrix_button = types.InlineKeyboardButton(Math.matrix,
                                               callback_data=Math.matrix)
    determinant_button = types.InlineKeyboardButton(Math.determinant,
                                                    callback_data=Math.determinant)
    clay_button = types.InlineKeyboardButton(Math.clay,
                                             callback_data=Math.clay)

    linal_markup = types.InlineKeyboardMarkup(row_width=1)
    linal_markup.add(matrix_button, determinant_button, clay_button)

    return linal_markup


def kb_for_geom():
    scalar_button = types.InlineKeyboardButton(Math.scalar_product,
                                               callback_data=Math.scalar_product)
    plane_button = types.InlineKeyboardButton(Math.plane,
                                              callback_data=Math.plane)
    curves_button = types.InlineKeyboardButton(Math.curves,
                                               callback_data=Math.curves)

    geom_markup = types.InlineKeyboardMarkup(row_width=1)
    geom_markup.add(scalar_button, plane_button, curves_button)

    return geom_markup


def start_kb_for_high_school():
    # section - отвечает за кнопку "раздел"

    sect_1_button = types.InlineKeyboardButton(Math.matan,
                                               callback_data=Math.matan + "section")
    sect_2_button = types.InlineKeyboardButton(Math.linal,
                                               callback_data=Math.linal + "section")
    sect_3_button = types.InlineKeyboardButton(Math.geom,
                                               callback_data=Math.geom + "section")

    math_mark = types.InlineKeyboardMarkup(row_width=1)
    math_mark.add(sect_1_button, sect_2_button, sect_3_button)

    return math_mark


class Math:
    # разделы
    matan = "Математический анализ."
    linal = "Линейная алгебра."
    geom = "Аналитическя геометрия."

    # темы матана
    lim = "Пределы."
    integral = "Интегралы."
    diff = "Производные."

    # темы линала
    matrix = "Матрицы."
    determinant = "Определители."
    clay = "Слау."

    # темы геометрии
    scalar_product = "Скалярное произведение."
    curves = "Кривые на плоскости."
    plane = "Плоскость."

    math_ans = "Выберите раздел:"
