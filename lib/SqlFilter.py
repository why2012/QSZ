# coding: utf-8
import importlib
from util.Exceptions import *
from util.ErrorCode import *
from service.GenericSqlService import *

def sql(sqlString, sqlParams = (), scope = "sqlResult", scopeType = "object"):
	def method_process(op):
		def get_param(self, *args, **kwargs):
			if not hasattr(self, "sqlServ"):
				sqlServ = GenericSqlService(self.db, self.cursor)
				setattr(self, "sqlServ", sqlServ)
			sqlServ = getattr(self, "sqlServ")
			sqlServ.SQL(self, sqlString, sqlParams, scope, scopeType)
			op(self, *args, **kwargs)
		return get_param
	return method_process