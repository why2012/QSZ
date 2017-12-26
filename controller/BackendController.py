# coding: utf-8
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from controller.BaseController import *
from util.encrypt import *
from model.AliModel import AliModel
import requests
import time
import sys
if sys.version_info[0] < 3:
	from urllib import urlencode
	from urllib import unquote
else:
	from urllib.parse import urlencode 
	from urllib.parse import unquote 

# 获取商户授权auth code
class MerchantAuthGrantGetAuthCodeUrlController(BaseController):
	def execute(self):
		params = {
			"app_id": AliPayment["appid"],
			"redirect_uri": AliPayment["backend_return_url_domain"] + "/payment/ali/auth_notify?op=" + PAYMENT_GLOBAL_CONFIG["APP_AUTH_NOTIFY"],
		}
		print(params)
		return "https://openauth.alipay.com/oauth2/appToAppAuth.htm" + "?" + urlencode(params)

# auth code 回调
class MerchantAuthGrantReturnAuthCodeUrlController(BaseController):
	def execute(self):
		app_auth_code = self.getStrArg("app_auth_code")
		app_id = self.getStrArg("app_id")
		if app_id != AliPayment["appid"]:
			self.resultBody = "app_id check failed." + app_id
			return
		if app_auth_code == "":
			self.resultBody = "app_auth_code check failed." + app_auth_code
			return
		url = "https://openapi.alipay.com/gateway.do?"
		paramObj = {
			"app_id": AliPayment["appid"],
			"method": "alipay.open.auth.token.app",
			"format": AliPayment["format"],
			"charset": AliPayment["charset"],
			"sign_type": AliPayment["sign_type"],
			"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
			"version": AliPayment["version"],
			"biz_content": '{"grant_type":"authorization_code","code":"%s"}' % (app_auth_code, )
		}
		paramObj["sign"] = AliParamEncrypt(paramObj, AliPayment["secret_key"])
		url += urlencode(paramObj)
		print("-----", url)
		# 目前的服务器无法直接访问这个https链接，需要设置verify=False, 有待调查解决
		response = requests.post(url, verify = False)
		content = response.json()
		print(content)
		# https://docs.open.alipay.com/common/105193
		try:
			content = content["alipay_open_auth_token_app_response"]
			if content["code"] != "10000":
				content["_msg"] = "Token refresh failed."
				return content
			app_auth_token = content["app_auth_token"]
			user_id = content["user_id"]
			auth_app_id = content["auth_app_id"]
			expires_in = content["expires_in"]
			re_expires_in = content["re_expires_in"]
			app_refresh_token = content["app_refresh_token"]
			if app_auth_token is not None and app_auth_token.strip() != "":
				aliModel = AliModel(self.db, self.cursor)
				aliModel.insertAppToken(app_auth_token, expires_in, int(time.time()), app_refresh_token, re_expires_in)
				self.resultBody = "Token refreshed. " + app_auth_token
			else:
				self.loggerError.error("Callback get app auth token failed." + response.content)
		except Exception as e:
			self.loggerError.error("Callback get app auth token failed.Error occured. " + response.content)
			self.resultBody = "Token refresh failed. " + response.content
			raise e





