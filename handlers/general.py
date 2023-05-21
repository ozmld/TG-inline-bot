import asyncio

from aiogram import types, Dispatcher
from keyboard import get_keyboard_duel
from create_bot import bot
from database import sqlite_db
from aiogram.utils.exceptions import BotBlocked
from handlers.messages_representings import *
from handlers.actions import *

import aioschedule
import datetime
from threading import Thread

async def start_duel(callback: types.CallbackQuery):
    # get players names
    name_first = callback.data.split(";")[1][1:]
    name_second = callback.from_user.first_name

    text = f'<b>{name_second} принимает вызов {name_first}!</b>'

    # get random cards for players
    card1, card2 = sqlite_db.sql_get_random()[0], sqlite_db.sql_get_random()[1]

    # representing players' cards
    text += "\n\n"
    text += f'<b>Карта {name_first}:</b>\n' + represent_card(card1[1], card1[2], card1[3])
    text += "\n\n"
    text += f'<b>Карта {name_second}:</b>\n' + represent_card(card2[1], card2[2], card2[3])

    # get result of the battle
    battle_result = get_battle_result(card1, card2)

    # representing battle result
    text += "\n\n"
    text += "<b>" + represent_winner(battle_result, name_first, name_second) + "</b>"

    # "sending" result
    await bot.edit_message_text(inline_message_id=callback.inline_message_id, text=text, parse_mode='html')
    await callback.answer()


async def inline_mode(query: types.InlineQuery):
    actions = []

    name = query.from_user.first_name
    text = f"<b>{name} вызывает на дуэль карточек!</b>"

    # creating unique id
    result_id = get_unique_id(text)
    input_content = types.InputTextMessageContent(text, parse_mode='html')
    title = "ДУЭЛЬ"
    description = "Нажмите, чтобы начать дуэль карточек"
    # creating inline item
    item = types.InlineQueryResultArticle(id=result_id,
                                          input_message_content=input_content,
                                          title=title,
                                          description=description,
                                          reply_markup=get_keyboard_duel(name),
                                          thumb_url="https://i.postimg.cc/sf6PQVPg/ShowDown.jpg"
                                          )
    actions.append(item)
    name = query.query or query.from_user.first_name
    text = f"<i>Размер аппарата <b>{name}</b> {get_random_size()} см</i>"

    # creating unique id, text, title and description
    result_id = get_unique_id(text)
    input_content = types.InputTextMessageContent(text, parse_mode='html')
    title = "Breaking Balls"
    description = f"Нажмите, чтобы узнать размер аппарата {name}"
    # creating inline item
    item = types.InlineQueryResultArticle(id=result_id,
                                          input_message_content=input_content,
                                          title=title,
                                          description=description,
                                          thumb_url="https://i.postimg.cc/T2zwHFfc/Breaking-Balls.jpg",
                                          )
    actions.append(item)

    text = f"{query.query or ''}\n\n<b>Магический шар отвечает: <tg-spoiler>{get_random_answer()}</tg-spoiler></b>"

    # creating unique id
    result_id = get_unique_id(text)
    input_content = types.InputTextMessageContent(text, parse_mode="html")
    title = "Магический шар"
    description = f"Использовать магишеский шар, чтобы ответить на вопрос: {query.query or ''}"
    # creating inline item
    item = types.InlineQueryResultArticle(id=result_id,
                                          input_message_content=input_content,
                                          title=title,
                                          description=description,
                                          thumb_url="https://i.postimg.cc/8Pd1XCy1/Magic-Ball.jpg"
                                          )
    actions.append(item)
    # answering to inline query
    await bot.answer_inline_query(results=actions, cache_time=1, inline_query_id=query.id, is_personal=True)


async def start_command(message: types.Message):
    await sqlite_db.sql_add_user(message.chat.id, message.from_user.id)
    start_message = get_start_message()
    await bot.send_message(message.chat.id, start_message, parse_mode="Markdown")


async def help_command(message: types.Message):
    help_message = get_help_message()
    await bot.send_message(message.chat.id, help_message, parse_mode="Markdown")
async def my_warns_command(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await message.edit_text(f"Количество моих предупеждений: {sqlite_db.sql_get_warns_command(chat_id, user_id)}")

async def pidor_command(message: types.Message):
    msg = await bot.send_message(message.chat.id, "Вычисляю главного пидора чата, подождите...")
    await asyncio.sleep(5)
    member = await bot.get_chat_member(message.chat.id, sqlite_db.sql_get_random_users(message.chat.id)[0][1])
    await msg.edit_text(f"Главный пидор чата {member.user.first_name} ({member.user.username}). Пиздец...")

# async def echo(message: types.Message):
#     await sqlite_db.sql_add_user(message.chat.id, message.from_user.id)
#     await sqlite_db.sql_add_user(-1001631377117, 516379369)
#     await sqlite_db.sql_add_user(-1001631377117, 982036709)
#     print(sqlite_db.sql_get_random_user()[0][1])
async def say_something_nice_to_all(phrase_generator):
    users = sqlite_db.sql_get_all_users()
    if len(users) == 0:
        return
    chat_id = users[0][0]
    text = ""
    async def get_name(chat_id, user_id):
        return (await bot.get_chat_member(chat_id, user_id)).user.username

    for user in users:
        if user[0] != chat_id:
            try:
                await bot.send_message(chat_id, text + "\n\n" + phrase_generator())
            except BotBlocked:
                print(await get_name(user[0], user[1]), "blocked a bot")
            except:
                pass
            chat_id = user[0]
            text = '@' + await get_name(user[0], user[1]) + " "
        else:
            text += '@' + await get_name(user[0], user[1]) + " "
async def scheduler():
    aioschedule.every().day.at("00:00").do(say_something_nice_to_all, phrase_generator=get_good_night_wish)
    aioschedule.every().day.at("08:00").do(say_something_nice_to_all, phrase_generator=get_good_morning_wish)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def register_handlers_general(dp: Dispatcher):
    # dp.register_message_handler(echo)
    print(datetime.datetime.now().hour)
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(pidor_command, commands=['pidor'])
    dp.register_message_handler(my_warns_command, commands=['mywarns'])

    dp.register_callback_query_handler(start_duel)
    dp.register_inline_handler(inline_mode)
