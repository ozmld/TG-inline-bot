import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect("NetZheCards.db")
    cur = base.cursor()
    if base:
        print("All Good!")
    base.execute('CREATE TABLE IF NOT EXISTS cards(img TEXT, name TEXT PRIMARY KEY, strength TEXT, health TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO cards VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

def sql_get_random():
    return cur.execute('SELECT * FROM cards ORDER BY RANDOM() LIMIT 2').fetchall()

def sql_read():
    return cur.execute('SELECT * FROM cards').fetchall()
