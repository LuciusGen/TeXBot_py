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

    lim_button = types.InlineKeyboardButton(Math.lim,
                                            callback_data=Math.lim)
    integral_button = types.InlineKeyboardButton(Math.integral,
                                                 callback_data=Math.integral)
    diff_button = types.InlineKeyboardButton(Math.diff,
                                             callback_data=Math.diff)
    # back_button = types.InlineKeyboardButton("🔥 " + ans.Answers.back,
    #                                         callback_data=ans.Answers.back + "back to sections")

    buttons_list = [lim_button, integral_button, diff_button]*3

    # matan_markup = types.InlineKeyboardMarkup(row_width=1)
    # matan_markup.add(lim_button, diff_button, integral_button)

    return buttons_list[first_button:last_button]


def kb_for_linal(first_button, last_button):

    matrix_button = types.InlineKeyboardButton(Math.matrix,
                                               callback_data=Math.matrix)
    determinant_button = types.InlineKeyboardButton(Math.determinant,
                                                    callback_data=Math.determinant)
    clay_button = types.InlineKeyboardButton(Math.clay,
                                             callback_data=Math.clay)
    # back_button = types.InlineKeyboardButton("🔥 " + ans.Answers.back,
    #                                         callback_data=ans.Answers.back + "back to sections")

    buttons_list = [matrix_button, determinant_button, clay_button]*6

    # linal_markup = types.InlineKeyboardMarkup(row_width=1)
    # linal_markup.add(matrix_button, determinant_button, clay_button)

    return buttons_list[first_button:last_button]


def kb_for_geom(first_button, last_button):

    scalar_button = types.InlineKeyboardButton(Math.scalar_product,
                                               callback_data=Math.scalar_product)
    plane_button = types.InlineKeyboardButton(Math.plane,
                                              callback_data=Math.plane)
    curves_button = types.InlineKeyboardButton(Math.curves,
                                               callback_data=Math.curves)
    # back_button = types.InlineKeyboardButton("🔥 " + ans.Answers.back,
    #                                         callback_data=ans.Answers.back + "back to sections")

    buttons_list = [scalar_button, plane_button, curves_button]*10

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
    topic_sizes_dict = {matan: 9, linal: 18, geom: 30}

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

    @staticmethod
    def get_topic_size(topic):
        return Math.topic_sizes_dict[topic]
