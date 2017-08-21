# coding: utf-8
from controller.BaseController import *
import uuid
import time
import datetime

# 申请微信预支付交易单, 返回prepayid
class WxPrepayController(BaseController):
	@checklogin()
	@service("WxService", "wxService")
	def execute(self):
		out_trade_no = "" # 订单号
		prepayObj = wxService.constructPrepayObj(WxPayment["appid"], WxPayment["mch_id"], out_trade_no, self.remote_ip, WxPayment["wxkey"], WxPayment["notify_url"])
		# todo: 存储sign, 用于回调时安全验证
		sign = prepayObj["sign"]

		responseObj = wxService.applyPrepayInfo(prepayObj)
		prepay_code = responseObj["prepay_id"] # 预支付号
		return {result: "SUCCESS", "prepay_code": prepay_code} #

# 微信用户付款回调接口
class WxPaymentNotifyController(BaseController):
	@service("WxService", "wxService")
	def execute(self):
		notifyObj = wxService.parseResponseXml(self.post_body, notify = True)
		# todo: 取出sign, 比较sign与数据库中的值是否一致
		sign = notifyObj["sign"]

		resultXml = wxService.getNotifyResultXml(True)
		self.resultBody = resultXml

# 发送红包, 内部定时脚本接口
class WxSendRedpack(BaseController):
	@service("WxService", "wxService")
	def execute(self):
		# todo: 内部登录码验证

		mch_billno = "" # 订单号
		re_openid = "" # 用户openid
		total_amount = 0 # 金额
		redpackObj = wxService.constructRedpackObj(WxPayment["appid"], WxPayment["mch_id"], mch_billno, re_openid, WX_APPID, MCH_NAME, total_amount, self.local_ip)
		CA_PEM_PATH = ""
		AUTH_PEM_PATH = ""
		responseObj = wxService.sendRedPack(redpackObj, verify = CA_PEM_PATH, certPathList = (AUTH_PEM_PATH, ))
		return {result: "SUCCESS"}

# 支付宝请求url获取接口
class AliPaymentUrlController(BaseController):
	@checklogin()
	@service("AliService", "aliService")
	def execute(self):
		out_trade_no = "" # 订单号
		total_fee = 0 # 金额
		body_desc = "" # 描述
		subject_title = "" # 标题 
		paymentObj = self.aliService.constructPaymentObj(AliPayment, body_desc, subject_title, out_trade_no, total_fee)
		payment_url = self.aliService.getPaymentUrl(AliPayment["payment"]["domain_url"], paymentObj)
		return {result: "SUCCESS", "payment_url": payment_url} #

# 支付宝回调接口
class AliPaymentNotifyController(BaseController):
	@service("AliService", "aliService")
	def execute(self):
		notifyObj = self.aliService.constructNotifyObj(self)
		# sign 验签
		checkResult = self.aliService.checkNotifyObj(notifyObj)
		if checkResult:
			# todo: 业务处理

			self.resultBody = "success"
		else:
			self.resultBody = "[failed]sign check failed."

# todo: 支付宝，获取引导用户授权url
class AliUserInfoAuthUrl(BaseController):
	@checklogin()
	@service("AliService", "aliService")
	def execute(self):
		pass

# todo: 支付宝，获取auth token后, 获取用户信息
class AliFetchUserInfo(BaseController):
	@checklogin()
	@service("AliService", "aliService")
	def execute(self):
		pass

# todo: 支付宝，企业转账
class AliEnterpriseTransfer(BaseController):
	@checklogin()
	@service("AliService", "aliService")
	def execute(self):
		pass














