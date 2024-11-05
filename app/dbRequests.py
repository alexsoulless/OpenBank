import mysql.connector
from mysql.connector import pooling
import mysql.connector.cursor
from config import DB_PASSWORD, DB_USER, DB_HOST, DB_NAME, DB_PORT
from OBclasses import *


def connectToDB()-> bool:
    global pool
    pool = connectionPool()
    if pool is not None:
        return True
    return False


def connectionPool() -> pooling.MySQLConnectionPool | None:
    """Создание пула подключений

    Returns:
        pooling.MySQLConnectionPool | None: возвращает пул подклчений, либо None если возникли ошибки
    """
    db_config = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME,
    }
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="mypool", pool_size=10, pool_reset_session=True, **db_config
        )
        return connection_pool
    except Exception:
        return None


def getConnection(pool: pooling.MySQLConnectionPool) -> pooling.PooledMySQLConnection:
    return pool.get_connection()


def getCursor(conn: pooling.PooledMySQLConnection) -> mysql.connector.cursor:
    """Возвращает курсор. Курсор буферизирванный, извлакать данные нужно как из генератора/итератора

    Args:
        conn (pooling.PooledMySQLConnection): соединение

    Returns:
        mysql.connector.cursor: курсор
    """
    return conn.cursor(buffered=True)


def getUser(
    pool: pooling.MySQLConnectionPool,
    id: UserID | None = None,
    username: str | None = None,
    FIO: str | None = None,
) -> dict | None:
    """Возвращает всю информацию о пользователе по id или username или ФИО. ВАЖНО! Использовать только с 1 из критериев отбора.

    Args:
        pool (pooling.MySQLConnectionPool): пул соединений
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

        При ошибке выполнения функции возвращает None (напр. передано несколько критериев)
    """
    if [id, username, FIO].count(None) != 2:
        return None
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
SELECT * FROM users
WHERE {} = {}
"""
    values = ()
    if id is not None:
        values = ("id", f"{id}")
    elif username is not None:
        values = ("username", f"'{username}'")
    else:
        values = ("FIO", f"'{FIO}'")

    cursor.execute(query.format(*values))
    try:
        res = next(cursor)
    except Exception:
        return {}

    cursor.close()
    conn.close()

    if res:
        id, username, FIO, balance, isBanned, isOrg = res
        return {
            "id": id,
            "username": username,
            "FIO": FIO,
            "balance": balance,
            "isBanned": isBanned,
            "isOrg": isOrg,
        }
    else:
        return {}
    

if __name__ == "__main__":
    pool = connectionPool()
    if pool == None:
        print("error on db connect")
        exit(1)

    print(getUser(FIO="Абрамович Александр Владимирович"))
