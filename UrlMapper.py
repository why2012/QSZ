# coding: utf-8
from controller.UserLoginController import UserLoginController
from controller.TestController import TestController

class UrlMapper(object):

	def __init__(self):
		self.mapper = [
			(r"/login", UserLoginController),
			(r"/test", TestController)
		]	

	def getMapper(self):
		return self.mapper