from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# inline keyboard builder
def get_keyboard_duel(user_name):
    keyboard_duel = InlineKeyboardMarkup()
    duel = InlineKeyboardButton(text="Присоединиться к дуэле", callback_data=f'start duel; {user_name};')

    keyboard_duel.add(duel)

    return keyboard_duel
