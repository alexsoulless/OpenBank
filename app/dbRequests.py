import mysql.connector
from mysql.connector import pooling
import mysql.connector.cursor
from config import DB_PASSWORD, DB_USER, DB_HOST, DB_NAME, DB_PORT


def connectionPool() -> pooling.MySQLConnectionPool | None:
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
    
def getConnection(pool : pooling.MySQLConnectionPool) -> pooling.PooledMySQLConnection:
    return pool.get_connection()

def getCursor(conn : pooling.PooledMySQLConnection) -> mysql.connector.cursor:
    return conn.cursor(buffered=True)


if __name__ == "__main__":
    pool = connectionPool()
    if pool == None:
        print("error on db connect")
        exit(1)
    
    conn = getConnection(pool)
    cursor = getCursor(conn)
    
    query = """
SHOW COLUMNS FROM users
"""
    cursor.execute(query)
    
    for line in cursor:
        print(line)

    cursor.close()
    conn.close()
    
    
