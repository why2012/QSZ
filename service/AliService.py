# coding: utf-8
from service.BaseService import *
import json
import xml.dom.minidom as xmldom
import uuid
from util.encrypt import *
import requests
import time
from model.AliModel import AliModel
from lib.AES import AES
import random
import sys
if sys.version_info[0] < 3:
	from urllib import urlencode
	from urllib import unquote
else:
	from urllib.parse import urlencode 
	from urllib.parse import unquote 

class AliService(BaseService):
	def __init__(self, db, cursor):
		self.aliModel = AliModel(db, cursor)

	def constructPaymentObj(self, configObj, bodyDesc, subjectTitle, out_trade_no, total_amount_fee, return_url = None, notify_url = None):
		paymentObj = {}
		paymentObj["app_id"] = configObj["appid"]
		paymentObj["method"] = configObj["payment"]["method"]
		paymentObj["format"] = configObj["format"]
		if return_url is None:
			paymentObj["return_url"] = configObj["payment"]["return_url"]
		else:
			if return_url.strip().startswith("http"):
				paymentObj["return_url"] = return_url
			else:
				paymentObj["return_url"] = configObj["return_url_domain"] + return_url
		paymentObj["charset"] = configObj["charset"]
		paymentObj["sign_type"] = configObj["sign_type"]
		paymentObj["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		paymentObj["version"] = configObj["version"]
		if notify_url is None:
			paymentObj["notify_url"] = configObj["payment"]["notify_url"]
		else:
			if notify_url.strip().startswith("http"):
				paymentObj["notify_url"] = notify_url
			else:
				paymentObj["notify_url"] = configObj["notify_url_domain"] + notify_url
		# 请求参数
		biz_content_obj = {
			"body": bodyDesc, 
			"subject": subjectTitle, 
			"out_trade_no": out_trade_no, 
			"total_amount": total_amount_fee,
			"product_code": configObj["payment"]["product_code"],
		}
		biz_content_jsonstr = json.dumps(biz_content_obj, ensure_ascii = False)
		paymentObj["biz_content"] = biz_content_jsonstr
		paymentObj["sign"] = AliParamEncrypt(paymentObj, configObj["secret_key"])
		return paymentObj

	def getPaymentUrl(self, domain_url, paymentObj):
		return domain_url + "?" + urlencode(paymentObj)

	# --- 交易状态 ---
	# WAIT_BUYER_PAY	交易创建，等待买家付款
	# TRADE_CLOSED	未付款交易超时关闭，或支付完成后全额退款
	# TRADE_SUCCESS	交易支付成功
	# TRADE_FINISHED	交易结束，不可退款

	# --- 通知触发条件 ---
	# TRADE_FINISHED	交易完成	false（不触发通知）
	# TRADE_SUCCESS	支付成功	true（触发通知）
	# WAIT_BUYER_PAY	交易创建	false（不触发通知）
	# TRADE_CLOSED	交易关闭	true（触发通知）

	# doc https://docs.open.alipay.com/203/105286
	def constructNotifyObj(self, baseController):
		notifyObj = {}
		notifyObj["notify_time"] = baseController.getStrArg("notify_time") # 2015-14-27 15:45:58
		notifyObj["notify_type"] = baseController.getStrArg("notify_type") # trade_status_sync
		notifyObj["notify_id"] = baseController.getStrArg("notify_id")
		notifyObj["app_id"] = baseController.getStrArg("app_id")
		notifyObj["charset"] = baseController.getStrArg("charset")
		notifyObj["version"] = baseController.getStrArg("version")
		notifyObj["sign_type"] = baseController.getStrArg("sign_type") # RSA2 | RSA
		notifyObj["sign"] = baseController.getStrArg("sign") 
		notifyObj["trade_no"] = baseController.getStrArg("trade_no") # 支付宝交易号
		notifyObj["out_trade_no"] = baseController.getStrArg("out_trade_no") # 商户订单号
		notifyObj["out_biz_no"] = baseController.getStrArg("out_biz_no") # 非必须, 商户业务号	
		notifyObj["buyer_id"] = baseController.getStrArg("buyer_id") # 非必须, 买家支付宝用户号
		notifyObj["buyer_logon_id"] = baseController.getStrArg("buyer_logon_id") # 非必须, 买家支付宝账号
		notifyObj["seller_id"] = baseController.getStrArg("seller_id") # 非必须, 卖家支付宝用户号
		notifyObj["seller_email"] = baseController.getStrArg("seller_email") # 非必须, 卖家支付宝账号
		notifyObj["trade_status"] = baseController.getStrArg("trade_status") # 非必须, 交易状态
		notifyObj["total_amount"] = baseController.getStrArg("total_amount") # 非必须, 订单金额
		notifyObj["receipt_amount"] = baseController.getStrArg("receipt_amount") # 非必须, 实收金额
		notifyObj["invoice_amount"] = baseController.getStrArg("invoice_amount") # 非必须, 开票金额
		notifyObj["buyer_pay_amount"] = baseController.getStrArg("buyer_pay_amount") # 非必须, 付款金额
		notifyObj["refund_fee"] = baseController.getStrArg("refund_fee") # 非必须, 总退款金额
		notifyObj["subject"] = baseController.getStrArg("subject") # 非必须, 订单标题
		notifyObj["body"] = baseController.getStrArg("body") # 非必须, 商品描述
		notifyObj["gmt_create"] = baseController.getStrArg("gmt_create") # 非必须, 交易创建时间
		notifyObj["gmt_payment"] = baseController.getStrArg("gmt_payment") # 非必须, 交易付款时间 2015-04-27 15:45:57
		notifyObj["gmt_refund"] = baseController.getStrArg("gmt_refund") # 非必须, 交易退款时间 2015-04-28 15:45:57.320
		notifyObj["gmt_close"] = baseController.getStrArg("gmt_close") # 非必须, 交易结束时间
		notifyObj["fund_bill_list"] = baseController.getStrArg("fund_bill_list") # 非必须, 支付金额信息
		notifyObj["passback_params"] = baseController.getStrArg("passback_params") # 非必须, 回传参数
		notifyObj["voucher_detail_list"] = baseController.getStrArg("voucher_detail_list") # 非必须, 优惠券信息

		return notifyObj

	# 所有回调参数，用于验参
	def constructGlobalNotifyMap(self, baseController):
		notifyMap = baseController.getAllArgs()
		for key, value in notifyMap.items():
			if key not in ["sign", "sign_type"]:
				notifyMap[key] = unquote(value)
		return notifyMap

	# 验证签名
	# doc: https://docs.open.alipay.com/203/105286
	def checkNotifyObj(self, configObj, notifyMap):
		result = False;
		try:
			if notifyMap["seller_id"] != configObj["sellerid"]:
				return False
			if notifyMap["app_id"] != configObj["appid"]:
				return False 
			result = AliParamVerify(notifyMap, configObj["payment"]["public_key"])
		except e:
			import rsa
			if isinstance(e, rsa.VerificationError):
				pass
			else:
				raise e
		finally:
			return result

	# 企业向个人转账 obj
	# doc https://docs.open.alipay.com/api_28/alipay.fund.trans.toaccount.transfer
	# 配置数据， 订单号， 收款用户账户类型[ALIPAY_USERID-用户id， 2088开头； ALIPAY_LOGONID：用户支付宝登录号，邮箱或手机号]
	# 用户id，转账金额
	def constructTransferObj(self, configObj, out_biz_no, payee_type, payee_account, amount, remark = ""):
		transferObj = {}
		transferObj["app_id"] = configObj["appid"]
		transferObj["method"] = configObj["transfer"]["method"]
		transferObj["charset"] = configObj["transfer"]["charset"]
		transferObj["sign_type"] = configObj["transfer"]["sign_type"]
		transferObj["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		transferObj["version"] = configObj["transfer"]["version"]
		biz_content_obj = {}
		biz_content_obj["out_biz_no"] = out_biz_no
		biz_content_obj["payee_type"] = payee_type
		biz_content_obj["payee_account"] = payee_account
		biz_content_obj["amount"] = amount
		biz_content_obj["remark"] = remark
		transferObj["biz_content_json"] = json.dumps(biz_content_obj, ensure_ascii = False)
		transferObj["sign"] = AliParamEncrypt(transferObj, configObj["secret_key"])
		transferObj["url_domain"] = configObj["transfer"]["domain_url"]

		return transferObj

	# 企业向个人转账
	# 状态码 https://docs.open.alipay.com/common/105806
	def sendFeeTransfer(self, transferObj):
		url_domain = transferObj["url_domain"]
		del transferObj["url_domain"]
		response = requests.get(url_domain, params = transferObj)
		responseObj = response.json()
		transacObj = {}
		transacObj["sign"] = responseObj["sign"]
		transacObj["code"] = responseObj["alipay_fund_trans_toaccount_transfer_response"]["code"]
		transacObj["msg"] = responseObj["alipay_fund_trans_toaccount_transfer_response"]["msg"]
		if "out_biz_no" in responseObj["alipay_fund_trans_toaccount_transfer_response"]:
			transacObj["out_biz_no"] = responseObj["alipay_fund_trans_toaccount_transfer_response"]
		if "order_id" in responseObj["alipay_fund_trans_toaccount_transfer_response"]:
			transacObj["order_id"] = responseObj["alipay_fund_trans_toaccount_transfer_response"]["order_id"]
		if "pay_date" in responseObj["alipay_fund_trans_toaccount_transfer_response"]:
			transacObj["pay_date"] = responseObj["alipay_fund_trans_toaccount_transfer_response"]["pay_date"]
		if "sub_code" in responseObj["alipay_fund_trans_toaccount_transfer_response"]:
			transacObj["sub_code"] = responseObj["alipay_fund_trans_toaccount_transfer_response"]["sub_code"]
		if "sub_msg" in responseObj["alipay_fund_trans_toaccount_transfer_response"]:
			transacObj["sub_msg"] = responseObj["alipay_fund_trans_toaccount_transfer_response"]["sub_msg"]
		if transacObj["code"] != "10000":
			transacObj["result"] = False
		else:
			transacObj["result"] = True
		return transacObj

	# 引导用户授权urlobj
	# doc https://docs.open.alipay.com/289/105656
	def constructUserAuthObj(self, configObj, redirect_uri = None, userId = -1):
		authObj = {}
		authObj["app_id"] = configObj["appid"]
		authObj["scope"] = configObj["usercode"]["scope"]
		if redirect_uri is None:
			authObj["redirect_uri"] = configObj["usercode"]["redirect_uri"]
		elif not redirect_uri.startswith("http"):
			authObj["redirect_uri"] = configObj["usercode"]["redirect_uri_domain"] + redirect_uri
		else:
			authObj["redirect_uri"] = redirect_uri
		aes = AES(AES_KEY)
		authObj["state"] = aes.encrypt("%s|%s" % (str(random.random() * 10000000), userId))
		authObj["domain_url"] = configObj["usercode"]["domain_url"]

		return authObj

	# 引导用户授权url, 获取auth_code
	def getUserAuthUrl(self, authObj):
		url_domain = authObj["domain_url"]
		return url_domain + "?" + urlencode(authObj)

	# https://docs.open.alipay.com/common/105193
	def getAppAuthToken(self):
		app_auth_token, is_expired, refresh_token, re_expire_in = self.aliModel.getAppToken()
		if app_auth_token == 0:
			app_auth_token = self.getAppAuthToken()
		elif is_expired:
			app_auth_token = self.refreshAppAuthToken(refresh_token)
		return app_auth_token

	def refreshAppAuthToken(self, refresh_token):
		response = requests.get("alipay.open.auth.token.app", {"grant_type": "refresh_token", "refresh_token": refresh_token})
		responseObj = response.json()
		authObj = {}
		authObj["app_auth_token"] = responseObj["alipay_open_auth_token_app_response"]["app_auth_token"]
		authObj["app_refresh_token"] = responseObj["alipay_open_auth_token_app_response"]["app_refresh_token"]
		authObj["expires_in"] = responseObj["alipay_open_auth_token_app_response"]["expires_in"]
		authObj["re_expires_in"] = responseObj["alipay_open_auth_token_app_response"]["re_expires_in"]
		authObj["code"] = responseObj["alipay_open_auth_token_app_response"]["code"]
		authObj["msg"] = responseObj["alipay_open_auth_token_app_response"]["msg"]

		self.aliModel.insertAppToken(authObj["app_auth_token"], authObj["expires_in"], int(time.time()), authObj["app_refresh_token"], authObj["re_expires_in"])

		return authObj["app_auth_token"]

	# 为避免获取app_auth_code，此处直接读取配置信息
	def getAppAuthToken(self):
		return AliPayment["app_startup_auth_token"]

	# 回调，获取用户信息 obj
	# doc https://docs.open.alipay.com/289/105656
	def constructFetchUserInfoObj(self, baseController):
		notifyObj = {}
		notifyObj["app_id"] = baseController.getStrArg("app_id")
		notifyObj["scope"] = baseController.getStrArg("scope")
		notifyObj["error_scope"] = baseController.getStrArg("error_scope")
		notifyObj["state"] = baseController.getStrArg("state")
		notifyObj["auth_code"] = baseController.getStrArg("auth_code")
		notifyObj["app_auth_token"] = self.getAppAuthToken()
		return notifyObj

	# 获取用户信息, https://docs.open.alipay.com/api_9/alipay.system.oauth.token
	def fetchUserInfo(self, configObj, userInfoObj):
		url_domain = configObj["userauth"]["domain_url"]
		requestObj = {}
		requestObj["app_id"] = configObj["appid"]
		requestObj["method"] = configObj["userauth"]["method"]
		requestObj["charset"] = configObj["userauth"]["charset"]
		requestObj["sign_type"] = configObj["userauth"]["sign_type"]
		requestObj["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		requestObj["version"] = configObj["userauth"]["version"]
		requestObj["app_auth_token"] = userInfoObj["app_auth_token"]
		requestObj["grant_type"] = configObj["userauth"]["grant_type"]
		requestObj["code"] = userInfoObj["auth_code"]
		requestObj["sign"] = AliParamEncrypt(requestObj, configObj["secret_key"])
		url = url_domain + "?" + urlencode(requestObj)
		print("-----fetchUserInfo-----", url)
		response = requests.get(url, verify = False)
		responseObj = response.json()
		transacObj = {}
		if "alipay_system_oauth_token_response" not in responseObj:
			responseObj["alipay_system_oauth_token_response"] = {}
		if "user_id" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["user_id"] = responseObj["alipay_system_oauth_token_response"]["user_id"]
		if "access_token" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["access_token"] = responseObj["alipay_system_oauth_token_response"]["access_token"]
		if "expires_in" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["expires_in"] = responseObj["alipay_system_oauth_token_response"]["expires_in"]
		if "refresh_token" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["refresh_token"] = responseObj["alipay_system_oauth_token_response"]["refresh_token"]
		if "re_expires_in" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["re_expires_in"] = responseObj["alipay_system_oauth_token_response"]["re_expires_in"]
		if "code" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["code"] = responseObj["alipay_system_oauth_token_response"]["code"]
		if "msg" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["msg"] = responseObj["alipay_system_oauth_token_response"]["msg"]
		if "sub_code" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["sub_code"] = responseObj["alipay_system_oauth_token_response"]["sub_code"]
		if "sub_msg" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["sub_msg"] = responseObj["alipay_system_oauth_token_response"]["sub_msg"]
		if "error_response" in responseObj:
			transacObj["error_response"] = responseObj["error_response"]
		if "sign" in responseObj:
			transacObj["sign"] = responseObj["sign"]
		if "user_id" in responseObj["alipay_system_oauth_token_response"]:
			transacObj["result"] = True
		else:
			transacObj["result"] = False
		transacObj["state"] = userInfoObj["state"]

		return transacObj










