from DBUtils.PooledDB import PooledDB

"""
    @author:zh123
    @date:2020-02-21
    @description:
        1.数据操作级基类
        2.需要用到数据库操作的模块继承进行使用
"""


class DBOptBase(object):
    def __init__(self, pool: PooledDB):
        self.__is_error = False                                 # 运行当中是否有错误
        self.db = pool.connection()                             # 初始化
        self.db_cursor = self.db.cursor()                       # 从连接池中获取连接并获取游标

    def error_occurred(self):
        self.__is_error = True                                  # 表明执行过程中出现错误

    def __enter__(self):
        return self                                             # 用于 with 操作时 返回自身

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__is_error:
            self.db.rollback()                                  # 如果发生错误则回滚
        else:
            self.db.commit()                                    # 没有错误时将事物进行提交
        self.db_cursor.close()                                  # with 结束时进行关闭,回收连接
        self.db.close()
