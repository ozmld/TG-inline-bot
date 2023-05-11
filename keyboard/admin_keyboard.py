from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

upload_btn = KeyboardButton("Загрузить")
cancel_btn = KeyboardButton("Отмена")

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(upload_btn).add(cancel_btn)
