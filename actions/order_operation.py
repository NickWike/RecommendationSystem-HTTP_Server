from base.action_base import BaseAction
from utils.TypeTransform import format_line
from utils.my_response import Status
from pymysql.cursors import DictCursor
from redis import Redis as RedisConnection
from utils.secret_key_util import MyMD5
from flask import request
import json
import time


class PullOrderInfo(BaseAction):
    def __init__(self, db_pool, redis_pool):
        super().__init__(db_pool)
        self.db_cursor = self.db.cursor(DictCursor)
        self.redis_connect = RedisConnection(connection_pool=redis_pool)
        self.request_data = dict(request.args)

    def commit_action(self):
        try:
            # 从什么地方获取的订单  0-购物车 1-立即购买
            if self.request_data.get("product_id") is None:
                order_from = 0
                order_info = self.__get_order_info_to_shop_car()

            else:
                order_from = 1
                order_info = self.__get_order_info_to_product()

            order_info["shipping_info"] = self.__get_default_shipping()

            if len(order_info["items"]) != 0:
                token = self.__create_token(order_info, order_from)
                order_info["token"] = token

            self.res_data.set_status_code(Status.OK)
            self.res_data.set_data(order_info)
            self.log_data.res_data = {
                "user_id": self.user_id,
                "items": [item["product_id"] for item in order_info["items"]],
                "order_from": order_from
            }
        except Exception as e:
            self.res_data.set_status_code(Status.ERROR)
            self.error_occurred()
            self.log_data.res_data = {
                "user_if": self.user_id,
                "error": str(e),
                "request_args": self.request_data
            }

    def __get_order_info_to_product(self):
        sql = """
            SELECT
                rpbi.id AS product_id,
                rpbi.name AS product_name,
                rpbi.price AS unit_price,
                rpbi.image_url AS product_image,
                rpbi.postage AS postage,
                rsi.name AS shop_name,
                rai.name AS area_name
            FROM 
                rs_product_base_info AS rpbi,
                rs_shop_info AS rsi,
                rs_area_info AS rai
            WHERE
                rpbi.shop_id = rsi.id AND
                rsi.area_code = rai.area_code AND
                rpbi.id = %s
        """
        product_id = self.request_data.get("product_id")
        quantity = self.request_data.get("quantity")

        assert product_id is not None and quantity is not None, "The submitted data lacks the necessary arguments"

        assert product_id.isdigit(), "The incoming data format is incorrect (argument: product_id)"

        assert quantity.isdigit(), "The incoming data format is incorrect (argument: quantity)"

        quantity = int(quantity)

        cnt = self.db_cursor.execute(sql, product_id) or 1

        if cnt == 0:
            return {"items": [], "total_price": 0.00}
        query_data = list(self.db_cursor.fetchall())
        total_price = 0.00
        for item in query_data:
            subtotal_fee = float(item["unit_price"]) * quantity + float(item["postage"])
            item["subtotal_fee"] = "%.2f" % subtotal_fee
            total_price += subtotal_fee
            item["quantity"] = quantity

        query_data = [format_line(line) for line in query_data]

        return {"items": query_data, "total_price": "%.2f" % total_price}

    def __get_order_info_to_shop_car(self):
        sql = """
            SELECT
                rpbi.id AS product_id,
                rpbi.name AS product_name,
                rpbi.price AS unit_price,
                rpbi.image_url AS product_image,
                rpbi.postage AS postage,
                rsi.name AS shop_name,
                rsci.quantity AS quantity,
                rai.name AS area_name
            FROM 
                rs_product_base_info AS rpbi,
                rs_shop_info AS rsi,
                rs_area_info AS rai,
                rs_shop_car_info AS rsci
            WHERE
                rsci.user_id = %s AND
                rpbi.shop_id = rsi.id AND
                rsi.area_code = rai.area_code AND
                rpbi.id = rsci.product_id AND
                rsci.checked = 1
        """
        cnt = self.db_cursor.execute(sql, self.user_id)
        if cnt == 0:
            return {"items": [], "total_price": 0.00}

        query_data = list(self.db_cursor.fetchall())
        total_price = 0.00

        for item in query_data:
            subtotal_fee = float(item["unit_price"]) * int(item["quantity"]) + float(item["postage"])
            item["subtotal_fee"] = "%.2f" % subtotal_fee
            total_price += subtotal_fee

        query_data = [format_line(line) for line in query_data]

        return {"items": query_data, "total_price": "%.2f" % total_price}

    def __get_default_shipping(self):
        sql = """
            SELECT
                id AS shipping_id,
                receiver_name,
                receiver_mobile,
                receiver_province,
                receiver_city,
                receiver_district,
                receiver_address
            FROM
                rs_shipping_info
            WHERE
                user_id = %s AND
                is_default = 1
            LIMIT 1
        """
        cnt = self.db_cursor.execute(sql, self.user_id)
        if cnt != 0:
            return self.db_cursor.fetchall()[0]
        return {}

    def __create_token(self, order_info, order_from):
        order_info["order_from"] = order_from
        seeds = self.user_id
        seeds += str(int(time.time() * 1000))
        token = MyMD5.change_to_md5(seeds)[1]
        self.redis_connect.set(name="rs:order:info:token:"+token, value=json.dumps(order_info), ex=60*60*24)
        return token

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis_connect.close()
        super().__exit__(exc_type, exc_val, exc_tb)


