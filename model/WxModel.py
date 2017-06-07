# coding: utf-8
from model.BaseModel import *

class WxModel(BaseModel):
	def __init__(self, db, cursor):
		self.db = db
		self.cursor = cursor

	def getAccessToken(self):
		self.cursor.execute("select value from keyvalue_data where vkey=%s", (WX_ACCESS_TOKEN_KEY,))
		token = self.cursor.fetchone()
		return token is not None and {"access_token": token[0]}