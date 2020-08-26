from flask import request
from utils import my_response
from log_manager.log_data_struct import LogDataStruct


class ResAndLogBean:
    def __init__(self):
        self._log_data = LogDataStruct()
        self._res_data = my_response.DataStruct()

    def log_data_init(self):
        self._log_data.res_status = self._res_data.get_status_code()
        self._log_data.remote_address = request.remote_addr
        self._log_data.req_http_info = request.environ.get("SERVER_PROTOCOL")  # http版本
        self._log_data.req_path = request.path  # 请求地址
        self._log_data.req_method = request.method  # 请求类型
        self._log_data.log_message = self._res_data.get_status_text()      # 获取消息内容
        if request.headers.get("referrer"):
            self._log_data.req_referrer = request.headers.get("referrer")  # 上一跳地址

    def get_log_data(self):
        return self._log_data

    def get_res_data(self):
        return self._res_data
