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


class reqType:
	item = "item/"
	ping = "ping/"

def baseGetRequest(
		type : reqType | None, 
		params : dict | None
		) -> dict:
	return json.loads(rq.get(config.API_PATH + type, params).content)

if __name__ == "__main__":
	print(baseGetRequest(reqType.ping, {"q" : 123}))