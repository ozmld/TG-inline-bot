from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import bot
from database import sqlite_db
from keyboard import admin_keyboard
from sqlite3 import DatabaseError
from handlers import represent_card

ID = []


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    strength = State()
    health = State()


async def answer_admin(message: types.Message, reply_message: str):
    if message.chat.type == "private":
        await message.reply(reply_message)
    else:
        await message.delete()
        await bot.send_message(message.from_user.id, reply_message)


async def moderation(message: types.Message):
    global ID
    ID.append(message.from_user.id)
    await bot.send_message(message.from_user.id, "Да, папочка?", reply_markup=admin_keyboard.kb_admin)
    await message.delete()


async def cm_start(message: types.Message):
    if message.from_user.id not in ID:
        return
    await answer_admin(message, 'Загрузи изображение')
    await FSMAdmin.photo.set()


async def cancel_handler(message: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    global ID
    ID.remove(message.from_user.id)
    await answer_admin(message, 'OK')


async def image_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await answer_admin(message, 'Теперь имя')


async def name_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await answer_admin(message, 'Сила')


async def strength_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['strength'] = message.text
    await FSMAdmin.next()
    await answer_admin(message, 'Здоровье')


async def health_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['health'] = message.text
    global ID
    ID.remove(message.from_user.id)
    try:
        await sqlite_db.sql_add_command(state)
        await answer_admin(message, 'Ваша карточка добавлена')
    except DatabaseError:
        await answer_admin(message, 'Не удалось добавить карточку! Ошибка базы данных')
    await state.finish()


async def show_cards(message: types.Message):
    for photo, name, strength, health in sqlite_db.sql_read():
        await bot.send_photo(message.chat.id, photo, represent_card(name, strength, health))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(show_cards, commands=['cards'], is_chat_admin=True)

    dp.register_message_handler(moderation, commands=['moder', 'admin'], is_chat_admin=True)

    dp.register_message_handler(cm_start, commands=['загрузить'], state=None)
    dp.register_message_handler(cm_start, Text(equals='загрузить', ignore_case=True), state=None)

    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

    dp.register_message_handler(image_load, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(name_load, content_types=['text'], state=FSMAdmin.name)
    dp.register_message_handler(strength_load, content_types=['text'], state=FSMAdmin.strength)
    dp.register_message_handler(health_load, content_types=['text'], state=FSMAdmin.health)