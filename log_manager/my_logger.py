import logging
import logging.handlers
import sys
from conf import LoggerConf
from logging.handlers import TimedRotatingFileHandler

"""
    @author:zh123
    @date: 2020-02-13
    @doc:
        1.初始化一个写日志的对象
        2.在对其导入相应的配置
        3.用于别处写日志用
"""


my_logger = logging.getLogger()                                         # 初始化日志管理对象


def set_logger():
    my_logger.setLevel(LoggerConf.LOG_LEVEL)                            # 设置日志级别

    formatter = logging.Formatter(LoggerConf.LOG_LINE_FORMAT)           # 初始化一个日志行的日志格式

    console_handler = logging.StreamHandler(sys.stdout)                 # 创建一个控制台的处理对象

    console_handler.setFormatter(formatter)                             # 为这个处理对象设置输出格式

    my_logger.addHandler(console_handler)                               # 将控制台的处理对象添加到日志管理对象当中

    file_handler = TimedRotatingFileHandler(                            # 创建一个文件输出的处理对象(根据时间划分日志)
        filename=LoggerConf.LOG_FILE_NAME,
        when=LoggerConf.LOG_FILE_WHEN,
        interval=LoggerConf.LOG_FILE_INTERVAL,
        backupCount=LoggerConf.LOG_FILE_BACKUP_COUNT,
        encoding="utf-8")

    file_handler.suffix = LoggerConf.LOG_FILE_SUFFIX                     # 自定义日志文件文件名的后缀格式

    file_handler.setFormatter(formatter)                                 # 为处理对象设置日志输出格式

    my_logger.addHandler(file_handler)                                   # 将处理对象添加到日志管理对象当中


set_logger()                                                            # 在导入之前先行调用进行配置
