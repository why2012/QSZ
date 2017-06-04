# coding: utf-8
from controller.BaseController import *

class TestController(BaseController):
	@checklogin()
	def execute(self):
		self.setResult(self.userId)

	@staticmethod
	def checkParams(self):
		pass
