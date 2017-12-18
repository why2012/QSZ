# coding: utf-8
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
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
	@queryparam("out_trade_no", "string")
	@queryparam("total_fee", "float")
	@queryparam("body_desc", "string")
	@queryparam("subject_title", "string")
	def execute(self):
		out_trade_no = self.out_trade_no # 订单号
		total_fee = self.total_fee # 金额
		body_desc = self.body_desc # 描述
		subject_title = self.subject_title # 标题 
		paymentObj = self.aliService.constructPaymentObj(AliPayment, body_desc, subject_title, out_trade_no, total_fee)
		payment_url = self.aliService.getPaymentUrl(AliPayment["payment"]["domain_url"], paymentObj)
		return {"result": "SUCCESS", "payment_url": payment_url} #

# 支付宝回调接口
class AliPaymentNotifyController(BaseController):
	@service("AliService", "aliService")
	def execute(self):
		notifyObj = self.aliService.constructNotifyObj(self)
		# sign 验签
		checkResult = self.aliService.checkNotifyObj(notifyObj, AliPayment)
		if checkResult:
			# todo: 业务处理

			self.resultBody = "success"
		else:
			self.resultBody = "[failed]sign check failed."

# 支付宝，获取引导用户授权url
class AliUserInfoAuthUrl(BaseController):
	@checklogin()
	@service("AliService", "aliService")
	def execute(self):
		authObj = self.aliService.constructUserAuthObj(AliPayment)
		userauth_url = self.aliService.getUserAuthUrl(authObj)
		return {result: "SUCCESS", "payment_url": userauth_url}

# 支付宝, 回调，获取auth token后, 获取用户信息
class AliFetchUserInfo(BaseController):
	@checklogin()
	@service("AliService", "aliService")
	def execute(self):
		fetchUserInfoObj = self.aliService.constructFetchUserInfoObj(self)
		userInfo = self.aliService.fetchUserInfo(AliPayment, fetchUserInfoObj)
		# todo: 业务处理
		if userInfo["result"]:
			pass
		else:
			pass

# 支付宝，企业转账
class AliEnterpriseTransfer(BaseController):
	@checklogin()
	@service("AliService", "aliService")
	def execute(self):
		out_trade_no = "" # 订单号
		payee_type = "ALIPAY_USERID" # 账户类型
		payee_account = "" # 用户支付宝账户
		amount = "" # 金额，单位元
		remark = "" # 转账备注
		transferObj = self.aliService.constructTransferObj(notifyObj, out_trade_no, payee_type, payee_account, amount, remark)
		transacObj = self.aliService.sendFeeTransfer(transferObj)
		resultObj = {"result": "FAIL"}
		if transacObj["result"]:
			# todo: 转账成功， 业务处理
			resultObj["result"] = "SUCCESS"
		else:
			# 转账失败， 业务处理， 日志记录
			pass

		return resultObj

# 开发者获取支付宝应用的auth_code和auth_token， 回调
# https://docs.open.alipay.com/common/105193
# 调用url https://openauth.alipay.com/oauth2/appToAppAuth.htm?app_id=2015101400446982&redirect_uri=http%3A%2F%2Fexample.com
class AliGetAuthCode(BaseController):
	@service("AliService", "aliService")
	def execute(self):
		import requests

		app_id = self.getStrArg("app_id")
		app_auth_code = self.getStrArg("app_auth_code")
		response = requests.get("alipay.open.auth.token.app", {"grant_type": "authorization_code", "code": app_auth_code})
		responseObj = response.json()

		authObj = {}
		authObj["app_auth_token"] = responseObj["alipay_open_auth_token_app_response"]["app_auth_token"]
		authObj["app_refresh_token"] = responseObj["alipay_open_auth_token_app_response"]["app_refresh_token"]
		authObj["expires_in"] = responseObj["alipay_open_auth_token_app_response"]["expires_in"]
		authObj["re_expires_in"] = responseObj["alipay_open_auth_token_app_response"]["re_expires_in"]
		authObj["code"] = responseObj["alipay_open_auth_token_app_response"]["code"]
		authObj["msg"] = responseObj["alipay_open_auth_token_app_response"]["msg"]

		self.aliService.aliModel.insertAppToken(authObj["app_auth_token"], authObj["expires_in"], int(time.time()), authObj["app_refresh_token"], authObj["re_expires_in"])

		return authObj















