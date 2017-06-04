# coding: utf-8
from model.UserModel import UserModel

class UserService(object):

	def __init__(self, db, cursor, spec):
		self.spec = spec
		self.userModel = UserModel(db, cursor)

	def findUser(self, phone, passwd):
		print self.spec
		return self.userModel.findOneByPhoneAndPasswd(phone, passwd)