import hashlib

from aiogram import types, Dispatcher
from keyboard import get_keyboard_duel
from create_bot import bot
from database import sqlite_db

from handlers import represent_card, represent_winner, get_start_message, get_help_message
from handlers import get_battle_result


async def start_duel(callback: types.CallbackQuery):
    # get players names
    name_first = callback.data.split(";")[1][1:]
    name_second = callback.from_user.first_name

    text = f'{name_second} принимает вызов {name_first}!'

    # get random cards for players
    card1, card2 = sqlite_db.sql_get_random()[0], sqlite_db.sql_get_random()[1]

    # representing players' cards
    text += "\n\n"
    text += f'Карта {name_first}:\n' + represent_card(card1[1], card1[2], card1[3])
    text += "\n\n"
    text += f'Карта {name_second}:\n' + represent_card(card2[1], card2[2], card2[3])

    # get result of the battle
    battle_result = get_battle_result(card1, card2)

    # representing battle result
    text += "\n\n"
    text += represent_winner(battle_result, name_first, name_second)

    # "sending" result
    await bot.edit_message_text(inline_message_id=callback.inline_message_id, text=text)
    await callback.answer()


async def inline_mode(query: types.InlineQuery):
    text = f"{query.from_user.first_name} вызывает на дуэль карточек!"

    # creating unique id
    result_id = hashlib.md5(text.encode()).hexdigest()
    input_content = types.InputTextMessageContent(text)

    # creating inline item
    item = types.InlineQueryResultArticle(id=result_id,
                                          input_message_content=input_content,
                                          title="ДУЭЛЬ",
                                          description="Нажмите, чтобы начать дуэль карточек",
                                          reply_markup=get_keyboard_duel(query.from_user.first_name),
                                          )
    actions = [item]

    # answering to inline query
    await bot.answer_inline_query(results=actions, cache_time=1, inline_query_id=query.id, is_personal=True)


async def start_command(message: types.Message):
    start_message = get_start_message()
    await bot.send_message(message.chat.id, start_message)


async def help_command(message: types.Message):
    help_message = get_help_message()
    await bot.send_message(message.chat.id, help_message)


def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])

    dp.register_callback_query_handler(start_duel)
    dp.register_inline_handler(inline_mode)
