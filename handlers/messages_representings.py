def represent_card(card_name, card_strength, card_health):
    return f'{card_name}\nСила: {card_strength}\nЗдоровье: {card_health}'


def represent_winner(battle_message, name_first, name_second):
    match battle_message:
        case 'both non-positive health':
            return f"{name_first} и {name_second} не смогли выстоять и секунды друг против друга"
        case '1 non-positive health':
            return f"{name_first} не смог выстоять и секунды против {name_second}"
        case '2 non-positive health':
            return f"{name_second} не смог выстоять и секунды против {name_first}"
        case 'both non-positive strength':
            return f"Битва между {name_first} и {name_second} будет длиться целую вечность!"
        case '1 non-positive strength':
            return f"{name_second} уничтожил {name_first} без единой царапины"
        case '2 non-positive strength':
            return f"{name_first} уничтожил {name_second} без единой царапины"
        case 'draw':
            return f"Боевая ничья между {name_first} и {name_second}!"
        case '1 win':
            return f"{name_first} победил! {name_second} не грусти. Повезет в следующий раз!"
        case '2 win':
            return f"{name_second} победил! {name_first} не грусти. Повезет в следующий раз!"


def get_start_message():
    message = "Привет! Я бот, с помощь которого можно устраивать карточные дуэли и многое дрругое!\n\n" \
              "Я очень прост в использовании. Достаточно в любом чате или в личной переписке с другом написсать:\n\n" \
              "@NetZheBot (любой текст)\n\nи я предложу Вам доступные команды!\n\nУдачи!"
    return message


def get_help_message():
    message = "Я очень прост в использовании. Достаточно в любом чате или в личной переписке с другом написсать:\n\n" \
              "@NetZheBot (любой текст)\n\nи я предложу Вам доступные команды!\n\nУдачи!"
    return message
