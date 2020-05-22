from math import ceil

from telebot import types

from mth import Math
import theorems
import themes


class Answers:
    """Class for bot answers"""

    main_markup = types.ReplyKeyboardMarkup()
    main_markup.row('📚Вышмат', '☝Рекомендации')
    main_markup.row('❔Справка', '💰Помощь проекту')

    back = "Назад"

    start_ans = "Приветствую. Бот позволяет генерировать картинки из кода LaTex, " \
                "также здесь содержатся основные темы вышмата"

    reference_ans = "🔘 /tex <формула> - конвертирует <формула> в картинку с ней.\n" \
                    "🔘 Для выбора тем по высшей математике" \
                    " последовательно переходите по кнопкам.\n" \
                    "🔘 *inlineMode* - введите в любом чате `@latex_edit_bot` а затем через пробел формулу" \
                    " для оперативного получения сконвертированной картинки с вашей формулой.\n" \
                    "🔘 Список поддерживаемых формул" \
                    " можно посмотреть [здесь](https://en.wikibooks.org/wiki/LaTeX/Mathematics#Inserting_%22Displayed)" \
                    ".\n🔘 Конструкция " + r"`\begin{}..\end{}` не работает."

    url_donate_path = 'https://money.yandex.ru/to/4100111962148422'
    url_team_leader = 'https://t.me/dont_open'
    url_bit_coin = 'https://topcash.me/ru/yamrub_to_btc'
    bit_coin_bill = 'bc1qwz2rcelzqdwh8y4kqupk3q5qrtsayltvnf955c'

    @staticmethod
    def gen_paged_list(section, sections_type, page, page_size):

        if sections_type == 'theorem':
            theorems.theorems_from_database(section)
            topic_len = len(theorems.matan_theorems_buttons)
            back = section + '.' + "back to themes"
        elif sections_type == 'section':
            topic_len = Math.get_topic_size(section)
            back = Answers.back + "back to sections"
        else:
            return

        # numb of pages
        pages_numb = ceil(topic_len / page_size)

        back_button = types.InlineKeyboardButton(
            "🔥 " + Answers.back + "(" + str(page + 1) + "/" + str(pages_numb) + ")",
            callback_data=back)

        if pages_numb > 1:
            if page == 0:
                where_left = pages_numb - 1
                where_right = page + 1
            elif page == pages_numb - 1:
                where_left = page - 1
                where_right = 0
            else:
                where_left = page - 1
                where_right = page + 1

            left_button = types.InlineKeyboardButton("⬅(" + str(where_left + 1) + "/" + str(pages_numb) + ")",
                                                     callback_data=section + sections_type + "." + str(where_left))

            right_button = types.InlineKeyboardButton("➡(" + str(where_right + 1) + "/" + str(pages_numb) + ")",
                                                      callback_data=section + sections_type + "." + str(where_right))

            if (page + 1) * page_size <= topic_len:
                if sections_type == 'theorem':
                    markup = theorems.generate_theorems(page * page_size, (page + 1) * page_size)
                elif sections_type == 'section':
                    markup = themes.generate_topic_markup(section, page * page_size, (page + 1) * page_size)
            else:
                if sections_type == 'theorem':
                    markup = theorems.generate_theorems(page * page_size, topic_len)
                elif sections_type == 'section':
                    markup = themes.generate_topic_markup(section, page * page_size, topic_len)

            markup.row(left_button, back_button, right_button)
        else:
            if sections_type == 'theorem':
                markup = theorems.generate_theorems(page, topic_len, section)
            elif sections_type == 'section':
                markup = themes.generate_topic_markup(section, page, topic_len)
            markup.add(back_button)
        return markup
