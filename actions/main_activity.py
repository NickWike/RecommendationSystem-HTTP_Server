from base.action_base import BaseAction
from utils import my_response
import random


class MainInitAction(BaseAction):
    def __init__(self, db_pool):
        super().__init__(db_pool)
        self.product_list = []
        self.product_cnt = random.randint(10, 15)

    def init_recommend_product(self):
        try:
            self.find_recommend_product()       # 在数据库中查找用户需要推荐的商品
            self.complement_product()           # 当推荐数量不足cnt的数量时自动补全
            self.res_data.set_message(my_response.Status.get_status_text(my_response.Status.OK))
            self.res_data.set_status_code(my_response.Status.OK)
            self.res_data.set_items(self.product_list)
            self.log_data.res_data = {
                "user_id": self.user_id,
                "items": [it["product_id"] for it in self.product_list]
            }
        except Exception as e:
            self.res_data.set_message(my_response.Status.get_status_text(my_response.Status.ERROR))
            self.res_data.set_status_code(my_response.Status.ERROR)
            self.log_data.res_data = str(e)

    def find_recommend_product(self):
        sql = """
                SELECT id,name,image_url,price,average_score,comment_count
                FROM rs_product_base_info AS RPBI,
                    rs_product_sales_info AS RPSI,
                    rs_product_recommend_info AS RPRI
                WHERE RPBI.id = RPSI.product_id
                    AND RPBI.id = RPRI.product_id
                    AND RPRI.user_id = %s 
                    AND RPRI.status = 1
                    AND RPBI.status = 1
                 ORDER BY recommend_rate DESC
                 LIMIT 5;
        """
        self.db_cursor.execute(sql, self.user_id)
        query_data = self.db_cursor.fetchall()
        for row in query_data:
            product_info = self.row_to_dict(row)
            self.product_list.append(product_info)

    def complement_product(self):
        sql = """
                SELECT id,name,image_url,price,average_score,comment_count
                FROM rs_product_base_info,
                     rs_product_sales_info
                WHERE id = product_id
                AND id = %s
        """
        self.db_cursor.execute("SELECT MAX(id) FROM rs_product_base_info")
        max_id = self.db_cursor.fetchall()[0][0]
        while len(self.product_list) < self.product_cnt:
            rand_id = random.randint(0, max_id)
            query_cnt = self.db_cursor.execute(sql, rand_id)
            if query_cnt:
                row = self.db_cursor.fetchall()[0]
                product_info = self.row_to_dict(row)
                self.product_list.append(product_info)

    @staticmethod
    def row_to_dict(row):
        product_info = {"product_id": str(row[0]).zfill(11),
                        "product_name": row[1],
                        "product_image": row[2],
                        "price": str(row[3]),
                        "average_score": str(row[4]),
                        "comment_count": row[5]}
        return product_info


if __name__ == '__main__':
    from DBUtils.PooledDB import PooledDB
    from conf import DBConf

    DB_CONNECTION_POOL = PooledDB(**DBConf.all_config)
    with MainInitAction(DB_CONNECTION_POOL, 1, 10) as m:
        m.init_recommend_product()
        for item in m.product_list:
            print(item)
