# coding: utf-8
from controller.TestController import *
from controller.UserController import *

class UrlMapper(object):

	def __init__(self):
		self.mapper = [
			(r"/test", TestController),
			#(r"/login", UserLoginController),
			(r"/wx_fetch_userinfo", WxFetchUserInfo),
		]	

	def getMapper(self):
		return self.mapper