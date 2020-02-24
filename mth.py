from telebot import types


class Math:

    section_1_button = types.InlineKeyboardButton("Математический анализ",
                                                  callback_data="SEC_1")
    section_2_button = types.InlineKeyboardButton("Линейная алгебра",
                                                  callback_data="SEC_2")
    section_3_button = types.InlineKeyboardButton("Комплексный анализ",
                                                  callback_data="SEC_3")

    math_markup = types.InlineKeyboardMarkup(row_width=1)
    math_markup.add(section_1_button, section_2_button, section_3_button)

    math_ans = "Выберите раздел:"
