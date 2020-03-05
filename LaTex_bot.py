# -*- coding: utf-8 -*-
import telebot
from telebot import types
import re

import mth
from conf import Config
from ans import Answers
from mth import Math

url_donate_path = 'https://money.yandex.ru/to/4100111962148422'
url_team_leader = 'https://t.me/dont_open'
bot_token = Config.get_token()

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, Answers.start_ans, reply_markup=Answers.main_markup, parse_mode='markdown')


@bot.message_handler(regexp=r"^\/tex .+")
def convert_latex(message):
    regex = r"^\/tex (.+)"
    parser = re.search(regex, message.text)
    tex_command = parser.group(1)

    # Заглушка. Убрать, когда сделаем генерацию картинки
    bot.send_message(message.chat.id,
                     "Вы ввели команду *\"" + tex_command + "\"*. Вскоре я научусь переводить её в картинку!",
                     parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '📚Вышмат':
        bot.send_message(message.chat.id, Math.math_ans, reply_markup=mth.start_kb_for_high_school())

    if message.text == '💰Помощь проекту':
        bot.send_message(message.chat.id, url_donate_path)

    if message.text == '☝Рекомендации':
        bot.send_message(message.chat.id, "Ссылка на руководителя проекта: " + url_team_leader)

    if message.text == '❔Справка':
        bot.send_message(message.chat.id, "/tex <формула> - конвертирует <формула> в картинку с ней. "
                                          "Для выбора тем по высшей математике "
                                          "последовательно переходите по кнопкам")


def is_section(data):
    if "section" in data.split('.'):
        return True
    return False
    

@bot.callback_query_handler(func=lambda call: is_section(call.data))
def query_handler(call):
    kb = types.InlineKeyboardMarkup()
    data = call.data.split('.')
    topic = data[0]
    page = data[-1]

    if topic+"." in [Math.matan, Math.linal, Math.geom]:
        kb = mth.generate_paged_list(topic+".", int(page))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb,
                          text="Вы выбрали раздел: " + topic + "\nТеперь выберите тему.")


@bot.callback_query_handler(func=lambda call: call.data.endswith("back to sections"))
def query_handler(call):
    data = call.data[:-len('back to sections')]
    if data == Answers.back:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=mth.start_kb_for_high_school(),
                              text=Math.math_ans)


bot.polling(none_stop=False, interval=1, timeout=20)
