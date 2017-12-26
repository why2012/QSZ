# coding: utf-8
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from controller.BaseController import *
from lib.AES import AES
import json
import uuid
import time
import datetime
import six
import abc

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
	@queryparam("notify_url", "string")
	@queryparam("return_url", "string")
	def execute(self):
		out_trade_no = self.out_trade_no # 订单号
		total_fee = self.total_fee # 金额
		body_desc = self.body_desc # 描述
		subject_title = self.subject_title # 标题 
		paymentObj = self.aliService.constructPaymentObj(AliPayment, body_desc, subject_title, out_trade_no, total_fee, return_url = self.return_url, notify_url = self.notify_url)
		payment_url = self.aliService.getPaymentUrl(AliPayment["payment"]["domain_url"], paymentObj)
		return {"result": "SUCCESS", "payment_url": payment_url} #

@six.add_metaclass(abc.ABCMeta)
class BaseDelegate(object):
	def __init__(self, op, db):
		self.op = op.strip()
		self.db = db

	@abc.abstractmethod
	def delegate():
		"""
		"""

class AliPaymentNotifyDelegate(BaseDelegate):
	def __init__(self, op, notifyObj, db):
		super(AliPaymentNotifyDelegate, self).__init__(op, db)
		self.notifyObj = notifyObj

	def delegate(self):
		processor = None
		if self.op == PAYMENT_GLOBAL_CONFIG["PRE_ORDER_PAYMENT"]:
			from .OrderProcedureController import PreOrderProcessor
			processor = PreOrderProcessor(self.notifyObj["out_trade_no"], self.db)

		if processor is not None:
			result_bool = processor.process()
			return result_bool

class AliPaymentNotifyFailureDelegate(BaseDelegate):
	def __init__(self, op, notifyObj, db):
		super(AliPaymentNotifyFailureDelegate, self).__init__(op, db)
		self.notifyObj = notifyObj

	def delegate(self):
		pass

# 支付宝回调接口
class AliPaymentNotifyController(BaseController):
	@service("AliService", "aliService")
	def execute(self, op):
		print("OP: " + op)
		notifyObj = self.aliService.constructNotifyObj(self)
		notifyMap = self.aliService.constructGlobalNotifyMap(self)
		print(notifyMap)
		# sign 验签
		checkResult = self.aliService.checkNotifyObj(AliPayment, notifyMap)
		# delegate
		commonDelegate = AliPaymentNotifyDelegate(op, notifyObj, self.db)
		failureDelegate = AliPaymentNotifyFailureDelegate(op, notifyObj, self.db)
		if checkResult:
			self.logger.info("alipay verify OK. | " + notifyObj["out_trade_no"] + "|" + notifyObj["total_amount"] + " | " + notifyObj["trade_no"])
			if(commonDelegate.delegate()):
				self.resultBody = "success"
			else:
				self.resultBody = "[failed]order processing error."
		else:
			self.loggerError.error("alipay verify Fail. | " + notifyObj["out_trade_no"] + " | " + notifyObj["total_amount"] + " | " + notifyObj["trade_no"])
			failureDelegate.delegate()
			self.resultBody = "[failed]sign check failed."

# 支付宝，获取引导用户授权url, 获取auth code授权
class AliUserInfoAuthUrlController(BaseController):
	@checklogin()
	@service("AliService", "aliService")
	def execute(self):
		authObj = self.aliService.constructUserAuthObj(AliPayment, "/payment/ali/auth_notify?op=" + PAYMENT_GLOBAL_CONFIG["USER_AUTH_NOTIFY"], self.userId)
		state = authObj["state"]
		sql("""
				update user_info set alipay_user_auth_state=%s where id=%s
			""", (state, "self.userId"))(None)(self)
		userauth_url = self.aliService.getUserAuthUrl(authObj)
		return {"result": "SUCCESS", "auth_url": userauth_url}

