# coding: utf-8
from conf.Config import *

class BaseModel(object):
	def __init__(self):
		pass

	def dev_print_sql(self, sql, params):
		if DEV:
			print("-----SQL-----" + (sql % tuple(params)))