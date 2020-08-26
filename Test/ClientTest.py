import requests
import random
from utils.secret_key_util import MyRSA
import time
import gevent
from gevent import monkey
from conf import RedisConfig
import json



import threading

# monkey.patch_all()
# MyRSA.init_secret_key()
# ff = hashlib.md5("nameisdhg-=-*/".encode("utf-8"))
# st = ff.hexdigest()
# print(ff)
# print(st)
# start_time = time.time()
#
# for i in range(1000):
#     s1 = MyRsa.encryption(st)[1]
#     s2 = MyRsa.decryption(s1)
# print(time.time() - start_time)


def login_use_cookies(cookies):
    url = "http://192.168.0.105:1234/user/login"
    res = requests.get(url, cookies=cookies)
    print(res.text)


def login_user_username(username, passwd):
    url = "http://192.168.0.105:1234/user/login"
    res = requests.get(url)
    res_json = json.loads(res.text)
    pub_key = res_json.get("pub_key")
    print(pub_key)
    password = MyRSA.encryption(passwd, pub_key)[1]
    data = {"user_name": username, "password": password}
    res = requests.post(url, data=data)
    print(res.text)
    print(res.cookies.get_dict())


def signup(data):
    url = "http://192.168.0.105t:1234/user/login"
    res = requests.get(url)
    res_json = json.loads(res.text)
    pub_key = res_json.get("pub_key")
    # data["password"] = MyRSA.encryption(data["password"], pub_key)[1]
    data["password"] = "f8aS6PtS+V+Lig6Szrm9UcSECnLnT2TXk04kyVlZEtceDsMX9tJwTZKBm0zDwNLtJhsvdIr3VOXq05E8EbDqmdSEf15YBFTlQgYHaE/iGGXQqsJDPgvaZK91KPEWftSqITf9526G/84MvobvjFaYUcxtSumvBfIsJMxmTVe1Plc="
    url_signup = "http://192.168.0.105:1234/user/signup"
    res = requests.post(url_signup, data=data)
    print(res.text)


def main_activity(cookies):
    url = "http://192.168.0.105:1234/product/get_main_items.action"
    res = requests.get(url, cookies=cookies)
    res_json_data = json.loads(res.text)
    print(res_json_data)
    for item in res_json_data["items"]:
        print(item)


def search_product(cookies, data):
    url = "http://192.168.0.105:1234/product/search/get_items.action"
    res = requests.get(url, cookies=cookies, params=data)
    json_data = json.loads(res.text)
    print(json_data)
    return json_data["items"]


def get_product_detail_info(cookies, items):
    url = "http://192.168.0.105:1234/product/detail_info.action"
    res = requests.get(url, cookies=cookies, params={"items": ";".join(items)})
    print(res.text)
    print(json.loads(res.text))
    return res


def get_hot_keyword(cookies):
    url = "http://192.168.0.105:1234/product/get_hot_keyword.action"
    res = requests.get(url, cookies=cookies)
    print(res.text)
    print(json.loads(res.text))


def add_product_to_car(cookies,data):
    url = "http://192.168.0.105:1234/product/car/add_to_car.action"
    res = requests.post(url, cookies=cookies, data=data)
    print(res.text)


def remove_product_to_car(cookies, params):
    url = "http://192.168.0.105:1234//product/car/remove_items_to_car.action"
    res = requests.get(url, cookies=cookies, params=params)
    print(res.text)


def get_shop_car_items(cookies):
    url = "http://192.168.0.105:1234/product/car/get_shop_car_items.action"
    res = requests.get(url, cookies=cookies)
    print(json.loads(res.text))


def getShopCarOrderInfo(cookies, args):
    url = "http://192.168.0.105:1234/order/pull_order_info.action"
    res = requests.get(url,cookies=cookies,params=args)
    print(res.headers)
    print(json.loads(res.text))

def commitOrder(cookies,token,items):
    url = "http://192.168.0.105:1234/order/commit_order.action"
    res = requests.post(url=url, cookies=cookies, data={"token": token, "payment_type": json.dumps(items)})
    print(res.text)

ck = {'session': '.eJyrViotTi2Kz0xRslIygANDJR2IeF5ibipQpirD0MjYRKkWADesDRA.XnnEMQ.W6fkR-Iyh3Fv2R-tGBUU6WvyjCs'}


if __name__ == '__main__':
    getShopCarOrderInfo(ck, None)
    # commitOrder(ck, "336e7eda0019fd79530504ce94a8c003", {k:1 for k in [1234, 6394]})

    # get_shop_car_items(ck)

    # remove_product_to_car(ck, {"items": '00000005566'})

    # add_product_to_car(ck, data={"quantity": 1, "checked": 1, "product_id": 5656})

    # for i in range(10):
    #     get_hot_keyword(ck)


    # pool = [i for i in range(10000)]
    # # search_items = random.choices(pool, k=10)
    # search_items = [str(random.choice(pool)) for i in range(10)]
    # print(search_items)
    # get_product_detail_info(ck, ["0001"])


    # signup({"user_name": "root2", "password": "123456", "gender": "F"})
    # login_user_username("zh1234", "123456")
    # login_use_cookies(ck)
    # main_activity(ck)
    # search_product(ck, {"keyword": "年货礼盒", "page": 2, "order_by": "price", "reverse": True})
    # page = 1
    # while search_product(ck, {"keyword": "梅酒", "page": page,"order_by":"price","reverse": True}):
    #     page += 1

# headers = {"referrer": "www.log.com"}


# url_signup = "http://localhost:1234/signup"
# # res = requests.get(url)
# #
# # res_json = json.loads(res.text)
# # pub_key = res_json.get("pub_key")
# # password = MyRSA.encryption("123456", pub_key)[1]
# # r = requests.post(url, data={"user_name": "root3", "password": password, "gender": "F"})
# #
# # cookies = r.cookies.get_dict()
# # print(r.headers)
# # r_post = requests.post(url, data={"user_name": "root", "password": password}, headers=headers)
# print(json.loads(r.text))
# # print(json.loads(r.text))
# print(json.loads(requests.get(url, cookies=cookies).text))






# # res = requests.post(url,data={"username": "zh123", "password": "123456"})
# user_name = "test"
# passwd = "13s2/s*fst+"
# pub_key = requests.get(url).text
# passwd_cipher = MyRSA.encryption(passwd, pub_key)[1]
# # print(passwd_cipher)
# start_time = time.time()
#
# def t():
#     for i in range(3):
#         try:
#             res = requests.post(url, data={"username": user_name, "password": passwd_cipher})
#             return
#         except Exception as e:
#             continue
#
# async_list = [gevent.spawn(t) for i in range(1000)]
# gevent.joinall(async_list)
#
# print(time.time() - start_time)