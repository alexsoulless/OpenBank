import config
import requests as rq
import json

# В этом файле будут все запросы от тг бота к бэкенду на FastAPI
# Пиши сюда запросы в следущем виде:

def requestTemplate(value : str, a : int) -> int:
	"""	тут пиши docstring в таком формате. Их можно генерировать автоматически с помощью дополения autoDocstring в VSCode
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

class postReqType(
	ReqType
):
	pass

def _baseGetRequest(
		type : getReqType | None, 
		params : dict | None
		) -> dict:
	reqRes = rq.get(config.API_PATH + type, params)
	return json.loads(reqRes.content)

def pingReq(q : int) -> dict:
	return _baseGetRequest(getReqType.ping)

def getUserReq(
		id: int | None = None,
		username: str | None = None,
		FIO: str | None = None,
):
	"""Возвращает всю информацию о пользователе по id или username или ФИО. ВАЖНО! Использовать только с 1 из критериев отбора.

    Args:
        id (int | None, optional): ID пользователя. Defaults to None.
        username (str | None, optional): имя пользователя. Defaults to None.
        FIO (str | None, optional): ФИО пользователя. Defaults to None.

    Returns:
        dict | None: Все данные о пользователе в формате словаря:
        {
            "id": id,
            "username": username,
            "FIO": FIO,
            "balance": balance,
            "isBanned": isBanned,
            "isOrg": isOrg
        }
        Если пользователя не нашлось, словарь пустой.
		{}
        При ошибке выполнения функции возвращает None (напр. передано несколько критериев)
    """
	return _baseGetRequest(getReqType.getUser,{
		"id": id,
		"username": username,
		"FIO": FIO,
	})

if __name__ == "__main__":
	print(getUserReq(username="AlexSsoulless"))