# coding: utf-8
from conf.Config import *
from util.Exceptions import *
from util.ErrorCode import *
from lib.AES import AES
import time
import traceback

def checklogin(enbale_check = True):
	def method_process(op):
		def check(self, *args, **kwargs):
			if enbale_check:
				try:
					if TOKEN_NAME not in self.request.headers:
						warnLoginOut(self)
					token = self.request.headers[TOKEN_NAME]
					token_str = token
					aes = AES(AES_KEY)
					token = aes.decrypt(token)
					if token is not None and token.startswith(TOKEN_HEADER):
						head, userId, createTime = token.split("|")
						if int(time.time()) - int(createTime) >= TOKEN_EXPIRE:
							warnLoginOut(self)
						else:
							self.userId = userId
							self.token_original = token_str
							_fresult = op(self, *args, **kwargs)
							return _fresult
					else:
						warnLoginOut(self)
				except Exception as e:
					print traceback.format_exc()
					raise e
			else:
				_fresult = op(self, *args, **kwargs)
				return _fresult

		def warnLoginOut(self):
			raise LoginException("Login first.", STATUS_LOGIN_ERROR)	
		return check
	return 	method_process
