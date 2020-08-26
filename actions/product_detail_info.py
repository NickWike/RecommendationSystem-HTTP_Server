from base.action_base import BaseAction
from flask import request
from pymysql.cursors import DictCursor
from utils import my_response
from utils import TypeTransform


class ProductDetailAction(BaseAction):
    def __init__(self, db_pool):
        super().__init__(db_pool)
        self.db_cursor = self.db.cursor(DictCursor)
        self.request_data = request.args
        self.query_items = set()
        for item in self.request_data["items"].split(";"):
            if item.isdigit():
                self.query_items = self.query_items | {int(item)}
        self.query_items = list(self.query_items)

    def batch_query(self):
        result_info_items = []
        query_sql = """
                SELECT rpbi.id as product_id,
                       rpbi.name as product_name,
                       rpbi.image_url as product_image,
                       rpbi.status as product_status,
                       rpbi.price as price,
                       rpbi.postage as postage,
                       rpsi.comment_count as comment_count,
                       rpsi.average_score as average_score,
                       rpsi.good_count as good_count,
                       rpsi.general_count as general_count,
                       rpsi.poor_count as poor_count,
                       rpsi.good_rate as good_rate,
                       rpsi.inventory as inventory,
                       rpsi.month_sales as month_sales,
                       rsi.id as shop_id,
                       rsi.name as shop_name,
                       rai.area_code as area_code,
                       rai.name as area_name
                FROM rs_product_base_info as rpbi,
                     rs_product_sales_info as rpsi,
                     rs_shop_info as rsi,
                     rs_area_info as rai
                WHERE
                     rpbi.id = rpsi.product_id AND
                     rpbi.shop_id = rsi.id AND
                     rsi.area_code = rai.area_code AND
                     rpbi.id = %s
        """
        try:
            for product_id in self.query_items:
                if self.db_cursor.execute(query_sql, product_id):
                    data_line = self.db_cursor.fetchall()[0]
                    format_line = TypeTransform.format_line(data_line)
                    result_info_items.append(format_line)
        except Exception as e:
            raise Exception("%s - batch_query execute error" % str(e))
        return result_info_items

    def start_task(self):
        try:
            info_items = self.batch_query()
            self.res_data.set_items(info_items)
            self.res_data.set_status_code(my_response.Status.OK)
            self.log_data.res_data = {
                "user_id": self.user_id,
                "items": [str(i).zfill(11) for i in self.query_items]
            }
        except Exception as e:
            self.res_data.set_status_code(my_response.Status.ERROR)
            self.log_data.res_data ={
                "error": str(e),
                "request_args": dict(request.args)
            }


if __name__ == '__main__':
    items = [str(i).zfill(11) for i in range(1, 3000, 3)]

    sql = ProductDetailAction.batch_query()

    print(sql % tuple(items))