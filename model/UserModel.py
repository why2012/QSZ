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
			wx_openid, wx_nickname, wx_sex, wx_country, wx_province, wx_city, wx_headimgurl, id,
			addressProvince, addressCity, birthday, constellations, education, occupation, virtual_tel_flag,
			virtual_tel, wechat, qq, headimgurl
			from user_info where wx_openid=%s limit 1""", (openid,))
		userInfo = self.cursor.fetchone()
		userInfoMap = {}
		if userInfo is not None:
			userInfoMap = {"wx_openid": userInfo[0], "wx_nickname": userInfo[1], "wx_sex": userInfo[2], "wx_country": userInfo[3],
			"wx_province": userInfo[4], "wx_city": userInfo[5], "wx_headimgurl": userInfo[6], "id": userInfo[7]}
			userInfoMap["addressProvince"] = userInfo[8]
			userInfoMap["addressCity"] = userInfo[9]
			userInfoMap["birthday"] = userInfo[10]
			userInfoMap["constellations"] = userInfo[11]
			userInfoMap["education"] = userInfo[12]
			userInfoMap["occupation"] = userInfo[13]
			userInfoMap["virtual_tel_flag"] = userInfo[14]
			userInfoMap["virtual_tel"] = userInfo[15]
			userInfoMap["wechat"] = userInfo[16]
			userInfoMap["qq"] = userInfo[17]
			userInfoMap["headimgurl"] = userInfo[18]
		else:
			userInfoMap = None
		return userInfoMap

	def findUserByUserid(self, userid):
		self.cursor.execute("""select 
			wx_openid, wx_nickname, wx_sex, wx_country, wx_province, wx_city, wx_headimgurl, id,
			addressProvince, addressCity, birthday, constellations, education, occupation, virtual_tel_flag,
			virtual_tel, wechat, qq, headimgurl
			from user_info where id=%s limit 1""", (userid,))
		userInfo = self.cursor.fetchone()
		userInfoMap = {}
		if userInfo is not None:
			userInfoMap = {"wx_openid": userInfo[0], "wx_nickname": userInfo[1], "wx_sex": userInfo[2], "wx_country": userInfo[3],
			"wx_province": userInfo[4], "wx_city": userInfo[5], "wx_headimgurl": userInfo[6], "id": userInfo[7]}
			userInfoMap["addressProvince"] = userInfo[8]
			userInfoMap["addressCity"] = userInfo[9]
			userInfoMap["birthday"] = userInfo[10]
			userInfoMap["constellations"] = userInfo[11]
			userInfoMap["education"] = userInfo[12]
			userInfoMap["occupation"] = userInfo[13]
			userInfoMap["virtual_tel_flag"] = userInfo[14]
			userInfoMap["virtual_tel"] = userInfo[15]
			userInfoMap["wechat"] = userInfo[16]
			userInfoMap["qq"] = userInfo[17]
			userInfoMap["headimgurl"] = userInfo[18]
		else:
			userInfoMap = None
		return userInfoMap

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
