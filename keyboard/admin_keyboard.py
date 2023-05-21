from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

upload_btn = KeyboardButton("Загрузить")
cancel_btn = KeyboardButton("Отмена")

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(upload_btn).add(cancel_btn)

def get_warns_keyboard(user_id):
    kb_warns = InlineKeyboardMarkup(one_time_keyboard=True)
    warn_add_button = KeyboardButton("➕", callback_data=f"warn_add_{user_id}")
    warn_dec_button = KeyboardButton("➖", callback_data=f"warn_dec_{user_id}")
    kb_warns.add(warn_add_button, warn_dec_button)
    return kb_warns
