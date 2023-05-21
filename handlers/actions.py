import hashlib
from random import choice, shuffle

def get_battle_result(card1, card2):
    strength_1 = int(card1[2])
    health_1 = int(card1[3])
    strength_2 = int(card2[2])
    health_2 = int(card2[3])

    if health_1 <= 0 and health_2 <= 0:
        return 'both non-positive health'
    if health_1 <= 0:
        return '1 non-positive health'
    if health_2 <= 0:
        return '2 non-positive health'

    if strength_1 <= 0 and strength_2 <= 0:
        return 'both non-positive strength'
    if strength_1 <= 0:
        return '1 non-positive strength'
    if strength_2 <= 0:
        return '2 non-positive strength'

    # Evaluate number of shots needed to kill opponent
    shots_1 = (health_2 + strength_1 - 1) // strength_1
    shots_2 = (health_1 + strength_2 - 1) // strength_2

    if shots_1 == shots_2:
        return 'draw'
    if shots_1 < shots_2:
        return '1 win'
    return '2 win'


def get_unique_id(text):
    return hashlib.md5(text.encode()).hexdigest()


def get_random_size():
    sizes = []
    for size in range(41):
        num = 0
        match (size + 4) // 5:
            case 0: # 0 = 1%
                num = 5
            case 1: # 1 - 5 = 10%
                num = 10
            case 2: # 6 - 10 = 25%
                num = 25
            case 3: # 11 - 15 = 30%
                num = 30
            case 4: # 16 - 20 = 15%
                num = 15
            case 5: # 21 - 25 = 10%
                num = 10
            case 6: # 26 - 30 = 5%
                num = 5
            case 7: # 31 - 35 = 3%
                num = 3
            case 8: # 36 - 40 = 1%
                num = 1

        sizes.extend([size] * num)
    return choice(sizes)



def get_pidor(members):
    return choice(members)


def get_good_night_wish():
    with open("wishes/good_night_wishes.txt", 'r') as f:
        return choice(f.readlines()).rstrip()

def get_good_morning_wish():
    with open("wishes/good_morning_wishes.txt", 'r') as f:
        return choice(f.readlines()).rstrip()

def get_random_answer():
    answers = ["Да", "Нет", "Определенно", "100%", "Точно нет", "Вероятно", "Вряд ли", "Скорее всего",
               "Может быть", "Не знаю", "Не в моей компетенции", "Спроси еще раз", "Мне подсказывают, что да",
               "Думаю да", "50/50", "Tough question", "Несомненно", "Нет же", "Мда, ну и вопрос тупой",
               "Daubi", "Я, во всяком случае, в это верю", "Безусловно", "0%", "ДА И ТОЧКА", "НЕТ И ТОЧКА",
               "Это точно правда, можете даже не сомневаться", "Это не может быть правдой", "Нет. Закрыли тему"]
    shuffle(answers)
    return choice(answers)
