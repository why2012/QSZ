# coding: utf-8
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from controller.BaseController import *
from lib.AES import AES
import time

# 用户信息录入
class UserInfoCreate(BaseController):
	@checklogin()
	# 称呼
	@queryparam("nickname", "string")
	# 性别 1 男， 2 女，0 未知
	@queryparam("sex", "string")
	# 用户类型, 1 房东, 2 二房东, 3 中介
	@queryparam("user_type", "string")
	# 介绍
	@queryparam("self_description", "string", optional = True)
	# 头像
	@userfile("portrait", "portrait")
	@sql("update user_info set nickname=%s, wx_sex=%s, user_type=%s, self_description=%s, wx_headimgurl = %s where id=%s",
		("self.nickname", "self.sex", "self.user_type", "self.self_description", "self.portrait", "self.userId"))
	def execute(self):
		self.setResult()

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

# 实名认证
class UserRealNameIdentification(BaseController):
	@checklogin()
	@queryparam("realname", "string")
	@queryparam("idcardnumber", "string")
	@userfile("portrait", "idcardportrait")
	@userfile("idcardfront", "idcardfront")
	@userfile("idcardback", "idcardback")
	@sql("""
		update user_info
		set real_name = %s, 
		identity_card_number = %s, 
		photo_url = %s, 
		id_card_photo_front_url = %s, 
		id_card_photo_back_url = %s,
		authentication = %s
		where id = %s
		""",
		("self.realname", "self.idcardnumber", "self.idcardportrait", "self.idcardfront", "self.idcardback", 0, "self.userId"))
	def execute(self):
		self.setResult([self.realname, self.idcardnumber])

# todo: 我的钱包
class MyWallet(BaseController):
	@checklogin()
	def execute(self):
		pass

# todo: 我的订单
class MyOrder(BaseController):
	@checklogin()
	def execute(self):
		pass













