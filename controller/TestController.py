# coding: utf-8
from controller.BaseController import *

class TestController(BaseController):
	#@checklogin()
	def execute(self):
		# self.setResult(self.userId)
		wxUserInfo = {
			"subscribe": 1, "openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M", "nickname": "Band", "sex": 1, "language": "zh_CN", 
			"city": "广州", "province": "广东", "country": "中国", 
			"headimgurl":  "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
			"subscribe_time": 1382694957, "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL", "remark": "", "groupid": 0, "tagid_list":[128,2]
		}
		access_token = {"access_token": "aabbcc123", "expires_in": 7200}
		self.jsonWrite(wxUserInfo)

	@staticmethod
	def checkParams(self):
		pass
