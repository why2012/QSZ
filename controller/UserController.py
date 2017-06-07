# coding: utf-8
from controller.BaseController import *
from lib.AES import AES
import time
import sys
reload(sys).setdefaultencoding("utf-8")

class UserLoginController(BaseController):
	@service("UserService", "userService", spec = "ABC")
	@service("UserService", "userService02", spec = "DEF")
	@queryparam("phone", "string")
	@queryparam("passwd", "string")
	def execute(self):
		aes = AES(AES_KEY)
		self.setResult(aes.encrypt("%s|%s|%d" % (TOKEN_HEADER, "123", int(time.time()))), msg = "OK")
		print self.userService.findUser("111", "111")
		print self.userService02.findUser("111", "111")

class WxFetchUserInfo(BaseController):
	@queryparam("openid", "string")
	@service("UserService", "userService")
	@service("WxService", "wxService")
	def execute(self):
		self.userInfo = self.userService.findUserByOpenid(self.openid)
		if self.userInfo is None:
			self.userInfo = {}
			access_token = self.wxService.getAccessToken()
			userInfo = self.wxService.fetchUserInfo(access_token, self.openid)
			if "errcode" not in userInfo:
				self.userService.insertUserWxInfo(userInfo)
				self.userInfo = self.userService.findUserByOpenid(self.openid)
		self.setResult(self.userInfo)

