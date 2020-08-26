from base.action_base import BaseAction
from pymysql.cursors import DictCursor
from flask import request
from utils import my_response
from utils import TypeTransform


class AddToCarAction(BaseAction):

    def __init__(self, db_pool):
        super().__init__(db_pool)
        self.db_cursor = self.db.cursor(DictCursor)
        self.request_data = dict(request.form)

    def commit_action(self):
        try:
            self.__commit_add_car()
            self.res_data.set_status_code(my_response.Status.OK)
            self.log_data.res_data = {
                "user_id": self.user_id,
                "product_id": self.request_data.get("product_id"),
                "checked": self.request_data.get("checked"),
                "quantity": self.request_data.get("quantity")
            }
        except Exception as e:
            self.res_data.set_status_code(my_response.Status.ERROR)
            self.log_data.res_data = {
                "error": str(e),
                "user_id": self.user_id,
                "request_args": self.request_data
            }

    def __car_is_have(self, product_id):
        sql = """
            SELECT
                id AS car_item_id,
                quantity
            FROM 
                rs_shop_car_info
            WHERE
                product_id = %s
        """
        car_item_id = -1
        quantity = 0

        cnt = self.db_cursor.execute(sql, product_id)
        if cnt:
            query_dict = self.db_cursor.fetchall()[0]
            car_item_id = query_dict.get("car_item_id")
            quantity = query_dict.get("quantity")

        return car_item_id, quantity

    def __commit_add_car(self):
        insert_sql = """
            INSERT INTO
                rs_shop_car_info (
                    user_id,
                    product_id,
                    quantity,
                    checked,
                    create_time,
                    update_time
                )
            VALUES(
                %s,%s,%s,%s,NOW(),NOW()
            )
        """
        update_sql = """
            UPDATE
                rs_shop_car_info
            SET
                quantity = %s,
                update_time = NOW()
            WHERE
                id = %s
        """
        product_id = self.request_data.get("product_id")
        user_id = self.user_id
        quantity = int(self.request_data.get("quantity"))

        checked = self.request_data.get("checked")

        assert product_id and user_id and quantity and checked, "The submitted data lacks the necessary arguments"

        assert checked in ("0", "1"), "Checked must be 0 or 1"

        car_item_id, original_quantity = self.__car_is_have(product_id)
        if car_item_id > 0:
            quantity += original_quantity
            assert quantity >= 0, "It can't be reduced"
            self.db_cursor.execute(update_sql, [quantity, car_item_id])
        else:
            assert quantity >= 0, "It can't be reduced"
            self.db_cursor.execute(insert_sql, [user_id, product_id, quantity, checked])


class CarToRemoveAction(BaseAction):

    def __init__(self, db_pool):
        super().__init__(db_pool)
        self.request_data = dict(request.args)

    def commit_action(self):
        try:
            self.__commit_remove()
            self.res_data.set_status_code(my_response.Status.OK)
            self.log_data.res_data = {
                "user_id": self.user_id,
                "items": self.request_data.get("items")
            }
        except Exception as e:
            self.res_data.set_status_code(my_response.Status.ERROR)
            self.log_data.res_data = {
                "error": str(e),
                "items": self.request_data.get("items")
            }

    def __commit_remove(self):
        remove_sql = """
            DELETE 
            FROM
                rs_shop_car_info
            WHERE
                product_id = %s AND         
                user_id = %s
        """
        product_id_str = self.request_data.get("items")

        assert product_id_str is not None, "The submitted data lacks the necessary arguments"

        product_id_list = product_id_str.split(";")

        for product_id in product_id_list:
            self.db_cursor.execute(remove_sql, [product_id, self.user_id])


class GetShopCarItemAction(BaseAction):

    def __init__(self, db_pool):
        super().__init__(db_pool)
        self.db_cursor = self.db.cursor(DictCursor)

    def commit_action(self):
        try:
            res_data = self.__commit_query()
            self.res_data.set_status_code(my_response.Status.OK)
            self.res_data.set_data(res_data)
            self.log_data.res_data = {
                "user_id": self.user_id
            }
        except Exception as e:
            self.res_data.set_status_code(my_response.Status.ERROR)
            self.res_data.set_data({"items": [], "total_price": "0.00"})
            self.log_data.res_data = {
                "error": str(e),
                "user_id": self.user_id,
            }

    def __commit_query(self):
        sql = """
            SELECT
                rpbi.id AS product_id,
                rpbi.price as unit_price,
                rpbi.name as product_name,
                rpbi.image_url AS product_image,
                rsci.quantity,
                rsci.checked,
                rsi.name AS shop_name
                
            FROM
                rs_shop_car_info AS rsci,
                rs_product_base_info AS rpbi,
                rs_shop_info AS rsi
            WHERE
                rsci.product_id = rpbi.id AND
                rpbi.shop_id = rsi.id AND
                rsci.user_id = %s
        """

        query_list = []
        total_price = 0

        if self.db_cursor.execute(sql, self.user_id) != 0:
            query_list = [TypeTransform.format_line(item) for item in self.db_cursor.fetchall()]
            for item in query_list:
                unit_price = float(item.get("unit_price"))
                quantity = int(item.get("quantity"))
                item_price = round(unit_price * quantity, 2)
                item["item_price"] = "%.2f" % item_price
                if item.get("checked"):
                    total_price += item_price
        return {"items": query_list, "total_price": "%.2f" % total_price}


class CheckedShopCarItemsAction(BaseAction):

    def __init__(self, db_pool):
        super().__init__(db_pool)
        self.request_data = dict(request.args)

    def commit_action(self):
        try:
            self.__commit_update()
            self.res_data.set_status_code(my_response.Status.OK)
            self.log_data.res_data = {
                "user_id": self.user_id,
                "items": self.request_data.get("items").split(";"),
                "checked": self.request_data.get("checked")
            }
        except Exception as e:
            self.res_data.set_status_code(my_response.Status.ERROR)
            self.log_data.res_data = {
                "error": str(e),
                "user_id": self.user_id,
                "request_args": self.request_data
            }

    def __commit_update(self):
        sql = """
            UPDATE
                rs_shop_car_info
            SET
                checked = %s
            WHERE
                user_id = %s AND
                product_id = %s
        """

        checked = self.request_data.get("checked")
        product_items_str = self.request_data.get("items")

        assert checked is not None and product_items_str is not None, "The submitted data lacks the necessary arguments"

        assert checked in ("0", "1"), "The incoming data format is incorrect (argument: checked)"

        product_items = product_items_str.split(";")
        for item in product_items:
            self.db_cursor.execute(sql, [checked, self.user_id, item])
