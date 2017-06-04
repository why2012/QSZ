# coding: utf-8

class ErrorStatusException(Exception):
	def __init__(self, errMsg, errCode):
		super(ErrorStatusException, self).__init__(errMsg, errCode)
		self.errMsg = errMsg
		self.errCode = errCode

	def getMsg(self):
		return self.errMsg

	def getCode(self):
		return self.errCode

class LoginException(ErrorStatusException):
	pass