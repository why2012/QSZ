# coding: utf-8
from conf.Config import *
from util.Exceptions import *
from util.ErrorCode import *
from lib.AES import AES
import time

def check_login(enbale_check = True):
	def method_process(op):
		def check(self, *args, **kwargs):
			if enbale_check:
				try:
					if TOKEN_NAME not in self.request.headers:
						warnLoginOut(self)
					token = self.request.headers[TOKEN_NAME]
					aes = AES(AES_KEY)
					token = aes.decrypt(token)
					if token is not None and token.startswith(TOKEN_HEADER):
						head, userId, createTime = token.split("|")
						if int(time.time()) - int(createTime) >= TOKEN_EXPIRE:
							warnLoginOut(self)
						else:
							self.userId = userId
							op(self, *args, **kwargs)
					else:
						warnLoginOut(self)
				except:
					warnLoginOut(self)
			else:
				op(self, *args, **kwargs)

		def warnLoginOut(self):
			raise LoginException("Login first.", STATUS_LOGIN_ERROR)	
		return check
	return 	method_process
