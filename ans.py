from telebot import types


class Answers:

    main_markup = types.ReplyKeyboardMarkup()
    main_markup.row('📚Вышмат', '☝Рекомендации')
    main_markup.row('❔Справка', '💰Помощь проекту')

    back = "Назад"

    start_ans = "Приветствую. Бот позволяет генерировать картинки из кода LaTex, " \
                "также здесь содержатся основные темы вышмата"
