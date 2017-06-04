# coding: utf-8
import MySQLdb as mysql
from conf.Config import *

def initDB():
	db = mysql.connect(host = db_config["host"], user = db_config["user"], passwd = db_config["pwd"], db = db_config["db"], charset = db_config["charset"], use_unicode = True)
	cursor = self.db.cursor()