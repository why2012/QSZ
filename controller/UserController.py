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

	# 所在地区
	@queryparam("addressProvince", "string")
	# 所在地区
	@queryparam("addressCity", "string")
	# 生日, 格式 0000-00-00
	@queryparam("birthday", "string")
	# 星座
	@queryparam("constellations", "string")
	# 教育背景
	@queryparam("education", "string")
	# 职业
	@queryparam("occupation", "string")

	# 收款账户对应姓名
	@queryparam("account_name", "string", optional = True)
	# 收款账户账号
	@queryparam("account_number", "string", optional = True)
	# 收款账户对应身份证号
	@queryparam("account_idcardnumber", "string", optional = True)
	# 手机号
	@queryparam("tel", "string", optional = True)
	# 是否使用400短号  仅限房东
	@queryparam("virtual_tel_flag", "int", optional = True, default = -1)
	# 400短号  仅限房东
	@queryparam("virtual_tel", "string", optional = True)
	# 微信号
	@queryparam("wechat", "string", optional = True)
	# QQ号
	@queryparam("qq", "string", optional = True)

	# 头像
	@userfile("portrait", "portrait")
	@sql("update user_info set nickname=%s, wx_sex=%s, user_type=%s, self_description=%s, headimgurl = %s where id=%s",
		("self.nickname", "self.sex", "self.user_type", "self.self_description", "self.portrait", "self.userId"))
	@sql("update user_info set addressProvince=%s, addressCity=%s, birthday=%s, constellations=%s, education=%s, occupation=%s where id=%s",
		("self.addressProvince", "self.addressCity", "self.birthday", "self.constellations", "self.education", "self.occupation", "self.userId"))
	def execute(self):
		sqlStringPayment = "insert into user_payment("
		sqlStringPaymentValues = " values("
		sqlStringPaymentDuplicate = " ON DUPLICATE KEY UPDATE "
		paramsPaymentList = []
		paymentAllNone = True

		sqlString = "update user_info set"
		paramsList = []
		allNone = True

		if self.account_name != "":
			sqlStringPayment += " account_name,"
			sqlStringPaymentValues += "%s,"
			sqlStringPaymentDuplicate += " account_name=%s,"
			paramsPaymentList.append(self.account_name)
			paymentAllNone = False
		if self.account_number != "":
			sqlStringPayment += " account,"
			sqlStringPaymentValues += "%s,"
			sqlStringPaymentDuplicate += " account=%s,"
			paramsPaymentList.append(self.account_number)
			paymentAllNone = False
		if self.account_idcardnumber != "":
			sqlStringPayment += " account_idcardnumber,"
			sqlStringPaymentValues += "%s,"
			sqlStringPaymentDuplicate += " account_idcardnumber=%s,"
			paramsPaymentList.append(self.account_idcardnumber)
			paymentAllNone = False

		sqlStringPayment += " type,"
		sqlStringPaymentValues += "%s,"
		sqlStringPaymentDuplicate += " type=%s,"
		paramsPaymentList.append(3)

		sqlStringPayment += " user_id,"
		sqlStringPaymentValues += "%s,"
		sqlStringPaymentDuplicate += " user_id=%s,"
		paramsPaymentList.append(self.userId)

		if sqlStringPayment.endswith(","):
			sqlStringPayment = sqlStringPayment[:-1]
		if sqlStringPaymentValues.endswith(","):
			sqlStringPaymentValues = sqlStringPaymentValues[:-1]
		if sqlStringPaymentDuplicate.endswith(","):
			sqlStringPaymentDuplicate = sqlStringPaymentDuplicate[:-1]
		sqlStringPayment += ")"
		sqlStringPaymentValues += ")"
		sqlStringPayment += sqlStringPaymentValues
		sqlStringPayment += sqlStringPaymentDuplicate
		paramsPaymentList.extend(paramsPaymentList)

		if self.tel != "":
			sqlString += " tel=%s ,"
			paramsList.append(self.tel)
			allNone = False
		if self.virtual_tel_flag != -1:
			sqlString += " virtual_tel_flag=%s ,"
			paramsList.append(self.virtual_tel_flag)
			allNone = False
		if self.virtual_tel != -1:
			sqlString += " virtual_tel=%s ,"
			paramsList.append(self.virtual_tel)
			allNone = False
		if self.wechat != "":
			sqlString += " wechat=%s ,"
			paramsList.append(self.wechat)
			allNone = False
		if self.qq != "":
			sqlString += " qq=%s ,"
			paramsList.append(self.qq)
			allNone = False
		if sqlString.endswith(","):
			sqlString = sqlString[:-1]
		sqlString += " where id=%s" % self.userId

		if not allNone:
			self.sqlServ.SQL(sqlString, paramsList)
		if not paymentAllNone:
			self.sqlServ.SQL(sqlStringPayment, paramsPaymentList)
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













