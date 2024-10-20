from mysql.connector import connect, Error
from config import DB_PASSWORD, DB_USER

try:
    with connect(
        host="localhost",
        user=DB_USER,
        password=DB_PASSWORD,
    ) as connection:
        print(connection)
except Error as e:
    print(e)

