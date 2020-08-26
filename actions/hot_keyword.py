from base.action_base import BaseAction
from flask import request
from utils import my_response
import random


class HotKeywordAction(BaseAction):

    def __init__(self, db_pool):
        super().__init__(db_pool)
        self.request_data = request.args

    def start_search(self):
        try:
            keyword_id, keyword = self._get_rand_keyword()
            if keyword_id > 0:
                keyword_id = str(keyword_id).zfill(11)
                self.res_data.set_status_code(my_response.Status.OK)
                self.res_data.set_data({"keyword_id": keyword_id, "keyword": keyword})
                self.log_data.res_data = {
                    "user_id": self.user_id,
                    "keyword_id": keyword_id
                }
            else:
                raise Exception("Hot keyword is empty")
        except Exception as e:
            self.res_data.set_status_code(my_response.Status.ERROR)
            self.res_data.set_data({})
            self.log_data.res_data = {
                "user_id": self.user_id,
                "error": str(e)
            }

    def _get_rand_keyword(self) -> (int, str):
        query_sql = """
            SELECT id,keyword
            FROM rs_product_keyword_search_info
            WHERE id = %s
        """
        result = -1, ""
        max_id = self._get_max_id()
        for i in range(10):
            cnt = self.db_cursor.execute(query_sql, random.randint(0, max_id))
            if cnt != 0:
                result = self.db_cursor.fetchall()[0]
                break
        return result

    def _get_max_id(self) -> int:
        sql = """
            SELECT max(id)
            FROM rs_product_keyword_search_info
        """
        self.db_cursor.execute(sql)
        max_id = self.db_cursor.fetchall()[0][0]
        return max_id

