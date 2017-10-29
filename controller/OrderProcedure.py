# coding: utf-8
from controller.BaseController import *
import uuid
import time
import datetime

# 创建看房申请
class CreatePreOrder(BaseController):
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
class GetPreOrderPaymentUrl(BaseController):
	@checklogin()
	@queryparam("pre_order_id", "string")
	@innerhttp("PaymentController.AliPaymentUrlController", {"out_trade_no": "self.pre_order_id", "total_fee": 10, "body_desc": "pre order fee", "subject_title": "信息费"}, headers = {TOKEN_NAME: "self.token_original"})
	def execute(self):
		return self.controller_bucket["AliPaymentUrlController"].jsonobj

# 看房红包支付结果
class PreOrderPaymentResult(BaseController):
	def execute(self):
		pass

# 创建租房订单
class CreateHouseRentingOrder(BaseController):
	@checklogin()
	def execute(self):
		pass

# 确认订单信息
class OwnerConfirmRentingOrderInfo(BaseController):
	@checklogin()
	def execute(self):
		pass

# 房东确认订单
class OwnerConfirmRentingOrder(BaseController):
	@checklogin()
	def execute(self):
		pass

# 获取待支付订单信息
class GetRentingOrderPaymentInfo(BaseController):
	@checklogin()
	def execute(self):
		pass

# 获取订单支付url
class GetRentingOrderPaymentUrl(BaseController):
	@checklogin()
	def execute(self):
		pass

# 租房订单支付结果
class RentingOrderPaymentResult(BaseController):
	def execute(self):
		pass

# 投诉订单
class ComplaintAndRefund(BaseController):
	@checklogin()
	def execute(self):
		pass

# 投诉结果
class ComplaintAndRefundResult(BaseController):
	@checklogin()
	def execute(self):
		pass














