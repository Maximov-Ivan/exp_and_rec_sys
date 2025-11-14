from math import sqrt


def pearson_similarity(ratings1: dict, ratings2: dict) -> float:
    """
    Вычисление коэффициента корреляции Пирсона между двумя векторами оценок

    :param dict ratings1: словарь оценок первого фильма
    :param dict ratings2: словарь оценок второго фильма
    :return float: коэффициент корреляции Пирсона
    """
    common_users = []
    for user in ratings1.keys():
        if user in ratings2.keys():
            common_users.append(user)
    n = len(common_users)
    if n < 2:
        return 0

    mean1 = sum(ratings1[user] for user in common_users) / n
    mean2 = sum(ratings2[user] for user in common_users) / n
    numerator = 0
    denom1 = 0
    denom2 = 0

    for user in common_users:
        diff1 = ratings1[user] - mean1
        diff2 = ratings2[user] - mean2
        numerator += diff1 * diff2
        denom1 += diff1**2
        denom2 += diff2**2

    if denom1 == 0 or denom2 == 0:
        return 0
    return numerator / (sqrt(denom1) * sqrt(denom2))
