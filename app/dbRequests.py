import mysql.connector
from mysql.connector import pooling
import mysql.connector.cursor
from config import DB_PASSWORD, DB_USER, DB_HOST, DB_NAME, DB_PORT
from classes import User, Transaction, Tax, TaxPayment, Currency, CreditRequest


def connectToDB() -> bool:
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
        "port": DB_PORT,
    }
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="mypool", pool_size=20, pool_reset_session=True, **db_config
        )
        return connection_pool
    except Exception:
        return None


def getConnection(pool: pooling.MySQLConnectionPool) -> pooling.PooledMySQLConnection:
    return pool.get_connection()


def getCursor(conn: pooling.PooledMySQLConnection) -> mysql.connector.cursor:
    """Возвращает курсор. Курсор буферизирванный, извлекать данные нужно как из генератора/итератора

    Args:
        conn (pooling.PooledMySQLConnection): соединение

    Returns:
        mysql.connector.cursor: курсор
    """
    return conn.cursor(buffered=True)


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
        User | None: Возвращается найденного пользователя, либо None.
    """
    if [id, username, FIO].count(None) != 2:
        return None
    global pool
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
    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return User(*res[0])
    else:
        return None


def setUserStats(
    id: int, balance: int | None = None, isBanned: bool | None = None
) -> User | None:
    """Обновляет атрибуты пользователя

    Args:
        id (int): id пользователя
        balance (int | None, optional): Новый баланс пользователя. Defaults to None.
        isBanned (bool | None, optional): заблокирован или нет. Defaults to None.

    Returns:
        User | None: возвращает экземпляр пользователя с актуальными полями если удачно, иначе None
    """
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    cond = ""

    if balance is not None and isBanned is not None:
        cond = f"balance = {balance}, isBanned = {isBanned}"
    elif balance is not None:
        cond = f"balance = {balance}"
    elif isBanned is not None:
        cond = f"isBanned = {isBanned}"

    query = f"""
UPDATE USERS
SET {cond}
WHERE id = {id};
"""
    cursor.execute(query)
    conn.commit()

    query = f"""
SELECT * FROM users
WHERE id = {id};
"""
    cursor.execute(query)

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return User(*res[0])
    else:
        return None


def findUser(pattern: str) -> list[User]:

    def isRu(s: str) -> bool:
        """Определяет русская ли 1 буква в строке по unicode символа"""
        return ord(s[0]) in range(1040, 1104)

    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    if isRu(pattern):
        query = """
SELECT * FROM users
where FIO like %s;
"""
    else:
        query = """
SELECT * FROM users
where username like %s;
"""
    pattern = f"%{pattern}%"
    cursor.execute(query, [pattern])
    res = [User(*i) for i in cursor]

    cursor.close()
    conn.close()

    return res


def getCreditRequests() -> list[CreditRequest]:
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = f"""
SELECT * FROM creditrequest
"""
    cursor.execute(query)

    res = [CreditRequest(*i) for i in cursor]

    cursor.close()
    conn.close()

    return res


def getCreditRequest(id: int) -> CreditRequest | None:
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
SELECT * FROM creditrequest
where id = %s
"""
    cursor.execute(query, params=[id])

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return CreditRequest(*res[0])
    else:
        return None


def postCreditRequest(
    userId: int,
    purpose: str,
    sum: Currency,
    status: int,
):
    global pool
    conn = getConnection(pool)
    cursor = getCursor(conn)

    query = """
INSERT INTO creditrequest(userId, purpose, sum, status) 
VALUES (%s, %s, %s, %s); 
"""
    cursor.execute(query, [userId, purpose, sum, status])
    conn.commit()

    query = """
SELECT * FROM creditrequest
WHERE id = %s;
"""
    cursor.execute(query, [cursor.lastrowid])

    res = [i for i in cursor]

    cursor.close()
    conn.close()

    if res:
        return CreditRequest(*res[0])
    else:
        return None


if __name__ == "__main__":
    if not connectToDB():
        raise Exception("Failed connect to DB")

    # print(setUserStats(3, balance=12))
    # print(getUser(3))
    print(postCreditRequest(3, "я хочу питсы", 100, 1))
