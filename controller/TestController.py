# coding: utf-8
from controller.BaseController import *

class TestController(BaseController):
	@check_login()
	def execute(self):
		self.setResult(self.userId)

	@staticmethod
	def checkParams(self):
		pass
