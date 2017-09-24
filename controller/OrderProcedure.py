# coding: utf-8
from controller.BaseController import *
import uuid
import time
import datetime

# 创建看房申请
class CreatePreOrder(BaseController):
	#@checklogin()
	@innerhttp("TestController", {"A": 1, "B": [2]})
	def execute(self):
		return self.controller_bucket["TestController"].jsonobj

# 获取支付url
class GetPreOrderPaymentUrl(BaseController):
	@checklogin()
	def execute(self):
		pass

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














