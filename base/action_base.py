from utils import my_response
from flask import session
from .db_opt_base import DBOptBase
from utils.ResAndLogBean import ResAndLogBean


class BaseAction(DBOptBase):
    def __init__(self, db_pool):
        super().__init__(db_pool)
        self.user_id = session.get("user_id")
        self.res_and_log_bean = ResAndLogBean()
        self.res_data = self.res_and_log_bean.get_res_data()
        self.log_data = self.res_and_log_bean.get_log_data()
        self.res_data.set_user_id(self.user_id)

    def finished(self):
        return self.res_and_log_bean
