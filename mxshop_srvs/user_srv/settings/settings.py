from playhouse.pool import PooledMySQLDatabase

from playhouse.shortcuts import ReconnectMixin


# mysql gone away
# 使用 peewee的连接池, 使用 ReconnectMixin防止连接断开查询失败

class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


MYSQL_DB = "mxshop_user_srv"
MYSQL_HOST = "159.75.37.58"
MYSQL_PORT = 3306
MYSQL_USER = "mxshop_user_srv"
MYSQL_PASSWORD = "mxshop_user_srv"
DB = ReconnectMysqlDatabase(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD)
