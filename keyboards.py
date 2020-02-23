from telebot import types

class Keyboard:

    button_school = 'btn_graduate_school'
    button_recommend = 'btn_recommendations'
    button_reference = 'btn_reference'
    button_donate = 'btn_donate'
    url_donate_path = 'https://money.yandex.ru/to/4100111962148422'

    inline_btn_graduate_school = types.InlineKeyboardButton('📚Вышмат', callback_data=button_school)
    inline_btn_recommendations = types.InlineKeyboardButton('☝Рекомендации', callback_data=button_recommend)
    inline_btn_reference = types.InlineKeyboardButton('❔Справка', callback_data=button_reference)
    inline_btn_donation = types.InlineKeyboardButton('💰Помощь проекту', callback_data=button_donate)

    inline_kb_full = types.InlineKeyboardMarkup(row_width=2).add(
        inline_btn_graduate_school, inline_btn_recommendations, inline_btn_reference, inline_btn_donation
    )
