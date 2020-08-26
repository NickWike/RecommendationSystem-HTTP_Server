from base.action_base import BaseAction
from utils.my_tokenizer import tokenizer
from utils import my_response
from utils import TypeTransform
from flask import request
from beans.product_card_bean import ProductCardBean


class ProductSearchAction(BaseAction):
    def __init__(self, db_pool):
        super().__init__(db_pool)

    @staticmethod
    def create_search_sql(n,
                          order_by="id",
                          page=1,
                          reverse=False
                          ) -> str:
        temp_sql = """
        SELECT id,name,image_url,price,average_score,comment_count 
        FROM rs_product_base_info AS rpbi,
             rs_product_sales_info AS rpsi
        WHERE rpbi.id = rpsi.product_id AND
             {sql_search}
        ORDER BY {order_by} {sort_method}
        LIMIT {sql_limit}
        """
        break_sql = "True = False"
        sql_search = " AND\n".join(["name LIKE %s"]*n)
        page = TypeTransform.str_to_int(page)
        reverse = TypeTransform.str_to_bool(reverse)
        page = 1 if page <= 0 else page
        order_by = order_by if order_by else 'id'

        sql_limit = (8*(page-1), 8)

        result_sql = temp_sql.format(sql_search=sql_search if sql_search else break_sql,
                                     order_by=order_by,
                                     sql_limit="%s,%s" % sql_limit,
                                     sort_method="ASC" if not reverse else "DESC")
        return result_sql

    def start_search(self):
        client_args = dict(request.args)
        try:
            word_list = tokenizer.start_cut(client_args.get("keyword"))
            word_list_pattern = list(map(lambda x: "%%%s%%" % x, word_list))
            search_sql = self.create_search_sql(n=len(word_list_pattern),
                                                page=client_args.get("page"),
                                                order_by=client_args.get("order_by"),
                                                reverse=client_args.get("reverse"))
            query_cnt = self.db_cursor.execute(search_sql, word_list_pattern)

            if query_cnt:
                rows = self.db_cursor.fetchall()
                item_list = [ProductCardBean.row_to_dict(row) for row in rows]
            else:
                item_list = []

            self.res_data.set_items(item_list)
            self.res_data.set_status_code(my_response.Status.OK)
            # self.res_data.set_message(my_response.Status.get_status_text(my_response.Status.OK))
            self.log_data.res_data = {
                "user_id": self.user_id,
                "client_args": client_args,
                "keyword_tokenizer": word_list,
                "items": [it["product_id"] for it in item_list]
            }
        except Exception as e:
            self.res_data.set_status_code(my_response.Status.ERROR)
            self.log_data.res_data = {
                "error": str(e),
                "request_args": dict(request.args)
            }


if __name__ == '__main__':
    for i in range(100):
        s = ProductSearchAction.create_search_sql(1, page=i)
        print(s)
