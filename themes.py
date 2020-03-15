import ans
from mth import Math
from math import ceil
from telebot import types


# This file need to show all themes in inline buttons
#  Download themes from mth.py file(Math class)

def generate_paged_list_themes(topic, page):
    # numb of sections per page
    page_size = 9

    # numb of all sections in topic
    topic_len = Math.get_topic_size(topic)

    # numb of pages
    pages_numb = ceil(topic_len / page_size)

    back_button = types.InlineKeyboardButton(
        "🔥 " + ans.Answers.back + "(" + str(page + 1) + "/" + str(pages_numb) + ")",
        callback_data=ans.Answers.back + "back to sections")

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
                                                 callback_data=topic + "section." + str(where_left))

        right_button = types.InlineKeyboardButton("➡(" + str(where_right + 1) + "/" + str(pages_numb) + ")",
                                                  callback_data=topic + "section." + str(where_right))
        if (page + 1) * page_size <= topic_len:
            markup = generate_topic_markup(topic, page * page_size, (page + 1) * page_size)
        else:
            markup = generate_topic_markup(topic, page * page_size, topic_len)
        markup.row(left_button, back_button, right_button)
    else:
        markup = generate_topic_markup(topic, page, topic_len)
        markup.add(back_button)
    return markup


def generate_topic_markup(topic, first_button, last_button):
    sect_list = list()
    markup = types.InlineKeyboardMarkup(row_width=1)

    if topic == Math.matan:
        sect_list = kb_for_matan(first_button, last_button)
    elif topic == Math.linal:
        sect_list = kb_for_linal(first_button, last_button)
    elif topic == Math.geom:
        sect_list = kb_for_geom(first_button, last_button)

    markup.add(*sect_list)
    return markup


def kb_for_matan(first_button, last_button):
    start_page = 0
    intr_button = types.InlineKeyboardButton(Math.intr,
                                             callback_data=Math.intr + "theorem." + str(start_page))
    lim_button = types.InlineKeyboardButton(Math.lim,
                                            callback_data=Math.lim + "theorem." + str(start_page))
    diff_button = types.InlineKeyboardButton(Math.diff,
                                             callback_data=Math.diff + "theorem." + str(start_page))
    unc_int_button = types.InlineKeyboardButton(Math.unc_int,
                                                callback_data=Math.unc_int + "theorem." + str(start_page))
    cer_int_button = types.InlineKeyboardButton(Math.cer_int,
                                                callback_data=Math.cer_int + "theorem." + str(start_page))
    seq_ser_button = types.InlineKeyboardButton(Math.seq_ser,
                                                callback_data=Math.seq_ser + "theorem." + str(start_page))
    fourier_ser_button = types.InlineKeyboardButton(Math.fourier_ser,
                                                    callback_data=Math.fourier_ser + "theorem." + str(start_page))
    diff_few_var_button = types.InlineKeyboardButton(Math.diff_few_var,
                                                     callback_data=Math.diff_few_var + "theorem." + str(start_page))
    doub_int_button = types.InlineKeyboardButton(Math.doub_int,
                                                 callback_data=Math.doub_int + "theorem." + str(start_page))
    trip_int_button = types.InlineKeyboardButton(Math.trip_int,
                                                 callback_data=Math.trip_int + "theorem." + str(start_page))
    mult_int_button = types.InlineKeyboardButton(Math.mult_int,
                                                 callback_data=Math.mult_int + "theorem." + str(start_page))
    curv_int_button = types.InlineKeyboardButton(Math.curv_int,
                                                 callback_data=Math.curv_int + "theorem." + str(start_page))
    surf_int_button = types.InlineKeyboardButton(Math.surf_int,
                                                 callback_data=Math.surf_int + "theorem." + str(start_page))
    field_th_button = types.InlineKeyboardButton(Math.field_th,
                                                 callback_data=Math.field_th + "theorem." + str(start_page))

    buttons_list = [intr_button, lim_button, diff_button, unc_int_button,
                    cer_int_button, seq_ser_button, fourier_ser_button,
                    diff_few_var_button, doub_int_button, trip_int_button,
                    mult_int_button, curv_int_button, surf_int_button, field_th_button]

    return buttons_list[first_button:last_button]


