from telebot import types


class Math:

    section_1_button = types.InlineKeyboardButton("Раздел 1",
                                                  callback_data="SEC_1")
    section_2_button = types.InlineKeyboardButton("Раздел 2",
                                                  callback_data="SEC_2")
    section_3_button = types.InlineKeyboardButton("Раздел 3",
                                                  callback_data="SEC_3")

    math_markup = types.InlineKeyboardMarkup()
    math_markup.add(section_1_button, section_2_button, section_3_button)

    math_ans = "Выберите раздел:"
