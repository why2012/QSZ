# coding: utf-8
from model.BaseModel import *

class UserModel(BaseModel):
	def __init__(self, db, cursor):
		self.db = db
		self.cursor = cursor

	def findOneByPhoneAndPasswd(self, phone, passwd):
		pass

	def findUserByOpenid(self, openid):
		self.cursor.execute("""select 
			wx_openid, wx_nickname, wx_sex, wx_country, wx_province, wx_city, wx_headimgurl as headimgurl, id 
			from user_info where wx_openid=%s limit 1""", (openid,))
		userInfo = self.cursor.fetchone()
		if userInfo is not None:
			userInfo = {"wx_openid": userInfo[0], "wx_nickname": userInfo[1], "wx_sex": userInfo[2], "wx_country": userInfo[3],
			"wx_province": userInfo[4], "wx_city": userInfo[5], "headimgurl": userInfo[6], "id": userInfo[7]}
		return userInfo

	def insertUserWxInfo(self, userInfo):
		self.cursor.execute("""
			insert into 
			user_info(wx_province, wx_openid, wx_headimgurl, wx_city, wx_unionid, wx_sex, wx_country, wx_nickname) 
			values(%s, %s, %s, %s, %s, %s, %s, %s)
			""", (
				userInfo["province"], userInfo["openid"], userInfo["headimgurl"], userInfo["city"], userInfo["unionid"], 
				userInfo["sex"], userInfo["country"], userInfo["nickname"]
			))
		self.db.commit()
		return True
