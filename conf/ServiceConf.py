from datetime import timedelta
import random
from string import ascii_letters, digits
from utils.my_path import get_root_path

# 服务端开启时需要绑定的端口
BIND_PORT = 1234

# 服务端开启时候需要绑定的地址
BIND_ADDRESS = "192.168.0.105"

# 是否开启多线程
THREADED = True

# session 是否使用原来的秘钥 配置为True时 即使服务重启以前的session也不会失效
IS_USE_BEFORE_KEY = True

# session 使用的秘钥当上面的参数为False 此参数才会有作用
SECRET_KEY = ''.join(random.choices(ascii_letters + digits, k=32))

# session 存活的时间
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# 是否是否打印原来的日志信息
ORIGINALLY_LOG = None


if IS_USE_BEFORE_KEY:
    with open(get_root_path() + "SecretKey/session_key.pem", 'r') as f:
        SECRET_KEY = f.read()
else:
    with open(get_root_path() + "SecretKey/session_key.pem", 'w') as f:
        f.write(SECRET_KEY)

all_config = {
    "THREADED": THREADED,
    "SECRET_KEY": SECRET_KEY,
    "PERMANENT_SESSION_LIFETIME": PERMANENT_SESSION_LIFETIME
}
if __name__ == '__main__':
    print(SECRET_KEY)