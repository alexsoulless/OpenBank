import config
import requests as rq
import json
from classes import User, Transaction, Currency

# В этом файле будут все запросы от тг бота к бэкенду на FastAPI
# Пиши сюда запросы в следущем виде:


def requestTemplate(value: str, a: int) -> int:
    """тут пиши docstring в таком формате. Их можно генерировать автоматически с помощью дополения autoDocstring в VSCode
    Args:
            value (str): _description_
            a (int): _description_

    Returns:
            int: _description_
    """
    print(f"Был вызван requestTemplate с аргументом {value}")
    return a


# В последующем я буду реализовывать все запросы, которые ты сюда напишешь
# Имя функции должно отражать её суть, напр getHistoryPage() - запрос на получение страницы истории транзакций


class ReqType:
    ping = "ping/"


class getReqType(ReqType):
    getUser = "getUser/"


class postReqType(ReqType):
    pass


def _baseGetRequest(type: getReqType | None, params: dict | None) -> dict | None:
    try:
        reqRes = rq.get(config.API_PATH + type, params)
    except Exception:
        return None # TODO logging
    deserRes = json.loads(reqRes.content)  # десериализованный результат
    return deserRes


def pingReq(q: int) -> dict:
    return _baseGetRequest(getReqType.ping)


def getUser(
    id: int | None = None,
    username: str | None = None,
    FIO: str | None = None,
) -> User | None:
    """Возвращает всю информацию о пользователе по id или username или ФИО. ВАЖНО! Использовать только с 1 из критериев отбора.

    Args:
        id (int | None, optional): ID пользователя. Defaults to None.
        username (str | None, optional): имя пользователя. Defaults to None.
        FIO (str | None, optional): ФИО пользователя. Defaults to None.

    Returns:
        User | None: Возвращает объект пользователя если пользователь нашёлся.
        При ошибке выполнения функции возвращает None (напр. передано несколько критериев)
    """
    res = _baseGetRequest(
        getReqType.getUser,
        {
            "id": id,
            "username": username,
            "FIO": FIO,
        },
    )
    if res:
        return User(**res)
    return None


def findUser(pattern: str) -> tuple[tuple[int, str, str]] | tuple | None:
    """Поиск имён пользователей и ФИО в базе данных, похожих на паттерн. Длина патерна должна быть больше 4 символов.

    Args:
        pattern (str): паттерн, по которому будет произведен поиск

    Returns:
        tuple[tuple[int, str, str]] | None: Возвращает id, username, FIO найденных пользователей в виде ((id1, username1, FIO1), (id2, username2, FIO2), ...) при удачном запросе. Если при запросе возникла ошибка, вернёт None.
    """
    pass


def UserTransaction(sender: str, recipient: str, sum: Currency) -> int:
    """Транзакция между 2 пользователями

    Args:
        sender (str): отправитель
        recipient (str): получатель
        sum (Currency): сумма перевода
    Returns:
        int: Код завршения
        0 - успешно,
        1 - ошибка
    """
    pass


def getTransactionsPage(username: str, i: int) -> tuple[Transaction] | None:
    """Возвращает i-ую страницу истории транзакций пользователя.
    i >= 0. Каждая страница содержит 15 транзакций.

    Args:
        username (str): имя пользователя
        i (int): индекс нужной страницы

    Returns:

    """
    pass


if __name__ == "__main__":
    print(getUser(username="AlexSsoulless"))
