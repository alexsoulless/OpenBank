# UPD теперь здесь будет импорт из файла app/.env 
# Чтобы добавить нужную тебе константу дописывай её в конце файла в том же формате и добавляй в файл app/.env
# Файл app/.env ОБЯЗАТЕЛЬНО должен быть в .gitignore, будем им обмениваться периодически через тг

import dotenv

config = dotenv.dotenv_values()

TELEGRAM_API_KEY = config["TELEGRAM_API_KEY"]
API_PATH = config["API_PATH"]
DB_PASSWORD = config["DB_PASSWORD"]
DB_USER = config["DB_USER"]
DB_HOST = config["DB_HOST"]
DB_PORT = config["DB_PORT"]
DB_NAME = config["DB_NAME"]
