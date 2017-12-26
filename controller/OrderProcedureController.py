# coding: utf-8
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from controller.BaseController import *
import uuid
import time
import datetime
import abc
import six

# 创建看房申请
class CreatePreOrderController(BaseController):
	@checklogin()
	@queryparam("owner_id", "string")
	@queryparam("house_id", "string")
	@invoke("if self.owner_id == self.userId: raise Exception('看房人与房东不能是同一人.')")
	@sql("insert ignore into pre_order_info(owner_id, renter_id, house_id, status) values(%s, %s, %s, %s)", ("self.owner_id", "self.userId", "self.house_id", "1"))
	def execute(self):
		if self.lastid == 0:
			self.lastid = self.sqlServ.SQL("select-one id from pre_order_info where owner_id=%s and renter_id=%s and house_id=%s", (self.owner_id, self.userId, self.house_id))["id"]
		return self.setResult(self.lastid, msg="OK")

# 获取看房申请支付url
class GetPreOrderPaymentUrlController(BaseController):
	@checklogin()
	@queryparam("pre_order_id", "string")
	@queryparam("return_url", "string")
	def execute(self):
		return_url = self.return_url
		notify_url = PAYMENT_GLOBAL_CONFIG["NOTIFY_MID_PATH"] + PAYMENT_GLOBAL_CONFIG["PRE_ORDER_PAYMENT"]
		innerhttp("PaymentController.AliPaymentUrlController", {"out_trade_no": str(self.pre_order_id) + "1", "total_fee": 0.01, "body_desc": "pre order fee", "subject_title": "信息费", "return_url": return_url, "notify_url": notify_url}, headers = {TOKEN_NAME: "self.token_original"})(None)(self)
		return self.controller_bucket["AliPaymentUrlController"].jsonobj

@six.add_metaclass(abc.ABCMeta)
class BaseProcessor(object):
	def __init__(self, db):
		self.db = db
		self.cursor = self.db.cursor()

	@abc.abstractmethod
	def process(self):
		"""
		"""

class PreOrderProcessor(BaseProcessor):
	def __init__(self, pre_order_id, db):
		super(PreOrderProcessor, self).__init__(db)
		self.pre_order_id = int(pre_order_id)

	@sql("update pre_order_info set status=2 where id=%s", ("self.pre_order_id",))
	def process(self):
		return True

# 看房红包支付结果
class PreOrderPaymentResultController(BaseController):
	def execute(self):
		pass

# 创建租房订单
class CreateHouseRentingOrderController(BaseController):
	@checklogin()
	def execute(self):
		pass

# 确认订单信息
class OwnerConfirmRentingOrderInfoController(BaseController):
	@checklogin()
	def execute(self):
		pass

# 房东确认订单
class OwnerConfirmRentingOrderController(BaseController):
	@checklogin()
	def execute(self):
		pass

# 获取待支付订单信息
class GetRentingOrderPaymentInfoController(BaseController):
	@checklogin()
	def execute(self):
		pass

# 获取订单支付url
class GetRentingOrderPaymentUrlController(BaseController):
	@checklogin()
	def execute(self):
		pass

# 租房订单支付结果
class RentingOrderPaymentResultController(BaseController):
	def execute(self):
		pass

# 投诉订单
class ComplaintAndRefundController(BaseController):
	@checklogin()
	def execute(self):
		pass

# 投诉结果
class ComplaintAndRefundResultController(BaseController):
	@checklogin()
	def execute(self):
		pass














