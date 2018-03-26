# coding: utf-8
from service.BaseService import *
from model.UserModel import UserModel

class UserService(BaseService):
	def __init__(self, db, cursor):
		self.userModel = UserModel(db, cursor)

	def findUser(self, phone, passwd):
		return self.userModel.findOneByPhoneAndPasswd(phone, passwd)

	def findUserByOpenid(self, openid):
		return self.userModel.findUserByOpenid(openid)

	def findUserByUserid(self, openid):
		return self.userModel.findUserByUserid(openid)

	def insertUserWxInfo(self, userInfo):
		return self.userModel.insertUserWxInfo(userInfo)