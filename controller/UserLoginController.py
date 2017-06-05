# coding: utf-8
from controller.BaseController import *
from lib.AES import AES
import time

class UserLoginController(BaseController):

	@service("UserService", "userService", spec = "ABC")
	@service("UserService", "userService02", spec = "DEF")
	def execute(self):
		aes = AES(AES_KEY)
		self.setResult(aes.encrypt("%s|%s|%d" % (TOKEN_HEADER, "123", int(time.time()))), msg = "OK")
		print self.userService.findUser("111", "111")
		print self.userService02.findUser("111", "111")

	@staticmethod
	def checkParams(self):
		self.phone = self.getStrArg("phone")
		self.passwd = self.getStrArg("passwd")