class CommitOrder(BaseAction):

    def __init__(self, db_pool, redis_pool):
        super().__init__(db_pool)
        self.db_cursor = self.db.cursor(DictCursor)
        self.redis_connect = RedisConnection(connection_pool=redis_pool)
        self.request_data = dict(request.form)

    def commit_action(self):
        try:
            commit_info = self.__create_order()
            self.res_data.set_status_code(Status.OK)
            self.res_data.set_data(commit_info)
            self.log_data.res_data = {
                "user_id": self.user_id,
                "items": [item for item in json.loads(self.request_data.get("payment_type")).keys()]
            }
        except Exception as e:
            self.res_data.set_status_code(Status.ERROR)
            self.error_occurred()
            self.log_data.res_data = {
                "user_id": self.user_id,
                "error": str(e),
                "request_args": self.request_data
            }

    def __create_order(self):
        sql = """
            INSERT INTO
                rs_order_base_info(
                    order_no,
                    user_id,
                    shipping_id,
                    payment,
                    payment_type,
                    postage,
                    status,
                    create_time,
                    update_time
                )
            VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
        """
        payment_types = self.request_data.get("payment_type")

        assert payment_types is not None, "The submitted data lacks the necessary arguments"

        payment_types = json.loads(payment_types)

        order_info = self.__get_order_info()

        assert order_info is not None, "The order information query is empty"

        order_list = []

        shipping_id = order_info.get("shipping_info").get("shipping_id")

        order_from = order_info["order_from"]

        insert_to_order_base_data = []
        insert_to_order_items_data = []
        shop_car_need_remove_items = []

        for item in order_info["items"]:
            product_id = str(item.get("product_id"))

            payment_type = payment_types.get(product_id) or '1'
            payment_type = payment_type if str(payment_type) in ('1', '2') else '1'

            date_seed = time.strftime("%Y%m%d")
            date_order_count = self.redis_connect.incr("rs:order:%s:count" % date_seed, amount=1)
            order_no = date_seed + str(date_order_count).zfill(11)

            order_list.append(order_no)

            shop_car_need_remove_items.append((self.user_id, product_id))

            insert_to_order_items_data.append((self.user_id,
                                               order_no,
                                               item["product_id"],
                                               item["product_name"],
                                               item["product_image"],
                                               item["unit_price"],
                                               item["quantity"],
                                               "%.2f" % (float(item["unit_price"]) * int(item["quantity"]))))

            insert_to_order_base_data.append((order_no,
                                              self.user_id,
                                              shipping_id,
                                              item["subtotal_fee"],
                                              payment_type,
                                              item["postage"],
                                              1))

        self.__insert_to_items_table(insert_to_order_items_data)

        self.db_cursor.executemany(sql, insert_to_order_base_data)
        if order_from == 0:
            self.remove_shop_car_item(shop_car_need_remove_items)
        token = MyMD5.change_to_md5("".join(order_list))[1]

        self.redis_connect.set("rs:order:commit:token:"+token, json.dumps({"order_list": order_list}), ex=60*15)

        return {"token": token, "payment": order_info["total_price"]}

    def remove_shop_car_item(self, data):
        sql = """
            DELETE
            FROM
                rs_shop_car_info
            WHERE
                user_id = %s AND
                product_id = %s
        """
        self.db_cursor.executemany(sql, data)

    def __insert_to_items_table(self, data):
        sql = """
            INSERT INTO
                rs_order_items_info(
                    user_id,
                    order_no,
                    product_id,
                    product_name,
                    product_image,
                    product_unit_price,
                    quantity,
                    total_price,
                    create_time,
                    update_time)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
        """
        self.db_cursor.executemany(sql, data)

    def __get_order_info(self):
        token = self.request_data.get("token")
        assert token is not None, "The submitted data lacks the necessary arguments"

        order_info = self.redis_connect.get("rs:order:info:token:"+token)

        if order_info is not None:
            order_info = json.loads(order_info)
            self.redis_connect.delete("rs:order:info:token:"+token)

        return order_info

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis_connect.close()
        super().__exit__(exc_type, exc_val, exc_tb)


"""
INSERT INTO rs_shipping_info(
    user_id,
    receiver_name,
    receiver_mobile,
    receiver_province,
    receiver_city,
    receiver_district,
    receiver_address,
    receiver_zip,
    is_default,
    create_time,
    update_time
)
VALUES(
    1,'胡图图',13100000000,NULL,'重庆','渝中区','番斗花园','60096',1,NOW(),NOW()
)

"""