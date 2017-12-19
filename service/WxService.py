# coding: utf-8
from service.BaseService import *
from model.WxModel import WxModel
import sys
if sys.version_info[0] < 3:
	import urllib2 as url
else:
	import urllib.request as url
import json
import xml.dom.minidom as xmldom
import uuid
from util.encrypt import *
import requests

class WxService(BaseService):
	def __init__(self, db, cursor):
		self.wxModel = WxModel(db, cursor)

	def getAccessToken(self):
		access_token = self.wxModel.getAccessToken()
		if access_token:
			return access_token['access_token']
		return access_token

	def fetchUserInfo(self, access_token, openid):
		wx_url = WX_USER_INFO_URL.format(access_token = access_token, openid = openid)#"http://192.168.1.100:20001/test"#
		userInfo = url.urlopen(wx_url).read()
		userInfo = json.loads(userInfo)
		return userInfo

	# appid, 商户id, 商户订单号, 终端IP , 商户平台密钥key, 支付结果通知地址, 交易类型, 商品描述	
	def constructPrepayObj(self, appid, mch_id, out_trade_no, spbill_create_ip, wxkey, notify_url, trade_type = "JSAPI", body = "付款"):
		# 随机字符串, <= 32
		nonce_str = str(uuid.uuid1())[0:14] + str(uuid.uuid1())[19:]
		# 可选
		device_info = ""
		sign_type = "MD5"
		detail = "" # 商品详情
		attach = "" # 附加数据
		fee_type = "CNY" # 标价金额
		# 参数
		argsDict = {}
		argsDict["appid"] = appid
		argsDict["mch_id"] = mch_id
		argsDict["out_trade_no"] = out_trade_no
		argsDict["spbill_create_ip"] = spbill_create_ip
		argsDict["notify_url"] = notify_url
		argsDict["trade_type"] = trade_type
		argsDict["body"] = body
		argsDict["nonce_str"] = nonce_str
		argsDict["device_info"] = device_info
		argsDict["sign_type"] = sign_type
		argsDict["detail"] = detail
		argsDict["attach"] = attach
		argsDict["fee_type"] = fee_type
		# 加密
		sign = WxParamEncrypt(argsDict, wxkey = wxkey)
		argsDict["sign"] = sign
		return argsDict

	# 发送红包参数, appid, 商户id, 商户订单号, 用户openid, 公众账号appid, 商户名称, 付款金额, 红包发放总人数, 场景id, 红包祝福语, Ip地址, 活动名称, 备注
	def constructRedpackObj(self, appid, mch_id, mch_billno, re_openid, wxappid, send_name, total_amount, total_num = 1, scene_id = "PRODUCT_5", wishing = "收款", client_ip = "192.168.0.1", act_name = "", remark = ""):
		# 随机字符串, <= 32
		nonce_str = str(uuid.uuid1())[0:14] + str(uuid.uuid1())[19:]
		# 参数
		argsDict = {}
		argsDict["appid"] = appid
		argsDict["mch_id"] = mch_id
		argsDict["mch_billno"] = mch_billno
		argsDict["re_openid"] = re_openid
		argsDict["wxappid"] = wxappid
		argsDict["send_name"] = send_name
		argsDict["total_amount"] = total_amount
		argsDict["total_num"] = total_num
		argsDict["scene_id"] = scene_id
		argsDict["wishing"] = wishing
		argsDict["client_ip"] = client_ip
		argsDict["act_name"] = act_name
		argsDict["remark"] = remark
		# 加密
		sign = WxParamEncrypt(argsDict, wxkey = wxkey)
		argsDict["sign"] = sign
		return argsDict

	def constructRequestParamXml(self, prepayObj):
		xmlstrf = "<xml>{body}</xml>"
		bodyitemf = "<{tag}>{content}</{tag}>"
		xmlbody = ""
		for key, value in prepayObj.items():
			xmlbody += bodyitemf.format(tag = key, content = value)
		xmlstr = xmlstrf.format(body = xmlbody)
		return xmlstr

	def getUniqueTagValue(self, dom_ele, tagname, default = ""):
		taglist = dom_ele.getElementsByTagName(tagname)
		if taglist is None or len(taglist) == 0:
			return default
		childNodes = taglist[0].childNodes
		if childNodes is None or len(childNodes) == 0:
			return default
		data = childNodes[0].data
		if data == "" or data is None:
			return default
		return data

	# prepay接口 和 notify接口共用
	def parseResponseXml(self, xmlstr, notify = False, redpack = False):
		dom = xmldom.parseString(xmlstr).documentElement
		return_code = self.getUniqueTagValue(dom, "return_code")
		return_msg = self.getUniqueTagValue(dom, "return_msg")
		request_result = False
		payment_result = False
		if return_code == "SUCCESS":
			request_result = True
		resultDict = {}
		resultDict["return_code"] = return_code
		resultDict["return_msg"] = return_msg
		resultDict["request_result"] = request_result
		if request_result:
			resultDict["appid"] = self.getUniqueTagValue(dom, "appid")
			resultDict["mch_id"] = self.getUniqueTagValue(dom, "mch_id")
			resultDict["device_info"] = self.getUniqueTagValue(dom, "device_info")
			resultDict["nonce_str"] = self.getUniqueTagValue(dom, "nonce_str")
			resultDict["sign"] = self.getUniqueTagValue(dom, "sign")
			resultDict["result_code"] = self.getUniqueTagValue(dom, "result_code")
			if resultDict["result_code"] == "SUCCESS":
				payment_result = True
			resultDict["payment_result"] = payment_result
			resultDict["err_code"] = self.getUniqueTagValue(dom, "err_code")
			resultDict["err_code_des"] = self.getUniqueTagValue(dom, "err_code_des")
			if payment_result:
				resultDict["trade_type"] = self.getUniqueTagValue(dom, "trade_type")
				resultDict["prepay_id"] = self.getUniqueTagValue(dom, "prepay_id")
				resultDict["code_url"] = self.getUniqueTagValue(dom, "code_url")
			if notify:
				resultDict["openid"] = self.getUniqueTagValue(dom, "openid")
				resultDict["is_subscribe"] = self.getUniqueTagValue(dom, "is_subscribe")
				resultDict["trade_type"] = self.getUniqueTagValue(dom, "trade_type")
				resultDict["bank_type"] = self.getUniqueTagValue(dom, "bank_type")
				resultDict["total_fee"] = int(self.getUniqueTagValue(dom, "total_fee", 0))
				resultDict["settlement_total_fee"] = self.getUniqueTagValue(dom, "settlement_total_fee")
				resultDict["fee_type"] = self.getUniqueTagValue(dom, "fee_type")
				resultDict["cash_fee"] = int(self.getUniqueTagValue(dom, "cash_fee", 0))
				resultDict["cash_fee_type"] = self.getUniqueTagValue(dom, "cash_fee_type")
				resultDict["coupon_fee"] = int(self.getUniqueTagValue(dom, "coupon_fee", 0))
				resultDict["coupon_count"] = int(self.getUniqueTagValue(dom, "coupon_count", 0))
				if resultDict["coupon_count"] > 0:
					resultDict["coupon_data"] = []
					for i in range(esultDict["coupon_count"]):
						i_str = str(i)
						couponData = {}
						couponData["coupon_type"] = self.getUniqueTagValue(dom, "coupon_type_" + i_str)
						couponData["coupon_id"] = self.getUniqueTagValue(dom, "coupon_id_" + i_str)
						couponData["coupon_fee"] = int(self.getUniqueTagValue(dom, "coupon_fee_" + i_str))
						resultDict["coupon_data"].append(couponData)
				resultDict["transaction_id"] = self.getUniqueTagValue(dom, "transaction_id")
				resultDict["out_trade_no"] = self.getUniqueTagValue(dom, "out_trade_no")
				resultDict["attach"] = self.getUniqueTagValue(dom, "attach")
				resultDict["time_end"] = self.getUniqueTagValue(dom, "time_end")
			if redpack and payment_result:
				resultDict["mch_billno"] = self.getUniqueTagValue(dom, "mch_billno")
				resultDict["mch_id"] = self.getUniqueTagValue(dom, "mch_id")
				resultDict["wxappid"] = self.getUniqueTagValue(dom, "wxappid")
				resultDict["re_openid"] = self.getUniqueTagValue(dom, "re_openid")
				resultDict["total_amount"] = self.getUniqueTagValue(dom, "total_amount")
				resultDict["send_listid"] = self.getUniqueTagValue(dom, "send_listid")
		return resultDict

	def getNotifyResultXml(self, status = False, msg = ""):
		xmlObj = {}
		if status:
			xmlObj["return_code"] = "SUCCESS"
		else:
			xmlObj["return_code"] = "FAIL"
		xmlObj["return_msg"] = msg
		return self.constructRequestParamXml(xmlObj)

	def applyPrepayInfo(self, prepayObj):
		requestXml = self.constructRequestParamXml(prepayObj)
		response = requests.post(WX_PAY_UNIFIEDORDER, data = requestXml)
		return self.parseResponseXml(response.content)

	# 若需要进行https安全验证则 verify=网站CA证书位置，若需要进行client身份认证，则服务器上需要放置证书 certPathList=[证书位置]
	# 分别对应微信 CA证书(rootca.pem) 和 pkcs12格式证书(apiclient_cert.p12)
	def sendRedPack(self, redpackObj, verify = False, certPathList = []):
		requestXml = self.constructRequestParamXml(redpackObj)
		response = requests.post(WX_SEND_REDPACK, data = requestXml, verify = verify, cert = certPathList)
		return self.parseResponseXml(response.content, redpack = True)


















