from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import bot
from database import sqlite_db
from keyboard import admin_keyboard, get_warns_keyboard
from sqlite3 import DatabaseError
from handlers import represent_card
import datetime
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
    async with state.proxy as data:
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
        await sqlite_db.sql_add_card_command(state)
        await answer_admin(message, 'Ваша карточка добавлена')
    except DatabaseError:
        await answer_admin(message, 'Не удалось добавить карточку! Ошибка базы данных')
    await state.finish()


async def show_cards(message: types.Message):
    for photo, name, strength, health in sqlite_db.sql_read():
        await bot.send_photo(message.chat.id, photo, represent_card(name, strength, health))


async def warn_command(message: types.Message):
    chat_id = message.reply_to_message.chat.id
    user_id = message.reply_to_message.from_user.id
    sqlite_db.sql_warn_command(chat_id, user_id)
    # new_text = f"<b>ОСТОРОЖНО!!! ТУТ ЧТО-ТО ПЛОХОЕ</b>\n<tg-spoiler>{message.reply_to_message.text}</tg-spoiler>"
    # await message.reply_to_message.edit_text(new_text, parse_mode='html')
    username = (await bot.get_chat_member(chat_id, user_id)).user.username
    warns_num = sqlite_db.sql_get_warns_command(chat_id, user_id)
    admin_chat_id = message.chat.id
    admin_user_id = message.from_user.id
    admin_username = (await bot.get_chat_member(admin_chat_id, admin_user_id)).user.username
    reason = message.text[6:]
    if (warns_num == 3):
        dt = datetime.datetime.now() + datetime.timedelta(minutes=15)
        timestamp = dt.timestamp()
        await message.reply(
            f'<b>Решение было принято:</b>@{admin_username}'
            f'\n<b>Нарушитель:</b> @{username}'
            f'\n<b>Срок наказания:</b> 15 минут'
            f'\n<b>Причина:</b> Неоднократные предупреждения',
            parse_mode='html')
        await bot.restrict_chat_member(chat_id, user_id,
                                       types.ChatPermissions(False), until_date=timestamp)
        sqlite_db.sql_set_warn_command(chat_id, user_id, 0)
    else:
        await message.reply(f"@{admin_username} выдал предупреждение @{username}!"
                            f"\nПояснение - {reason}"
                            f"\n\nТекущее количество нарушений @{username} - {warns_num}!"
                            f"\n\nБудь осторожнее! После третьего предупреждения будет выдан мут на 10 часов")


async def unban_command(message: types.Message):
    chat_id = message.reply_to_message.chat.id
    user_id = message.reply_to_message.from_user.id
    username = message.reply_to_message.from_user.username

    sqlite_db.sql_set_warn_command(chat_id, user_id, 0)
    admin_username = message.from_user.username
    await message.reply(f"@{admin_username} смиловался над @{username} и разбанил его!")
    await bot.restrict_chat_member(chat_id, user_id,
                                   types.ChatPermissions(True))


async def warns_command(message: types.Message):
    chat_id = message.reply_to_message.chat.id
    user_id = message.reply_to_message.from_user.id
    username = message.reply_to_message.from_user.username
    admin_username = message.from_user.username
    await message.reply(f"Количество нарушений @{username} - {sqlite_db.sql_get_warns_command(chat_id, user_id)}",
                        reply_markup=get_warns_keyboard(user_id))


async def change_warns(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id
    username = callback.message.from_user.username
    print((await bot.get_chat_member(chat_id, user_id)))
    if (await bot.get_chat_member(chat_id, user_id)).status != "creator" and (await bot.get_chat_member(chat_id, user_id)).status != "administrator":
        await callback.answer("Вы не можете менять нарушения")
        return
    text = callback.message.text
    text = text.split("-")
    user_id = callback.data.split("_")[2]
    if callback.data.split("_")[1] == "add":
        sqlite_db.sql_warn_command(chat_id, user_id)
    if callback.data.split("_")[1] == "dec":
        sqlite_db.sql_unwarn_command(chat_id, user_id)
    await callback.message.edit_text(f"{text[0]}- {sqlite_db.sql_get_warns_command(chat_id, user_id)}",
                                     reply_markup=get_warns_keyboard(user_id))
    await callback.answer("Успешно!")



async def all_command(message: types.Message):
    users = sqlite_db.sql_get_users_from_chat(message.chat.id)
    text = ""
    async def get_name(chat_id, user_id):
        return (await bot.get_chat_member(chat_id, user_id)).user.username

    for user in users:
        text += '@' + await get_name(user[0], user[1]) + " "
    await bot.send_message(message.chat.id, text)
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(all_command, commands=['all'], is_chat_admin=True)

    dp.register_message_handler(warns_command, commands=['warns'])
    dp.register_message_handler(warn_command, commands=['warn'], is_chat_admin=True)
    dp.register_message_handler(unban_command, commands=['unban'], is_chat_admin=True)

    dp.register_callback_query_handler(change_warns, Text(startswith="warn"))

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