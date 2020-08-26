from DBUtils.PooledDB import PooledDB
from utils import my_response
from base.db_opt_base import DBOptBase
from utils.secret_key_util import MyMD5
from utils.secret_key_util import MyRSA
from utils.ResAndLogBean import ResAndLogBean
from flask import session


class AddUserBean:
    def __init__(self, user_info):
        self.user_name = user_info.get("user_name")
        self.password = user_info.get("password")
        self.gender = user_info.get("gender")
        self.phone = user_info.get("phone")
        self.email = user_info.get("email")
        self.question = user_info.get("question")
        self.answer = user_info.get("answer")

    def create_sql(self):
        sql = "INSERT INTO rs_user_info(" \
              "`user_name`," \
              "`password`," \
              "`gender`," \
              "`phone`," \
              "`email`," \
              "`question`," \
              "`answer`," \
              "`create_time`," \
              "`update_time`) " \
              "VALUES(%s,%s,%s,%s,%s,%s,%s,NOW(),NOW());"
        values = [
            self.user_name,
            self.password,
            self.gender,
            self.phone,
            self.email,
            self.question,
            self.answer
        ]
        return sql, values


class SignUp(DBOptBase):

    def __init__(self, pool: PooledDB, data: dict, res_and_log: ResAndLogBean):
        super().__init__(pool)
        self.request_data = data
        self.response_data = res_and_log.get_res_data()
        self.log_data = res_and_log.get_log_data()
        self.add_user_bean = AddUserBean(data)

    def signup(self):
        if self.find_user_exists():
            self.response_data.set_status_code(my_response.Status.USER_EXISTED)
            self.response_data.set_message("用户名已存在")
            return
        status_rsa, password_rel = MyRSA.decryption(self.add_user_bean.password.encode("utf-8"))

        if status_rsa:
            status_md5, password_md5 = MyMD5.change_to_md5(password_rel)
            if status_md5:
                self.response_data.set_status_code(my_response.Status.MD5_ERROR)
                self.response_data.set_message("注册提交异常")
            self.add_user_bean.password = password_md5
            is_commit, user_id = self.commit()
            if is_commit:
                self.response_data.set_message("注册成功")
                self.response_data.set_status_code(my_response.Status.OK)
                self.response_data.set_user_id(str(user_id).zfill(11))
                self.response_data.set_user_name(self.request_data.get("user_name"))
                self.log_data.res_data = {"user_id": self.response_data.get_user_id()}
                session["user_id"] = self.response_data.get_user_id()
                session["user_name"] = self.request_data.get("user_name")

            else:
                self.response_data.set_message("注册失败")
                self.response_data.set_status_code(my_response.Status.ERROR)
        else:
            self.response_data.set_status_code(my_response.Status.DECRYPTION_ERROR)
            self.response_data.set_message("注册提交异常")

    def commit(self):
        sql, values = self.add_user_bean.create_sql()
        stat = self.db_cursor.execute(sql, values)
        user_id = self.find_user_exists()
        return stat, user_id

    def find_user_exists(self):
        self.db_cursor.execute("SELECT id FROM rs_user_info WHERE user_name=%s;", self.add_user_bean.user_name)
        user_id = None
        search_data = self.db_cursor.fetchall()
        if search_data:
            user_id = search_data[0][0]
        return user_id


if __name__ == '__main__':
   pass
