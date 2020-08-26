import logging as _logging
from utils.my_path import get_root_path
# 日志级别/INFO/DEBUG/ERROR/NOTSET/WARN/FATAL/CRITICAL
LOG_LEVEL = _logging.INFO

# 日志分隔符
LOG_SEQ = " - "

_log_types = ["[%(asctime)s]", "%(levelname)s",
              "%(remote_addr)s", "%(request_info)s",
              "%(message)s", "%(response_info)s"]

# 组合日志格式
LOG_LINE_FORMAT = LOG_SEQ.join(_log_types)

# 日志保存路径
LOG_FILE_NAME = get_root_path() + "logs/RS_Http_Server"

# 日志生成每个周期的基本单位 /日(D)/时(H)/分(M)/秒(S)/周(W)
LOG_FILE_WHEN = "D"

LOG_FILE_SUFFIX = "%Y-%m-%d_%H:%M:%S.log"

# 日志生成基本单位的周期
LOG_FILE_INTERVAL = 1

LOG_FILE_MAX_BYTES = 10485760

# 日志的保留个数 空表示全部保留
LOG_FILE_BACKUP_COUNT = 0

# 日志文件采用的编码
LOG_FILE_ENCODING = "utf-8"

