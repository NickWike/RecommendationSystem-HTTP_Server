from base.action_base import BaseAction
from flask import request


class PaymentAction(BaseAction):

    def __init__(self, db_pool):
        super().__init__(db_pool)
