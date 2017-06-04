# coding: utf-8
from controller.BaseController import *
from lib.AES import AES
import time

class UserLoginController(BaseController):

	@service("UserService", "userService", spec = "ABC")
	def execute(self):
		aes = AES(AES_KEY)
		self.setResult(aes.encrypt("%s|%s|%d" % (TOKEN_HEADER, "123", int(time.time()))))
		print self.userService.findUser("111", "111")

	@staticmethod
	def checkParams(self):
		self.phone = self.getStrArg("phone")
		self.passwd = self.getStrArg("passwd")
