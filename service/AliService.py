# coding: utf-8
from service.BaseService import *
import json
import xml.dom.minidom as xmldom
import uuid
from util.encrypt import *
import requests
import time

class AliService(BaseService):
	def __init__(self, db, cursor):
		pass

	def constructPaymentObj(self, configObj, bodyDesc, subjectTitle, out_trade_no, total_amount_fee):
		paymentObj = {}
		paymentObj["app_id"] = configObj["appid"]
		paymentObj["method"] = configObj["payment"]["method"]
		paymentObj["format"] = configObj["format"]
		paymentObj["return_url"] = configObj["payment"]["return_url"]
		paymentObj["charset"] = configObj["charset"]
		paymentObj["sign_type"] = configObj["sign_type"]
		paymentObj["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		paymentObj["version"] = configObj["version"]
		paymentObj["notify_url"] = configObj["payment"]["notify_url"]
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
		url_args = []
		for key, value in paymentObj:
			if type(value) != "str":
				value = str(value)
			url_args.append(key + "=" + value)
		return domain_url + "?" + "&".join(url_args)

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

	# todo: 验证签名
	# doc: https://docs.open.alipay.com/203/105286
	def checkNotifyObj(self, notifyObj):
		return True

	# todo: 企业向个人转账 obj
	# doc https://docs.open.alipay.com/api_28/alipay.fund.trans.toaccount.transfer
	def constructTransferObj(self):
		pass

	# todo: 企业向个人转账
	def sendFeeTransfer(self, transferObj):
		pass

	# todo: 引导用户授权urlobj
	# doc https://docs.open.alipay.com/289/105656
	def constructUserAuthObj(self):
		pass

	# todo: 引导用户授权url
	def getUserAuthUrl(self):
		pass

	# todo: 获取用户信息 obj
	# doc https://docs.open.alipay.com/api_2/alipay.user.userinfo.share
	def constructFetchUserInfoObj(self):
		pass

	# todo: 获取用户信息
	def fetchUserInfo(self, userInfoObj):
		pass









