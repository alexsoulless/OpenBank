import config
import requests as rq
import json
from datetime import datetime
from classes import User, Transaction, Currency, Tax


class ReqType:
    ping = "ping/"


class getReqType(ReqType):
    getUser = "/users"
    findUser = "/users/find"
    getTransactionsPage = "/transactions"
    getTaxes = "/taxes"
    getTax = "/taxes/{}"
    getTaxStats = "/taxes/{}/stats"
    getTaxDefaulters = "/taxes/{}/defaulters"
    getCreditRequests = "/credits"
    getCreditRequest = "/credits/{}"


class postReqType(ReqType):
    setUserBalance = "/users/{}"
    userTransaction = "/transactions"
    newTax = "/taxes"
    editTax = "/taxes/{}"
    newTaxPayment = "/taxes/payments"
    changeUserStatus = "/users/{}/status"
    postCreditRequest = "/credits"
    setCreditRequestStatus = "/credits/{}"


def baseGetRequest(type: getReqType | None, params: dict | None) -> dict | None:
    try:
        reqRes = rq.get(config.API_PATH + type, params)
    except Exception:
        return None  # TODO logging
    deserRes = json.loads(reqRes.content)  # десериализованный результат
    return deserRes


def basePostRequest(type: postReqType | None, params: dict | None) -> dict | None:
    try:
        reqRes = rq.post(config.API_PATH + type, params)
    except Exception:
        return None  # TODO logging
    if reqRes.status_code != 200:
        return None
    deserRes = json.loads(reqRes.content)  # десериализованный результат
    return deserRes


def pingReq() -> dict:
    return baseGetRequest(ReqType.ping)


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
    res = baseGetRequest(
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


def findUser(pattern: str) -> list[User] | None:
    """Поиск имён пользователей и ФИО в базе данных, похожих на паттерн. Длина патерна должна быть больше 3 символов.

    Args:
        pattern (str): паттерн, по которому будет произведен поиск

    Returns:
        list[User] | None: Возвращает id, username, FIO найденных пользователей в виде ((id1, username1, FIO1), (id2, username2, FIO2), ...) при удачном запросе. Если при запросе возникла ошибка, вернёт None.
    """
    if len(pattern) < 3:
        return None
    finded = baseGetRequest(getReqType.findUser, {"pattern": pattern})
    res = []
    for i in finded:
        res.append(User(**i))
    if res:
        return res
    return None


def postTransaction(
    sender: str, recipient: str, sum: Currency, forced: bool = False
) -> int:
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


def getTaxes() -> tuple[Tax] | None:
    """Возвращает всю информацию о существующих налогах.

    Returns:
        tuple[Tax] | None: налог, если запрос успешен, иначе None
    """
    pass


def getTax(taxId: int) -> Tax | None:
    """Возвращает налог по Id

    Args:
        taxId (int): Id налога

    Returns:
        Tax | None: возвращает объект Tax, либо None при ошибке
    """
    pass


def newTax() -> int | None:
    """Создаёт новый налог в системе

    Returns:
        int|None: Id нового налога или None, если неудачно
    """
    pass


def editTax(
    taxId: int, newDateTime: datetime = None, newSum: int = None, newName: str = None
) -> int:
    """Запрос на изменение налога

    Args:
        taxId (int): Id налога, который редактируем
        newDateTime (datetime, optional): новое датавремя, когда налог должен быть выплачен. Defaults to None.
        newSum (int, optional): Новая сумма налога. Defaults to None.
        newName (str, optional): Новое название налога. Defaults to None.

    Returns:
        int: Код выхода. 0 - успешно, 1 - нет
    """
    pass


def getTaxStats(taxId: int) -> tuple[Tax, int, int]:
    """Возвращает налог и статистику сбора по нему

    Args:
        taxId (int): Id налога

    Returns:
        tuple[Tax, int]: налог; кол-во человек, заплативших налог; кол-во налогоплательщиков
    """
    pass


def getTaxDefaulters(taxId: int) -> tuple[tuple[int, str, str]]:
    """Возвращает список должников по определённому налогу

    Args:
        taxId (int): Id налога

    Returns:
        tuple[tuple[int, str, str]]: кортеж, каждый элемент - (id, username, FIO) участника, который не заплатил данный налог
    """
    pass


def newTaxPayment(taxId: int, userId: int) -> int:
    """Создаёт новую выплату по налогу. Используется в том случае, если участник оплатил налог наличной валютой.

    Args:
        taxId (int)
        userId (int)

    Returns:
        int: Код выхода. 0 - успешно, 1 - нет
    """
    pass


def setUserBalance(username, newBalance):
    pass


def changeUserStatus(username):
    pass


def postCreditRequest():
    pass


def getCreditRequests():
    pass


def getCreditRequest():
    pass


def setCreditRequestStatus(id, status):
    pass


if __name__ == "__main__":
    r = findUser("лек")

    for i in r:
        print(i)
