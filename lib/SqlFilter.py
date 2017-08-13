# coding: utf-8
import importlib
from util.Exceptions import *
from util.ErrorCode import *
from service.GenericSqlService import *
from lib.ObjectAttrParser import *

# scope and scopeType for select
# holdon, and commit together
def sql(sqlString, sqlParams = (), scope = "sqlResult", scopeType = "object", affectId = "lastid", holdon = False):
	def method_process(op):
		def get_param(self, *args, **kwargs):
			sqlParamsValue = parseObjAttr(self, sqlParams)
			if not hasattr(self, "sqlServ"):
				sqlServ = GenericSqlService(self.db, self.cursor, self)
				setattr(self, "sqlServ", sqlServ)
			sqlServ = getattr(self, "sqlServ")
			sqlServ.SQL(sqlString, sqlParamsValue, scope, scopeType, affectId, holdon)
			_fresult = op(self, *args, **kwargs)
			return _fresult
		return get_param
	return method_process