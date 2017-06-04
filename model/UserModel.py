# coding: utf-8
class UserModel(object):
	def __init__(self, db, cursor):
		self.db = db
		self.cursor = cursor

	def findOneByPhoneAndPasswd(self, phone, passwd):
		print self.db
		print self.cursor
		return [111]