import ans
from mth import Math
from math import ceil
from telebot import types


def generate_paged_list_theorems(theme, page):
    # numb of sections per page
    page_size = 2

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
        markup = generate_theorems(page, topic_len)
        markup.add(back_button)
    return markup


def generate_theorems(first_button, last_button):  # so far, let's change the future
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*(matan_theorems_buttons[first_button:last_button]))
    return markup


#  теоремы матана(пока толкьо интерейс)
theorem1 = "Теорема 1"
theorem2 = "Теорема 2"
theorem3 = "Теорема 3"
theorem4 = "Теорема 4"
theorem5 = "Теорема 5"
theorem6 = "Теорема 6"
theorem1_button = types.InlineKeyboardButton(theorem1,
                                             callback_data=theorem1)
theorem2_button = types.InlineKeyboardButton(theorem2,
                                             callback_data=theorem2)
theorem3_button = types.InlineKeyboardButton(theorem3,
                                             callback_data=theorem3)
theorem4_button = types.InlineKeyboardButton(theorem4,
                                             callback_data=theorem4)
theorem5_button = types.InlineKeyboardButton(theorem5,
                                             callback_data=theorem5)
theorem6_button = types.InlineKeyboardButton(theorem6,
                                             callback_data=theorem6)
matan_theorems_buttons = [theorem1_button, theorem2_button, theorem3_button,
                          theorem4_button, theorem5_button, theorem6_button]
