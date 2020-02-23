import telebot
import keyboards
from conf import Config
from ans import Answers


bot_token = Config.get_token()

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def inline(message):
    bot.send_message(message.chat.id, Answers.start_ans, reply_markup=keyboards.Keyboard.inline_kb_full, parse_mode='markdown')


bot.polling(none_stop=False, interval=1, timeout=20)
