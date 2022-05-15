from functools import wraps

import MySQLdb
from config import DATABASE_USER, DATABASE_PWD, DATABASE_HOST, DATABASE_PORT
from config import DATABASE
from dbutils.pooled_db import PooledDB


# 使用连接池，blocking=True用处存疑
connection_pool = PooledDB(
    creator=MySQLdb,
    # blocking=True,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    user=DATABASE_USER,
    password=DATABASE_PWD
)

# 没有使用try catch块，编写代码时会跳过一些程序中的错误，不利于排查bug
def query_one(sql, num):
    ch_client = connection_pool.connection()
    cur = ch_client.cursor()
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    ch_client.close()
    if res is not None:
        return res
    else:
        return [None] * num

def query_many(sql, num):
    ch_client = connection_pool.connection()
    cur = ch_client.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    ch_client.close()
    if res is not None:
        return res
    else:
        return [None] * num

def Fail2None(func):
    @wraps(func)
    def Fail2None(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("[ERROR]", e)
            return None
    return Fail2None