# coding: utf-8
from service.BaseService import *
from model.WxModel import WxModel
import urllib2 as url
import json

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