from flask import Flask
from utils.my_decorator import need_session
from utils.my_decorator import response_and_logging
from gevent import monkey
from gevent.pywsgi import WSGIServer
from user.login import *
from user.signup import SignUp
from actions.main_activity import MainInitAction
from actions.product_search import ProductSearchAction
from actions.product_detail_info import ProductDetailAction
from actions.hot_keyword import HotKeywordAction
from actions.order_operation import *
from actions.shop_car_operation import *
from utils.ResAndLogBean import ResAndLogBean
from conf import DBConf
from conf import RedisConfig
from conf import ServiceConf
from DBUtils.PooledDB import PooledDB
from redis import ConnectionPool as RedisPool


monkey.patch_all()
DB_CONNECTION_POOL = PooledDB(**DBConf.all_config)
REDIS_CONNECTION_POOL = RedisPool(**RedisConfig.ALL_ARGUMENTS)

app = Flask(__name__)


@app.route('/')
def index():
    return "抱歉!\n推荐系统主页暂时还在建设当中"


@app.route('/user/login', methods=['POST', 'GET'])
@response_and_logging
def login():
    res_and_log_bean = ResAndLogBean()
    if request.method == "GET":
        lo = LoginGet(request.args, res_and_log_bean)
        lo.login()
    else:
        with LoginPost(DB_CONNECTION_POOL, request.form, res_and_log_bean) as lo:
            lo.login()
    return res_and_log_bean


@app.route('/user/signup', methods=["POST"])
@response_and_logging
def signup():
    res_and_log_bean = ResAndLogBean()
    with SignUp(DB_CONNECTION_POOL, request.form, res_and_log_bean) as su:
        su.signup()
    return res_and_log_bean


@app.route('/product/get_main_items.action', methods=['GET'])
@need_session
@response_and_logging
def main_activity():
    with MainInitAction(DB_CONNECTION_POOL) as m:
        m.init_recommend_product()
        return m.finished()


@app.route('/user/detail_info.action', methods=['GET'])
def user_detail_info():
    pass


@app.route('/user/update_info.action', methods=['GET'])
def user_update_info():
    pass


@app.route("/product/get_hot_keyword.action", methods=['GET'])
@need_session
@response_and_logging
def get_hot_keyword():
    with HotKeywordAction(DB_CONNECTION_POOL) as h:
        h.start_search()
        return h.finished()


@app.route("/product/detail_info.action", methods=['GET'])
@need_session
@response_and_logging
def product_detail_info():
    with ProductDetailAction(DB_CONNECTION_POOL) as p:
        p.start_task()
        return p.finished()


@app.route("/product/search/get_items.action", methods=['GET'])
@need_session
@response_and_logging
def get_search_items():
    with ProductSearchAction(DB_CONNECTION_POOL) as p:
        p.start_search()
        return p.finished()


@app.route("/product/car/add_to_car.action", methods=["POST"])
@need_session
@response_and_logging
def add_to_car():
    with AddToCarAction(DB_CONNECTION_POOL) as a:
        a.commit_action()
        return a.finished()


@app.route("/product/car/remove_items_to_car.action", methods=["GET"])
@need_session
@response_and_logging
def car_to_remove():
    with CarToRemoveAction(DB_CONNECTION_POOL) as c:
        c.commit_action()
        return c.finished()


@app.route("/product/car/get_shop_car_items.action", methods=["GET"])
@need_session
@response_and_logging
def get_item_to_car():
    with GetShopCarItemAction(DB_CONNECTION_POOL) as g:
        g.commit_action()
        return g.finished()


@app.route("/product/car/checked_car_items.action", methods=["GET"])
@need_session
@response_and_logging
def checked_car_items():
    with CheckedShopCarItemsAction(DB_CONNECTION_POOL) as c:
        c.commit_action()
        return c.finished()


@app.route("/order/pull_order_info.action", methods=["GET"])
@need_session
@response_and_logging
def get_shop_car_order_info():
    with PullOrderInfo(DB_CONNECTION_POOL, REDIS_CONNECTION_POOL) as p:
        p.commit_action()
        return p.finished()


@app.route("/order/commit_order.action", methods=["POST"])
@need_session
@response_and_logging
def commit_order():
    with CommitOrder(DB_CONNECTION_POOL, REDIS_CONNECTION_POOL) as c:
        c.commit_action()
        return c.finished()


if __name__ == '__main__':
    MyRSA.init_secret_key()
    app.config.update(ServiceConf.all_config)
    # app.run(host="localhost", port=9999, threaded=True, processes=3)
    http_server = WSGIServer((ServiceConf.BIND_ADDRESS, ServiceConf.BIND_PORT), app, log=None)
    http_server.serve_forever()
