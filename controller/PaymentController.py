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
class PaymentNotifyController(BaseController):
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


