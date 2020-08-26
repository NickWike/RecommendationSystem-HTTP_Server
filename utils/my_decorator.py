from log_manager.my_logger import my_logger
from functools import wraps

from flask import make_response
from flask import session
from flask import jsonify
from flask import redirect
from flask import url_for
import time

"""
    @author:zh123
    @date: 2020-02-20
    @description:
        此模块主要是一些装饰器的定义
"""


def db_operation(func):
    """
    关于数据库连接池的一些操作,主要是获取连接和释放连接
    :param func:
    :return: <class name=function>
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        res = None
        try:
            res = func(self, *args, **kwargs)
        except Exception as e:
            my_logger.error("errorMessage({err}),<{funcname}>".format(
                err=e,
                funcname=func.__name__))
        finally:
            self.close()
            return res
    return wrapper


def need_session(func):
    @wraps(func)
    def wrapper():
        if session.get('user_id'):
            return func()
        else:
            return redirect(url_for("login"), code=302)
    return wrapper


def response_and_logging(func):
    """
    此装饰器用于response的构建,和日志的书写
    :param func:
    :return: <class name=function>
    """
    @wraps(func)
    def wrapper():
        # print(request.referrer)                                           # 获取日志数据的一个结构体
        start_time = time.time()
        route_res = func()
        res_and_log_bean = route_res
        res_and_log_bean.log_data_init()
        log_data = res_and_log_bean.get_log_data()
        res_data = res_and_log_bean.get_res_data()

        end_time = time.time()
        log_data.res_duration = "%.3f" % ((end_time - start_time)*1000)

        res_data.set_time_stamp(int(end_time*1000))

        response = make_response(jsonify(res_data.get_all_data()))                  # 构造response
        response.status = "200"                                                 # 响应码
        my_logger.info(**log_data.get_all_data())                                   # 写入日志
        return response

    return wrapper
