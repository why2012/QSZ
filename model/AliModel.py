# coding: utf-8
from model.BaseModel import *

class AliModel(BaseModel):
	def __init__(self, db, cursor):
		self.db = db
		self.cursor = cursor

	# return auth_token and is_expired and refresh_token and re_expire_in
	def getAppToken(self):
		self.cursor.execute("select value, remark from keyvalue_data where vkey=%s", (AliPayment["app_auth_token_db_key"],))
		data = self.cursor.fetchone()
		if data is None:
			return (0, True, 0, 0)
		else:
			token, expire_in, start_date = data[0].split("|")
			expire_in = int(expire_in)
			start_date = int(start_date)
			refresh_token, re_expire_in = data[1].split("|")
			re_expire_in = int(re_expire_in)
			if start_date + expire_in > time.time() + 60 * 5:
				return (token, False, 0, 0)
			else:
				return (token, True, refresh_token, re_expire_in)

	def insertAppToken(self, app_token, expire_in, start_date, refresh_token, re_expire_in):
		value = app_token + "|" + str(expire_in) + "|" + str(start_date)
		remark = refresh_token + "|" + str(re_expire_in)
		self.cursor.execute("""
			insert into keyvalue_data(vkey, value, remark) values(%s, %s, %s) ON DUPLICATE KEY UPDATE value=%s, remark=%s
			""", (AliPayment["app_auth_token_db_key"], value, remark, value, remark))
		self.db.commit()
		return True
