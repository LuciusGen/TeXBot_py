# -*- coding: utf-8 -*-
import os

from flask import Flask, request
import telebot
from telebot import types
import re
import matplotlib.pyplot as plt

import mth
from conf import Config
from ans import Answers
from mth import Math
from parse import parse_command
import _sqlite3

bot_token = Config.get_token()

bot = telebot.TeleBot(bot_token)

server = Flask(__name__)

hook_url = Config.get_url()


@bot.edited_message_handler(regexp=r"^\/tex .+")
def edited_convert_latex(message):
    convert_latex(message)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Answer for /start command"""
    bot.send_message(message.chat.id, Answers.start_ans, reply_markup=Answers.main_markup, parse_mode='markdown')


@bot.message_handler(commands=['help'])
def start_message(message):
    """Answer for /help command"""
    bot.send_message(message.chat.id, Answers.reference_ans)


@bot.message_handler(regexp=r"^\/tex .+")
def convert_latex(message):
    """Converting Latex commands into .png images"""
    regex = r"^\/tex (.+)"
    parser = re.search(regex, message.text)
    tex_command = parser.group(1)

    try:
        png_list = list()
        pdf_list = list()

        lat_str, size, error = parse_command(tex_command)

        if len(error) != 0:
            bot.send_message(message.chat.id, error)
            return

        fig = plt.gca(frame_on=False)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)

        for id, lat in enumerate(lat_str):
            if id % 10 == 0 and id != 0:
                png_name = 'converted%i.png' % (id % 10)
                pdf_name = 'converted%i.pdf' % (id % 10)
                plt.savefig(png_name)
                png_list.append(png_name)
                plt.savefig(pdf_name)
                pdf_list.append(pdf_name)
                plt.close()

                fig = plt.gca(frame_on=False)
                fig.axes.get_xaxis().set_visible(False)
                fig.axes.get_yaxis().set_visible(False)

            hor_pos = 0.5
            vert_pos = 1/(2*min(len(lat_str), 10))*(2*(min(len(lat_str), 10)-id % 10)-1)

            if len(lat) != 0:
                plt.text(hor_pos, vert_pos, lat, fontsize=size, horizontalalignment='center', verticalalignment='center')

        plt.savefig('converted.png')
        png_list.append('converted.png')
        plt.savefig('converted.pdf')
        pdf_list.append('converted.pdf')
        plt.close()

        for png in png_list:
            bot.send_photo(message.chat.id, open(png, 'rb'))

        for pdf in pdf_list:
            bot.send_document(message.chat.id, open(pdf, 'rb'))
    except:
        bot.send_message(message.chat.id, "Допущен некорректный символ при написании формулы")
        plt.close()


@bot.message_handler(content_types=['text'])
def send_text(message):
    """Buttons settings"""
    if message.text == '📚Вышмат':
        bot.send_message(message.chat.id, Math.math_ans, reply_markup=mth.start_kb_for_high_school())

    if message.text == '💰Помощь проекту':
        bot.send_message(message.chat.id, Answers.url_donate_path)
        bot.send_message(message.chat.id, Answers.url_bit_coin)
        bot.send_message(message.chat.id, "Для доната в btc используйте счет Bitcoin кошелька: "
                         + Answers.bit_coin_bill)

    if message.text == '☝Рекомендации':
        bot.send_message(message.chat.id, "Ссылка на руководителя проекта: " + Answers.url_team_leader)

    if message.text == '❔Справка':
        bot.send_message(message.chat.id, Answers.reference_ans)


#  check that the inline button for the theme worked
def is_section(data):
    return "section" in data.split('.')


@bot.callback_query_handler(func=lambda call: is_section(call.data))
def query_handler(call):
    """Inline buttons for themes"""
    kb = types.InlineKeyboardMarkup()
    data = call.data.split('.')
    topic = data[0]
    page = data[-1]

    if topic + "." in [Math.matan, Math.linal, Math.geom]:
        kb = Answers.gen_paged_list(topic + ".", "section", int(page), page_size=9)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb,
                          text="Вы выбрали раздел: " + topic + "\nТеперь выберите тему.")


#  check that the inline button for the theorem worked
def is_theorem(data):
    return "theorem" in data.split('.')


def is_in_base(data):
    return "T" in data.split('.')


@bot.callback_query_handler(func=lambda call: is_theorem(call.data))
def query_handler(call):
    """Inline buttons for theorems"""
    data = call.data.split('.')
    theme = data[0]
    page = data[-1]

    kb = Answers.gen_paged_list(theme + ".", "theorem", int(page), page_size=9)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb,
                          text="Вы выбрали тему: " + theme + "\nТеперь выберите теорему.")


@bot.callback_query_handler(func=lambda call: is_in_base(call.data))
def query_handler(call):
    """Inline buttons to send data theorems"""
    _, theme, numb = call.data.split('.')
    theme += '.'

    conn = _sqlite3.connect('database.db')  # create data base
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM " + "[" + theme + "]" + "WHERE [callback_data]=" + numb)
    inf = cursor.fetchall()
    conn.close()

    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    rel_path = "images/" + theme.replace('.', '') + '/' + inf[0][2]
    abs_file_path = os.path.join(script_dir, rel_path)

    bot.send_photo(call.message.chat.id, open(abs_file_path, 'rb'))
    bot.send_message(call.message.chat.id, text="TeX code of this theorem:" + inf[0][3])


@bot.callback_query_handler(func=lambda call: call.data.endswith("back to sections"))
def query_handler(call):
    """Back inline button, to sections"""
    data = call.data[:-len('back to sections')]
    if data == Answers.back:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=mth.start_kb_for_high_school(),
                              text=Math.math_ans)


@bot.callback_query_handler(func=lambda call: call.data.endswith("back to themes"))
def query_handler(call):
    """back inline button, to themes"""
    data = call.data.split('.')
    theme = data[0] + '.'
    need_section = Math.give_need_section(theme)
    markup = Answers.gen_paged_list(need_section, "section", 0, page_size=9)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=markup,
                          text="Вы выбрали раздел: " + need_section + "\nТеперь выберите тему.")


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(inline_query):
    tex_command = inline_query.query
    try:

        lat_str, size, error = parse_command(tex_command)

        if len(error) != 0:
            plt.close()
            plt.clf()
            r = types.InlineQueryResultArticle('1', 'Ошибка в конвертации',
                                               types.InputTextMessageContent("Ошибка в конвертации."))
            bot.answer_inline_query(inline_query.id, [r])
            return

        fig = plt.gca(frame_on=False)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)

        if len(lat_str) > 10:
            plt.close()
            plt.clf()
            r = types.InlineQueryResultArticle('1', 'Ошибка, выражение слишком длинное.',
                                               types.InputTextMessageContent("Ошибка, выражение слишком длинное."))
            bot.answer_inline_query(inline_query.id, [r])
            return

        for id, lat in enumerate(lat_str):
            hor_pos = 0.5
            vert_pos = 1 / (2 * min(len(lat_str), 10)) * (2 * (min(len(lat_str), 10) - id % 10) - 1)

            if len(lat) != 0:
                plt.text(hor_pos, vert_pos, lat, fontsize=size, horizontalalignment='center',
                         verticalalignment='center')

        filename = 'converted' + str(inline_query.id) + '.png'
        plt.savefig(filename)
        plt.clf()
        plt.close()
        photo_id = bot.send_photo('267362684', open(filename, 'rb')).photo[0].file_id
        r = types.InlineQueryResultCachedPhoto(id=0, photo_file_id=photo_id)

        bot.answer_inline_query(inline_query.id, [r], cache_time=1)
    except Exception as e:
        print(e)
        plt.clf()
        plt.close()


@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(
        url=hook_url+"bot")  # этот url нужно заменить на url вашего Хероку приложения
    return "?", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
