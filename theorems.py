import _sqlite3

import ans
from math import ceil
from telebot import types


def generate_paged_list_theorems(theme, page):
    # numb of sections per page
    page_size = 9
    theorems_from_database(theme)

    # numb of all sections in topic
    topic_len = len(matan_theorems_buttons)

    # numb of pages
    pages_numb = ceil(topic_len / page_size)

    back_button = types.InlineKeyboardButton(
        "🔥 " + ans.Answers.back + "(" + str(page + 1) + "/" + str(pages_numb) + ")",
        callback_data=theme + '.' + "back to themes")

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

        left_button = types.InlineKeyboardButton("⬅(" + str(where_left + 1) + "/" + str(pages_numb) + ")",
                                                 callback_data=theme + "theorem." + str(where_left))

        right_button = types.InlineKeyboardButton("➡(" + str(where_right + 1) + "/" + str(pages_numb) + ")",
                                                  callback_data=theme + "theorem." + str(where_right))
        if (page + 1) * page_size <= topic_len:
            markup = generate_theorems(page * page_size, (page + 1) * page_size)
        else:
            markup = generate_theorems(page * page_size, topic_len)
        markup.row(left_button, back_button, right_button)
    else:
        markup = generate_theorems(page, topic_len, theme)
        markup.add(back_button)
    return markup


def theorems_from_database(theme):
    matan_theorems_buttons.clear()
    try:
        conn = _sqlite3.connect('database.db')  # create data base
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM " + "[" + theme + "]")
        math = cursor.fetchall()
        conn.close()

        for i in math:
            theorem = i[0]
            matan_theorems_buttons.append(types.InlineKeyboardButton(theorem,
                                                                 callback_data="T." + theme + i[1]))
    except:
        conn.close()

        for i in range(6):
            matan_theorems_buttons.append(types.InlineKeyboardButton("theorem" + str(i),
                                                                     callback_data="theorem" + str(i)))


def generate_theorems(first_button, last_button, theme):  # so far, let's change the future
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*(matan_theorems_buttons[first_button:last_button]))
    return markup


matan_theorems_buttons = []