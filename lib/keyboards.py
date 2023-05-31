from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import utils.utils as ut

menu_names = ut.get_menu_names()

start_keyboard_options = [
        [menu_names.show_deeds],
        [menu_names.add_deed]
    ]


def process_deeds(deed: 'Deed') -> str:
    # notify_emoji = '🔔 ' if deed.notify_time and ut.localize(deed.notify_time) > ut.localize(datetime.now()) else ''
    notify_emoji = '🔔 ' if deed.notify_time and deed.notify_time > ut.localize(datetime.now()) else ''
    return notify_emoji + deed.name


def get_start_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(start_keyboard_options, one_time_keyboard=False, resize_keyboard=True)
    return markup


def get_inline_deeds(deeds: list['Deeds']) -> InlineKeyboardMarkup:
    keyboard = []
    for deed in deeds:
        text = process_deeds(deed)
        deed_button = InlineKeyboardButton(text, callback_data=f"deed_id={deed.id}", )
        keyboard.append([deed_button])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def bool_variants() -> ReplyKeyboardMarkup:
    text = [[menu_names.yes_, menu_names.no_]]
    markup = ReplyKeyboardMarkup(text, one_time_keyboard=True, resize_keyboard=True)
    return markup


def get_inline_deed(deed: 'Deed') -> InlineKeyboardMarkup:

    button_timer = InlineKeyboardButton('🔔', callback_data=f"timer_deed_id={deed.id}")
    button_rename = InlineKeyboardButton('🖊️', callback_data=f"rename_deed_id={deed.id}")
    button_done = InlineKeyboardButton('✅', callback_data=f"done_deed_id={deed.id}")

    reply_markup = InlineKeyboardMarkup([[button_timer, button_rename, button_done]])
    return reply_markup


def get_inline_deed_after_notify(deed: 'Deed') -> InlineKeyboardMarkup:

    button_timer = InlineKeyboardButton('🔔', callback_data=f"notify_timer_deed_id={deed.id}")
    button_done = InlineKeyboardButton('✅', callback_data=f"notify_done_deed_id={deed.id}")

    reply_markup = InlineKeyboardMarkup([[button_timer, button_done]])
    return reply_markup


def get_postpone_minutes() -> list[list[InlineKeyboardButton]]:
    keyboard = [
        [
            InlineKeyboardButton('5min', callback_data='postpone=5'),
            InlineKeyboardButton('10min', callback_data='postpone=10'),
            InlineKeyboardButton('30min', callback_data='postpone=30'),
            InlineKeyboardButton('1hour', callback_data='postpone=60'),
            InlineKeyboardButton('1day', callback_data='postpone=1440'),
        ]
    ]

    return keyboard


def get_days() -> InlineKeyboardMarkup:

    keyboard = get_postpone_minutes()
    # current_time = ut.localize(datetime.now())
    current_time = datetime.now()
    days = [current_time + timedelta(days=day_add) for day_add in range(9)]
    showed_days = [ut.repr_date(day) for day in days]
    for ix, day in enumerate(showed_days):
        button = InlineKeyboardButton(day, callback_data=f'day={ix}')
        if not ix % 3:
            curr_row = [button]
        elif ix % 3 == 1:
            curr_row.append(button)
        else:
            curr_row.append(button)
            keyboard.append(curr_row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def get_hours() -> InlineKeyboardMarkup:
    keyboard = []
    curr_row = []
    for hour in range(24):
        str_hour = '0' + str(hour) if hour < 10 else str(hour)
        button = InlineKeyboardButton(str_hour, callback_data=f"hour={hour}")
        curr_row.append(button)
        if hour % 4 == 3:
            keyboard.append(curr_row)
            curr_row = []

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def get_minutes() -> InlineKeyboardMarkup:
    keyboard = []
    curr_row = []
    for minute in range(0, 60, 5):
        str_minute = '0' + str(minute) if minute < 10 else str(minute)
        button = InlineKeyboardButton(str_minute, callback_data=f"minute={minute}")
        curr_row.append(button)
        if minute % 20 == 15:
            keyboard.append(curr_row)
            curr_row = []

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def dzyn_keyboard() -> InlineKeyboardMarkup:
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🥂", callback_data='dzyn')]])
    return reply_markup
