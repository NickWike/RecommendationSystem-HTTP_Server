"""
    @author:zh123
    @date:2020-02-21
    @description:
        1.此模块主要用请求返回体的一些数据结构
        2.状态和返回信息等
"""


class Status:
    ERROR = -1                  # 未知异常标识
    DECRYPTION_ERROR = -2       # 解密异常
    MD5_ERROR = -3              # MD5码生成异常
    FAILURE = -4                # 失败 (一般用于数据的获取)
    NONE = 0                    # 空
    OK = 1                      # 成功标识
    NO_LOGIN = 2                # 没有登录
    NO_SIGN_UP = 3              # 没有注册成功
    NO_COOKIES = 4              # 没有COOKIES信息
    INVALID_PASSWORD = 5        # 密码不正确
    USER_EXISTED = 6            # 用户已存在
    USER_NOT_EXISTS = 7         # 用户不存在

    @staticmethod
    def get_status_text(code):                      # 将状态码转换成对相应的文本
        if code == Status.OK:
            return "OK"
        if code == Status.ERROR:
            return "ERROR"
        if code == Status.NONE:
            return "NONE"
        if code == Status.NO_LOGIN:
            return "NO_LOGIN"
        if code == Status.NO_SIGN_UP:
            return "NO_SIGN_UP"
        if code == Status.NO_COOKIES:
            return "NO_COOKIES"
        if code == Status.INVALID_PASSWORD:
            return "INVALID_PASSWORD"
        if code == Status.USER_EXISTED:
            return "USER_EXISTED"
        if code == Status.USER_NOT_EXISTS:
            return "USER_NOT_EXISTS"
        if code == Status.DECRYPTION_ERROR:
            return "DECRYPTION_ERROR"
        if code == Status.FAILURE:
            return "FAILURE"


class DataStruct:
    """
    返回体信息体结构
    """
    __status_code = None        # 状态码
    __status_text = None        # 状态信息
    __message = None            # 消息
    __time_stamp = None         # 时间戳
    __user_id = None            # 用户id
    __user_name = None          # 用户姓名
    __data = None            # cookies信息
    __pub_key = None            # 公钥
    __items = None              # 返回的数据项

    def get_items(self):
        return self.__items

    def set_items(self, items):
        self.__items = items

    def get_message(self):
        if self.__message:
            return self.__message

    def set_message(self, msg: str):
        self.__message = msg

    def get_status_code(self):
        return self.__status_code

    def set_status_code(self, status_code):
        self.__status_code = status_code
        self.__status_text = Status.get_status_text(status_code)

    def get_status_text(self):
        return self.__status_text

    def get_time_stamp(self):
        return self.__time_stamp

    def set_time_stamp(self, time_stamp):
        self.__time_stamp = time_stamp

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = str(user_id).zfill(11)

    def get_user_name(self):
        return self.__user_name

    def set_user_name(self,user_name):
        self.__user_name = user_name

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def get_pub_key(self):
        return self.__pub_key

    def set_pub_key(self, pub_key):
        self.__pub_key = pub_key

    def get_all_data(self):                                                      # 将整个数据格式化成字典,空值去掉
        data = {}
        for k in dir(self):
            if k.startswith("_DataStruct") and getattr(self, k) is not None:            # 捕获类结构中的非空私有变量
                data[k.split("__")[1]] = getattr(self, k)
        return data


if __name__ == '__main__':
    d = DataStruct()
    d.set_message("name")
    d.set_status_code(Status.OK)
    print(d.get_all_data())
