from telebot import types
from keyboards import Keyboard
from LaTex_bot import *


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == Keyboard.button_donate:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url=Keyboard.url_donate_path)
        keyboard.add(url_button)
        bot.send_message(call.message.chat.id, "Привет! Нажми на кнопку и перейди на сайт для оплаты", reply_markup=keyboard)
    elif call.data == Keyboard.button_school:
        pass
    elif call.data == Keyboard.button_reference:
        pass
    elif call.data == Keyboard.button_recommend:
        pass

