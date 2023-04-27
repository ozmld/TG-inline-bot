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
        return '2 win'
    return '1 win'
