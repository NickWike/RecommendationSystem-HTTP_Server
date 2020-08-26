"""
    @author:zh123
    @date:2020-02-21
    @description:
        数据库链接池的相关配置
        all_config 用于传参时直接解包导入使用
"""
import pymysql

# 绑定的数据库操作器
CREATOR = pymysql

# 数据库绑定的端口
PORT = 3306

# 数据库绑定的地址
HOST = "localhost"

# 连接数据库的名称
DB_NAME = "RECOMMENDATION_SYSTEM_DB"

# 数据库的密码
PASSWORD = "123qweQWE"

# 数据库用户名
USERNAME = "root"

# 是否自动提交 (经过测试发现自动提交,会在每次执行sql后自动将事物进行提交,但是这样耗时也就比较多,所以还是在所有事物完成后最后统一提交)
SET_SESSION = None      # ['SET AUTOCOMMIT = 1']

# 最小的连接闲置数目,也是启动的初始量
MIN_CACHED = 0

# 最大的闲置数目 (0表示无限制)
MAX_CACHED = 0

# 共享连接的最大数量 (0表示无限制)
MAX_SHARED = 0

# 通常允许的最大连接数 (0表示无限制)
MAX_CONNECTIONS = 0

# 当连接数超过最大连接数时进行阻塞与否 (True 为阻塞,False 为非阻塞)
BLOCKING = False

# 每个连接的最大使用次数,如果使用次数超过此数会自动将连接进行重置 (0表示无限制)
MAX_USAGE = 0


all_config = {
    "creator":          CREATOR,
    "port":             PORT,
    "host":             HOST,
    "db":               DB_NAME,
    "user":             USERNAME,
    "passwd":           PASSWORD,
    "setsession":       SET_SESSION,
    "mincached":        MIN_CACHED,
    "maxcached":        MAX_CACHED,
    "maxshared":        MAX_SHARED,
    "maxconnections":   MAX_CONNECTIONS,
    "blocking":         BLOCKING,
    "maxusage":         MAX_USAGE
}