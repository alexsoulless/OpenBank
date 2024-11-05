from datetime import datetime


class currency(int):
    """
    Валюта. Целое число, можно изменить
    """

    pass


class ID(int):
    pass


class TransactionID(ID):
    pass


class UserID(ID):
    pass


class TaxID(ID):
    pass


class TaxPaymentID(ID):
    pass


class CreditRequestID(ID):
    pass


class UserName(str):
    """
    Имя пользователя в tg
    """

    pass


class creditRequestStatus(int):
    """
    Статус кредитной заявки
    1 - отправлена
    2 - рассматривается
    3 - одобрена
    4 - отклонена
    """

    pass


class User:
    def __init__(
        self,
        id: UserID,
        username: UserName,
        FIO: str,
        balance: currency,
        isBanned: bool,
        isOrg: bool,
    ):
        self.id = id
        self.username = username
        self.FIO = FIO
        self.balance = balance
        self.isBanned = isBanned
        self.isOrg = isOrg


class Transaction:
    def __init__(
        self,
        ID: TransactionID,
        fromID: UserID,
        toID: UserID,
        datetime: datetime,
        sum: currency,
    ):
        self.ID = ID
        self.fromID = fromID
        self.toID = toID
        self.datetime = datetime
        self.sum = sum


class TaxPayment:
    def __init__(self, ID: TaxPaymentID, userID: UserID, taxID: TaxID):
        self.ID = ID
        self.userID = userID
        self.taxID = taxID


class Tax:
    def __init__(self, ID: TaxID, sum: currency, datetime: datetime, name: str):
        self.ID = ID
        self.sum = sum
        self.datetime = datetime
        self.name = name


class creditRequest:
    def __init__(
        self,
        ID: CreditRequestID,
        userID: UserID,
        purpose: str,
        sum: currency,
        status: creditRequestStatus,
    ):
        self.ID = ID
        self.userID = userID
        self.purpose = purpose
        self.sum = sum
        self.status = status
