from datetime import datetime, timedelta


def calculate_date_difference(date_time_from: str, date_time_to: str) -> timedelta:
    """
    Вычисляет разницу между двумя датами в формате ISO 8601.

    :param date_time_from: Начальная дата в формате строки (ISO 8601).
    :param date_time_to: Конечная дата в формате строки (ISO 8601).
    :return: Разница между датами в виде объекта timedelta.
    """

    # Преобразуем строки в объекты datetime
    dt_from = datetime.fromisoformat(date_time_from.replace("Z", "+00:00"))
    dt_to = datetime.fromisoformat(date_time_to.replace("Z", "+00:00"))

    difference = dt_to - dt_from
    print("Разница в днях:", difference.days)
    print("Разница в секундах:", difference.seconds)
    print("Общая разница:", difference)
    return difference

def subtract_days(date_time_to: str, days: int, inclusive: bool = True) -> datetime:
    """
    Вычитает заданное количество дней из указанной даты.

    :param date_time: Дата в формате строки ("%Y-%m-%d").
    :param days: Количество дней для вычитания.
    :param inclusive: Если True, вычитает дни включительно (учитывает конечную дату).
                     Если False, вычитает дни исключительно.
    :return: Новая дата в виде объекта datetime.
    """

    # try:
    #     dt = datetime.fromisoformat(date_time_to.replace("Z", "+00:00"))
    # except ValueError:
    #     dt = datetime.strptime(date_time_to, "%Y-%m-%d")
    
    dt = datetime.strptime(date_time_to, "%Y-%m-%d")
    
    if inclusive:
        # Вычитаем (days - 1) для включения конечной даты
        return dt - timedelta(days=days - 1)
    else:
        # Вычитаем days для исключения конечной даты
        return dt - timedelta(days=days)


if __name__ == "__main__":
    print(f'разница между timestamps на бэке равна {calculate_date_difference("2024-08-12T21:00:22Z", "2024-10-11T14:00:22Z")}\n')
    print(f'date_time_from на фронте должна быть {subtract_days("2024-10-11", 60, inclusive=True)}')