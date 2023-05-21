import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect("NetZheCards.db")
    cur = base.cursor()
    if base:
        print("All Good!")
    base.execute('CREATE TABLE IF NOT EXISTS cards(img TEXT, name TEXT PRIMARY KEY, strength TEXT, health TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS users(chat_id TEXT, user_id TEXT warns INTEGER DEFAULT 0)')
    base.commit()


async def sql_add_card_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO cards VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_add_user(chat_id, user_id):
    user = cur.execute("SELECT 1 FROM users WHERE chat_id == '{}' AND user_id == '{}'".format(chat_id,
                                                                                              user_id)).fetchall()
    if not user:
        cur.execute('INSERT INTO users VALUES (?, ?)', (chat_id, user_id))
        base.commit()

def sql_get_warns_command(chat_id, user_id):
    user = cur.execute("SELECT * FROM users WHERE chat_id == '{}' AND user_id == '{}' LIMIT 1".format(chat_id,
                                                                                                      user_id)).fetchall()
    if user:
        return user[0][2]
    return None


def sql_warn_command(chat_id, user_id):
    warns = sql_get_warns_command(chat_id, user_id)
    if warns is not None:
        cur.execute("UPDATE users SET warns = {} WHERE chat_id == '{}' AND user_id == '{}'".format(warns + 1,
                                                                                                   chat_id,
                                                                                                   user_id))
        base.commit()


def sql_unwarn_command(chat_id, user_id):
    warns = sql_get_warns_command(chat_id, user_id)
    if warns is not None:
        cur.execute("UPDATE users SET warns = {} WHERE chat_id == '{}' AND user_id == '{}'".format(warns - 1,
                                                                                                   chat_id,
                                                                                                   user_id))
        base.commit()

def sql_set_warn_command(chat_id, user_id, warn_num):
    user = cur.execute("SELECT * FROM users WHERE chat_id == '{}' AND user_id == '{}' LIMIT 1".format(chat_id,
                                                                                                      user_id)).fetchall()

    if user:
        cur.execute("UPDATE users SET warns = {} WHERE chat_id == '{}' AND user_id == '{}'".format(warn_num,
                                                                                                   chat_id,
                                                                                                   user_id))
        base.commit()

def sql_get_random_users(chat_id, num=1):
    return cur.execute("SELECT * FROM users WHERE chat_id == '{}' ORDER BY RANDOM() LIMIT '{}'".format(chat_id, num)).fetchall()

def sql_get_users_from_chat(chat_id):
    return cur.execute("SELECT * FROM users WHERE chat_id == '{}'".format(chat_id)).fetchall()

def sql_get_all_users():
    return cur.execute("SELECT * FROM users ORDER BY chat_id").fetchall()
# async def sql_update_user(chat_id, user_id, state):
#     async with state.proxy() as data:
#         cur.execute("UPDATE users WHERE chat_id == '{}' AND user_id == '{}' SET first_name = '{}', username = '{}'".format(user_id,
#                                                                                                                            chat_id,
#                                                                                                                            data['first_name'],
#                                                                                                                            data['username']))
#         base.commit()


def sql_get_random():
    return cur.execute('SELECT * FROM cards ORDER BY RANDOM() LIMIT 2').fetchall()


def sql_read():
    return cur.execute('SELECT * FROM cards').fetchall()