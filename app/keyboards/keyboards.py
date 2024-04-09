from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup
)

ONE_MONTH_BUTTON_TEXT = 'Один месяц'
ONE_MONTH_BUTTON_CALLBACK = '1'
TWO_MONTH_BUTTON_TEXT = 'Два месяца'
TWO_MONTH_BUTTON_CALLBACK = '2'

TARIFFS_LIST_BUTTON_TEXT = 'Тарифы 💼'
MY_SUBSCRIBTION_BUTTON_TEXT = 'Моя подписка 👀'

BANKS_CARD_BUTTON_TEXT = 'Банковская карта'
BACK_BUTTON_TEXT = 'Назад'
BACK_BUTTON_CALLBACK = 'back'

one_month_button = InlineKeyboardButton(
    text=ONE_MONTH_BUTTON_TEXT,
    callback_data=ONE_MONTH_BUTTON_CALLBACK
)
two_month_button = InlineKeyboardButton(
    text=TWO_MONTH_BUTTON_TEXT,
    callback_data=TWO_MONTH_BUTTON_CALLBACK
)
tariffs_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[one_month_button], [two_month_button]]
)

tariffs_list_button = KeyboardButton(text=TARIFFS_LIST_BUTTON_TEXT)
my_subscribtion_button = KeyboardButton(text=MY_SUBSCRIBTION_BUTTON_TEXT)
choose_action_keyboard = ReplyKeyboardMarkup(
    keyboard=[[tariffs_list_button, my_subscribtion_button]],
    resize_keyboard=True,
)

banks_card_button = InlineKeyboardButton(text=BANKS_CARD_BUTTON_TEXT, pay=True)
back_button = InlineKeyboardButton(
    text=BACK_BUTTON_TEXT,
    callback_data=BACK_BUTTON_CALLBACK
)
invoice_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[banks_card_button], [back_button]]
)
