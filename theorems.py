import _sqlite3

from telebot import types


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
