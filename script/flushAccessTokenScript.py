# coding: utf-8
from ScriptBase import *
import MySQLdb as mysql
from conf.Config import *
from util.Exceptions import *
import urllib2 as url
import json
import time

class FlushAccessToken(ScriptBase):
	def __init__(self):
		super(FlushAccessToken, self).__init__()
		self.db = mysql.connect(host = db_config["host"], user = db_config["user"], passwd = db_config["pwd"], db = db_config["db"], port = int(db_config["port"]), charset = db_config["charset"], use_unicode = True)
		self.cursor = self.db.cursor()

	def run(self):
		startTime = time.time()
		lastTime = -1
		while True:
			curTime = time.time()
			durTime = curTime - lastTime
			if durTime >= 4200:
				self.flushToken(curTime)
				lastTime = curTime

	def flushToken(self, curTime):
		try:
			res = url.urlopen(WX_ACCESS_TOKEN_URL.format(grant_type = "client_credential", appid  = WX_APPID, secret = WX_SECRET))
			rawData = res.read()
			print "flush_token" + str(curTime) + "|" + rawData
			responseData = json.loads(rawData)
			if "errcode" in responseData:
				self.loggerWaning.warn("[WX_WARNING]" + rawData)
			else:
				access_token = responseData['access_token']
				expires_in = int(responseData['expires_in'])
				self.cursor.execute("insert into keyvalue_data(vkey, value, remark, remarkInt) values(%s, %s, %s, %s) on duplicate key update vkey=%s, value=%s, remark=%s, remarkInt=%s", (WX_ACCESS_TOKEN_KEY , access_token, expires_in, int(curTime)) * 2)
				print self.cursor._executed 
				self.db.commit()
		except Exception, e:
			self.loggerWaning.warn("[WX_WARNING]" + str(e))

if __name__ == "__main__":
	FlushAccessToken().run()