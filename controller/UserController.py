# coding: utf-8
from controller.BaseController import *
from lib.AES import AES
import time

# TODO
# 用户信息录入
class UserInfoCreate(BaseController):
	# 称呼
	@queryparam("nickname", "string")
	# 性别 1 男， 2 女，0 未知
	@queryparam("sex", "string")
	# 用户类型, 1 房东, 2 二房东, 3 中介
	@queryparam("user_type", "string")
	# 介绍
	@queryparam("self_description", "string")
	# 头像
	@userfile("portrait", "portrait")
	@service("UserService", "userService")
	def execute(self):
		pass

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
		if self.userInfo is not None and "id" in self.userInfo:
			aes = AES(AES_KEY)
			self.userInfo["token"] = aes.encrypt("%s|%s|%d" % (TOKEN_HEADER, self.userInfo["id"], int(time.time())))
		self.setResult(self.userInfo)

# TODO
# 实名认证
class UserRealNameIdentification(BaseController):
	@checklogin()
	@queryparam("realname", "string")
	@queryparam("idcardnumber", "string")
	@userfile("portrait", "idcardportrait")
	@userfile("idcardfront", "idcardfront")
	@userfile("idcardback", "idcardback")
	def execute(self):
		self.setResult([self.realname, self.idcardnumber])
		pass
