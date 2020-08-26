from pymysql import Connect
import pymysql
import random
import time

db = Connect(
    host="localhost",
    port=3306,
    user="root",
    password="123qweQWE",
    database="RECOMMENDATION_SYSTEM_DB",
    charset='utf8'
)
cursor = db.cursor(pymysql.cursors.DictCursor)

sql = """
                SELECT rpbi.id as product_id,
                       rpbi.name as product_name,
                       rpbi.image_url as product_image,
                       rpbi.status as product_status,
                       rpbi.price as price,
                       rpsi.comment_count as comment_count,
                       rpsi.average_score as average_score,
                       rpsi.good_count as good_count,
                       rpsi.general_count as general_count,
                       rpsi.poor_count as poor_count,
                       rpsi.good_rate as good_rate,
                       rpsi.inventory as inventory,
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

pool = [i for i in range(100000)]
items = random.choices(pool, k=1)
items = [str(i).zfill(11) for i in items]
start_time = time.time()
try:
    for i in items:
        cursor.execute(sql, i)
        for k, v in cursor.fetchall()[0].items():
            if type(v) not in (float, int, str):
                print(v, type(v))
except Exception:

    print("err")
finally:
    cursor.close()
    db.close()

print(time.time() - start_time)