def kb_for_linal(first_button, last_button):
    start_page = 0
    matrix_button = types.InlineKeyboardButton(Math.matrix,
                                               callback_data=Math.matrix + "theorem." + str(start_page))
    determinant_button = types.InlineKeyboardButton(Math.determinant,
                                                    callback_data=Math.determinant + "theorem." + str(start_page))
    slough_button = types.InlineKeyboardButton(Math.slough,
                                               callback_data=Math.slough + "theorem." + str(start_page))
    quad_form_button = types.InlineKeyboardButton(Math.quad_form,
                                                  callback_data=Math.quad_form + "theorem." + str(start_page))
    lin_space_button = types.InlineKeyboardButton(Math.lin_space,
                                                  callback_data=Math.lin_space + "theorem." + str(start_page))
    eucl_space_button = types.InlineKeyboardButton(Math.eucl_space,
                                                   callback_data=Math.eucl_space + "theorem." + str(start_page))
    polynom_button = types.InlineKeyboardButton(Math.polynom,
                                                callback_data=Math.polynom + "theorem." + str(start_page))
    field_button = types.InlineKeyboardButton(Math.field,
                                              callback_data=Math.field + "theorem." + str(start_page))
    group_button = types.InlineKeyboardButton(Math.group,
                                              callback_data=Math.group + "theorem." + str(start_page))

    buttons_list = [matrix_button, determinant_button, slough_button,
                    quad_form_button, lin_space_button, eucl_space_button,
                    polynom_button, field_button, group_button]

    return buttons_list[first_button:last_button]


def kb_for_geom(first_button, last_button):
    start_page = 0
    coord_plan_button = types.InlineKeyboardButton(Math.coord_plan,
                                                   callback_data=Math.coord_plan + "theorem." + str(start_page))
    line_equat_button = types.InlineKeyboardButton(Math.line_equat,
                                                   callback_data=Math.line_equat + "theorem." + str(start_page))
    line_plan_button = types.InlineKeyboardButton(Math.line_plan,
                                                  callback_data=Math.line_plan + "theorem." + str(start_page))
    seqt_th_button = types.InlineKeyboardButton(Math.seqt_th,
                                                callback_data=Math.seqt_th + "theorem." + str(start_page))
    coord_trans_button = types.InlineKeyboardButton(Math.coord_trans,
                                                    callback_data=Math.coord_trans + "theorem." + str(start_page))
    det_sec_thir_button = types.InlineKeyboardButton(Math.det_sec_thir,
                                                     callback_data=Math.det_sec_thir + "theorem." + str(start_page))
    coord_spac_button = types.InlineKeyboardButton(Math.coord_spac,
                                                   callback_data=Math.coord_spac + "theorem." + str(start_page))
    vect_alg_button = types.InlineKeyboardButton(Math.vect_alg,
                                                 callback_data=Math.vect_alg + "theorem." + str(start_page))
    geom_equat_button = types.InlineKeyboardButton(Math.geom_equat,
                                                   callback_data=Math.geom_equat + "theorem." + str(start_page))
    line_spac_button = types.InlineKeyboardButton(Math.line_spac,
                                                  callback_data=Math.line_spac + "theorem." + str(start_page))
    plan_spac_button = types.InlineKeyboardButton(Math.plan_spac,
                                                  callback_data=Math.plan_spac + "theorem." + str(start_page))
    surf_sec_button = types.InlineKeyboardButton(Math.surf_sec,
                                                 callback_data=Math.surf_sec + "theorem." + str(start_page))

    buttons_list = [coord_plan_button, line_equat_button, line_plan_button,
                    seqt_th_button, coord_trans_button, det_sec_thir_button,
                    coord_spac_button, vect_alg_button, geom_equat_button,
                    line_spac_button, plan_spac_button, surf_sec_button]

    return buttons_list[first_button:last_button]
