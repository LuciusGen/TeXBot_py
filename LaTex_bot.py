# -*- coding: utf-8 -*-
import telebot
import mth
from conf import Config
from ans import Answers
from mth import Math
from telebot import types

url_donate_path = 'https://money.yandex.ru/to/4100111962148422'
bot_token = Config.get_token()

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, Answers.start_ans, reply_markup=Answers.main_markup, parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '📚Вышмат':
        bot.send_message(message.chat.id, Math.math_ans, reply_markup=mth.start_kb_for_high_school())
    elif message.text == '💰Помощь проекту':
        bot.send_message(message.chat.id, url_donate_path)
    else:
        bot.send_message(message.chat.id, "Данная фича в разработке, пожалуйста, выберите другую кнопу.")


@bot.callback_query_handler(func=lambda call: call.data.endswith('section'))
def query_handler(call):
    kb = types.InlineKeyboardMarkup()
    data = call.data[:-7]
    if data == Math.matan:
        kb = mth.kb_for_matan()

    elif data == Math.linal:
        kb = mth.kb_for_linal()

    elif data == Math.geom:
        kb = mth.kb_for_geom()

    bot.send_message(call.message.chat.id,
                     "Вы выбрали раздел: " + data + "\nТеперь выберите тему.", reply_markup=kb
                     )


bot.polling(none_stop=False, interval=1, timeout=20)