class AliPaymentUserAuthDelegate(BaseDelegate):
	def __init__(self, op, _self, db):
		super(AliPaymentUserAuthDelegate, self).__init__(op, db)
		self._self = _self

	def __process_app_auth(self, _self):
		innerhttp("BackendController.MerchantAuthGrantReturnAuthCodeUrlController")(None)(_self, _self.application, _self.request)

	# 支付宝, 回调，获取auth token后, 获取用户信息
	def __process_user_auth(self, _self):
		# get auth code in call back data
		fetchUserInfoObj = _self.aliService.constructFetchUserInfoObj(_self)
		print(fetchUserInfoObj)
		# get access token
		userInfo = _self.aliService.fetchUserInfo(AliPayment, fetchUserInfoObj)
		print("-----user-code---", userInfo)
		if userInfo["result"]:
			state = userInfo["state"]
			aes = AES(AES_KEY)
			dec_state = aes.decrypt(state)
			dec_list = dec_state.split("|")
			if len(dec_list) != 2:
				_self.loggerError.error("aliuserauth verify failed. dec_state" + dec_state)
				return
			userId = dec_list[1]
			if userId == -1:
				_self.loggerError.error("aliuserauth verify failed. userId" + userId)
				return
			sql("""
					select-one alipay_user_auth_state from user_info where id=%s
				""", (userId))(None)(_self)
			state = _self.sqlResult["alipay_user_auth_state"]
			if state == userInfo["state"]:
				ali_user_id = userInfo["user_id"]
				access_token = userInfo["access_token"]
				_self.logger.info("aliuserauth verify ok. " + ali_user_id)
				# 可以进一步调接口获取用户详细信息
				# 此处只获取ali user id
				sql("""
					update user_info set alipay_user_id=%s, alipay_user_access_token=%s where id=%s
				""", (ali_user_id, access_token, userId))(None)(_self)
				_self.resultBody = "success"
			else:
				_self.loggerError.error("aliuserauth verify failed | " + str(userInfo["result"]) + " | " + state + " | " + userInfo["state"])
		else:
			_self.loggerError.error("aliuserauth verify failed | " + str(userInfo["result"]) + " | " + json.dumps(userInfo, ensure_ascii = False))
			_self.setResult("aliuserauth verify failed", INTERNAL_ERROR, userInfo)

	def delegate(self):
		if self.op == PAYMENT_GLOBAL_CONFIG["APP_AUTH_NOTIFY"]:
			self.__process_app_auth(self._self)
		elif self.op == PAYMENT_GLOBAL_CONFIG["USER_AUTH_NOTIFY"]:
			self.__process_user_auth(self._self)
		else:
			self._self.resultBody = "Illegal Op field."

class AliPaymentUserAuthFailureDelegate(BaseDelegate):
	def __init__(self, op, _self, db):
		super(AliPaymentUserAuthFailureDelegate, self).__init__(op, db)
		self._self = _self

	def delegate(self):
		pass

# 支付宝，授权类接口回调
class AliFetchUserInfoController(BaseController):
	@service("AliService", "aliService")
	def execute(self):
		op = self.getStrArg("op")
		commonDelegate = AliPaymentUserAuthDelegate(op, self, self.db)
		failureDelegate = AliPaymentUserAuthFailureDelegate(op, self, self.db)

		commonDelegate.delegate()

# 支付宝，获取用户芝麻分
class AliFetchUserZhimaInfoController(BaseController):
	@checklogin()
	@queryparam("refresh", "string", False, "AUTO")
	@service("AliService", "aliService")
	def execute(self):
		sql("""
				select-one alipay_user_id, alipay_user_access_token, alipay_zhima_score from user_info where id=%s
			""", (self.userId))(None)(self)
		zhima_score = None
		refresh = self.refresh.strip().upper()
		if (refresh == "N" or refresh == "AUTO") and "alipay_zhima_score" in self.sqlResult and self.sqlResult["alipay_zhima_score"] is not None:
			zhima_score = self.sqlResult["alipay_zhima_score"]
			if zhima_score.isdigit() and int(zhima_score) > 0:
				self.logger.info("alizhima use cache. " + zhima_score)
				return zhima_score
		if (refresh == "Y" or refresh == "AUTO") and zhima_score is None:
			ali_user_id = self.sqlResult["alipay_user_id"]
			auth_token = self.sqlResult["alipay_user_access_token"]
			zhimaInfo = self.aliService.fetchUserZhimaInfo(AliPayment, auth_token)
			if zhimaInfo["result"]:
				zhima_score = zhimaInfo["zm_score"]
				self.logger.info("alizhima verify ok. " + zhima_score)
				sql("""
						update user_info set alipay_zhima_score=%s where id=%s
					""", (zhima_score, userId))(None)(self)
				return zhima_score
			else:
				self.loggerError.error("alizhima verify failed | " + str(zhimaInfo["result"]) + " | " + json.dumps(zhimaInfo, ensure_ascii = False))
				self.setResult(-1, INTERNAL_ERROR, zhimaInfo)
		return -1

# 支付宝，企业转账
class AliEnterpriseTransferController(BaseController):
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
class AliGetAuthCodeController(BaseController):
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















