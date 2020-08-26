"""
    Redis 配置文件
"""

# 访问地址
CONF__HOST = "localhost"
# 访问端口
CONF__PORT = "6379"
# 访问密码
CONF__PASSWORD = "123qwe"
# 是否以字节写入
CONF__DECODE_RESPONSES = True
# 允许的最大连接数 为None时表示为 2**31 个
CONF__MAX_CONNECTIONS = None


# ALL_ARGUMENTS =

__args = dict(locals())

# 用于外部批量导入全部参数使用
ALL_ARGUMENTS = {}

# 对全部参数进行转换
for k, v in __args.items():
    if k.startswith("CONF__"):
        ALL_ARGUMENTS[k.split("CONF__")[-1].lower()] = v
