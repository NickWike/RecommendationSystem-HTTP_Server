from DBUtils.PooledDB import PooledDB
from utils.secret_key_util import MyRSA, MyMD5
from base.db_opt_base import DBOptBase
from utils import my_response
from flask import session
from utils.ResAndLogBean import ResAndLogBean


class LoginPost(DBOptBase):
    def __init__(self, pool: PooledDB, data: dict, res_and_log: ResAndLogBean):
        super().__init__(pool)
        self.response_data = res_and_log.get_res_data()
        self.request_data = data
        self.log_data = res_and_log.get_log_data()

    def login(self):
        user_name = self.request_data.get("user_name")                     # 获取参数姓名的值
        password_cipher = self.request_data.get("password")                # 获取参数中的密码(密文)
        commit_status, user_info = self.commit(user_name, password_cipher)

        # data = {"status": status, "id": user_info[0], "username": user_info[1], "timeStamp": int(time.time()*1000)}

        if commit_status == 0:
            self.response_data.set_status_code(my_response.Status.USER_NOT_EXISTS)
            self.response_data.set_message("用户不存在,请检查用户名是否输错")
        elif commit_status == 1:
            self.response_data.set_status_code(my_response.Status.OK)
            self.response_data.set_user_id(user_info)
            self.response_data.set_message("登录成功")
            self.response_data.set_user_name(self.request_data.get("user_name"))
            session["user_id"] = self.response_data.get_user_id()
            session["user_name"] = self.response_data.get_user_name()
            self.log_data.res_data = {"user_id": self.response_data.get_user_id()}
        elif commit_status == 2:
            self.response_data.set_status_code(my_response.Status.INVALID_PASSWORD)
            self.response_data.set_message("密码错误请,注意大小写")

    def commit(self, username: str, password: str) -> (int, str):
        result_data = None
        user_existed, user_id = self.find_user(username)
        if user_existed:
            password_corrected, user_info = self.compare_password(password, user_id)
            if password_corrected:
                result_status = 1
                result_data = user_info
            else:
                result_status = 2
        else:
            result_status = 0
        return result_status, result_data

    def find_user(self, username: str) -> (bool, str):
        result_status = True
        result_data = None
        sql = "SELECT `id` from `rs_user_info` WHERE user_name=%s"
        try:
            ret = self.db_cursor.execute(sql, [username])
            if ret:
                result_data = self.db_cursor.fetchall()[0][0]
            else:
                result_status = False
        except Exception as e:
            result_status = False
        finally:
            return result_status, result_data

    def compare_password(self, password: str, user_id: str) -> (bool, str):
        result_data = None
        result_status = False
        rsa_status, password_real = MyRSA.decryption(password.encode("utf-8"))
        if not rsa_status:
            return rsa_status, None
        md5_status, password_md5 = MyMD5.change_to_md5(password_real)
        if not md5_status:
            return md5_status, None
        sql = "SELECT id FROM rs_user_info WHERE id=%s AND password=%s"
        try:
            result_status = True
            cnt = self.db_cursor.execute(sql, [user_id, password_md5])
            if cnt:
                result_data = str(self.db_cursor.fetchall()[0][0]).zfill(11)
            else:
                result_status = False
        except Exception as e:
            result_status = False
            result_data = None
        finally:
            return result_status, result_data


class LoginGet:
    def __init__(self, params: dict, res_and_log: ResAndLogBean):
        self.request_params = params
        self.response_data = res_and_log.get_res_data()
        self.log_data = res_and_log.get_log_data()

    def login(self):
        if session.get("user_id"):
            return self._have_session()
        else:
            return self._no_session()

    def _no_session(self):
        self.response_data.set_message("你还没有登录请先登录")
        self.response_data.set_status_code(my_response.Status.NO_LOGIN)
        self.response_data.set_pub_key(MyRSA.now_public_pem.decode())

    def _have_session(self):
        user_id = session.get("user_id")
        user_name = session.get("user_name")
        self.response_data.set_message("登录成功")
        self.response_data.set_user_id(user_id)
        self.response_data.set_user_name(user_name)
        self.response_data.set_status_code(my_response.Status.OK)
        self.log_data.res_data = {"user_id": self.response_data.get_user_id()}
