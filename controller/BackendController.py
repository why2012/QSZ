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
			"redirect_uri": AliPayment["backend_return_url_domain"] + "/_merchant/get_auth_token_url",
		}
		return "https://openauth.alipay.com/oauth2/appToAppAuth.htm" + "?" + urlencode(params)

# auth code 回调
class MerchantAuthGrantReturnAuthCodeUrlController(BaseController):
	def execute(self):
		app_auth_code = self.getStrArg("app_auth_code")
		app_id = self.getStrArg("app_id")
		if app_id != AliPayment["appid"]:
			self.resultBody = "app_id check failed." + appid
			return
		url = "https://openapi.alipay.com/gateway.do?"
		paramObj = {
			"app_id": AliPayment["appid"],
			"method": alipay.open.auth.token.app,
			"format": AliPayment["format"],
			"charset": AliPayment["charset"],
			"sign_type": AliPayment["sign_type"],
			"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
			"version": AliPayment["version"],
			"biz_content": "{'merchant': 1}",
			"grant_type": "authorization_code",
			"code": app_auth_code
		}
		paramObj["sign"] = AliParamEncrypt(paramObj, AliPayment["secret_key"])
		url += urlencode(paramObj)
		print(url)
		response = requests.post(url)
		content = response.json()
		# https://docs.open.alipay.com/common/105193
		app_auth_token = content["app_auth_token"]
		user_id = content["user_id"]
		auth_app_id = content["auth_app_id"]
		expires_in = content["expires_in"]
		re_expires_in = content["re_expires_in"]
		app_refresh_token = content["app_refresh_token"]
		aliModel = AliModel(self.db, self.cursor)
		aliModel.insertAppToken(app_auth_token, expires_in, int(time.time()), app_refresh_token, re_expires_in)
		# sql("""insert into keyvalue_data(vkey, value) values(%s, %s) 
		# 		ON DUPLICATE KEY UPDATE 
		# 		set vkey=%s, value=%s
		# 	""", (ALI_APP_AUTH_TOKEN_NAME, app_auth_token, ALI_APP_AUTH_TOKEN_NAME, app_auth_token))(None)(self)
		return url





