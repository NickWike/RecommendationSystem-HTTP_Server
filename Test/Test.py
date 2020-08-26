# from log_manager.MyLogger import my_logger
# from utils.MyPath import get_root_path
#
# def base_handle(func):
#     def wrapper(self, *args, **kwargs):
#         res = None
#         try:
#             res = func(self, *args, **kwargs)
#         except Exception as e:
#             pass
#         finally:
#             my_logger.info("execute,<{funcname}>".format(
#                 funcname=func.__name__))
#             return res
#     return wrapper
#
#
# class T:
#     name = "test"
#
#     def who_am_i(self, n):
#         print(self.name, n)
#
#     def logger(self):
#         print("日志")
#
#     def close(self):
#         print("已经关闭")
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.close()
#
#
# class Bean:
#     def __init__(self):
#         self.status = 20
#         self.message = "test"
#         self.age = 23
#         self.ids = [1,2,3,4,5,6]
#
#     def t(self):
#         for name in dir(self):
#             if not name.startswith("__"):
#                 print(name,type(getattr(self,name)))
#
#
# if __name__ == '__main__':
#     print(get_root_path())


import redis
import threading
from conf.RedisConfig import ALL_ARGUMENTS
import random
from string import ascii_letters,digits
import time

pool = redis.ConnectionPool(**ALL_ARGUMENTS)


def task():
    global num
    conn = redis.Redis(connection_pool=pool)

    for i in range(10):
        print(conn.incr(name="product:num", amount=1))
    conn.close()
    # with conn.pipeline() as pipe:
    #     for _ in range(3):
    #         try:
    #             pipe.watch("")


    # with conn.pipeline() as ctx:
    #     m = int(ctx.get("num"))
    #     m = m or 0
    #     ctx.set("num", m + 1)
    #     ctx.execute()
    # num += 1

#
# for i in range(100):
#     t = threading.Thread(target=task, args=())
#     t.start()
# task()
# task()

# print(num)
s = ""
for i in range(25):
    s += "".join(random.choices(ascii_letters+digits, k=199)) + "\n"

# print(s)

c = redis.Redis(connection_pool=pool)
# for key in c.keys():
#     c.delete(key)

start_time = time.time()
# c.set("name:name:star:dsa4f56das4f65d4f4dasf6d4asf6", s)
# c.get("name:name:star:dsa4f56das4f65d4f4dasf6d4asf6")
print(c.keys())
# print(c.get("rs:order:commit:token:b914c5502c3f0c0483e3194d4203d767"))
print(time.time() - start_time)
c.close()
