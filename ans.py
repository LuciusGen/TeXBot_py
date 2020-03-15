from telebot import types


class Answers:

    main_markup = types.ReplyKeyboardMarkup()
    main_markup.row('📚Вышмат', '☝Рекомендации')
    main_markup.row('❔Справка', '💰Помощь проекту')

    back = "Назад"

    start_ans = "Приветствую. Бот позволяет генерировать картинки из кода LaTex, " \
                "также здесь содержатся основные темы вышмата"

    url_donate_path = 'https://money.yandex.ru/to/4100111962148422'
    url_team_leader = 'https://t.me/dont_open'
    url_bit_coin = 'https://topcash.me/ru/yamrub_to_btc'
    bit_coin_bill = 'bc1qwz2rcelzqdwh8y4kqupk3q5qrtsayltvnf955c'