import telebot

from conf import Config
from ans import Answers
from mth import Math

url_donate_path = 'https://money.yandex.ru/to/4100111962148422'
bot_token = Config.get_token()

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Reply with welcome message and main keyboard"""
    bot.send_message(message.chat.id, Answers.start_ans, reply_markup=Answers.main_markup, parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '📚Вышмат':
        bot.send_message(message.chat.id, Math.math_ans, reply_markup=Math.math_markup)
    elif message.text == '💰Помощь проекту':
        bot.send_message(message.chat.id, url_donate_path)


bot.polling(none_stop=False, interval=1, timeout=20)
