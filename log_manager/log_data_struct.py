import json


class LogDataStruct:
    res_status = None
    log_message = ""
    req_method = None
    req_path = None
    remote_address = None
    req_http_info = None
    req_referrer = "/"
    res_duration = None
    res_data = None

    def __format_all_data(self):
        self.res_status = str(self.res_status)
        self.log_message = str(self.log_message)
        self.req_method = str(self.req_method)
        self.req_path = str(self.req_path)
        self.remote_address = str(self.remote_address)
        self.req_http_info = str(self.req_http_info)
        self.req_referrer = str(self.req_referrer)
        self.res_duration = "{0}ms".format(str(self.res_duration))
        self.res_data = "<{0}>".format(json.dumps(self.res_data))

    def get_all_data(self):
        self.__format_all_data()
        return {"msg": self.log_message,
                "extra": {
                    "remote_addr": self.remote_address,
                    "request_info": "`{0}`".format(" ~ ".join([self.req_method,
                                                               self.req_path,
                                                               self.req_http_info,
                                                               self.req_referrer])),

                    "response_info": "`{0}`".format(" ~ ".join([self.res_status,
                                                                self.res_duration,
                                                                self.res_data]))
                }
                }
