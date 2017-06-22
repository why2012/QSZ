# coding: utf-8
import importlib
from util.Exceptions import *
from util.ErrorCode import *

def queryparam(paramName, ptype = "string", optional = False, default = None):
	def method_process(op):
		def get_param(self, *args, **kwargs):
			paramValue = None
			if ptype == "string":
				if default is None:
					paramValue = self.getStrArg(paramName)
				else:
					paramValue = self.getStrArg(paramName, default)
			elif ptype == "int":
				if default is None:
					paramValue = self.getIntArg(paramName)
				else:
					paramValue = self.getIntArg(paramName, default)
			elif ptype == "float":
				if default is None:
					paramValue = self.getFloatArg(paramName)
				else:
					paramValue = self.getFloatArg(paramName, default)
			elif ptype is None:
				paramValue = self.getArg(paramName, default)
			if not optional and (paramValue is None or (ptype == "string" and paramValue == "")):
				raise ErrorStatusException("Query param %s is None" % paramName, STATUS_PARAM_ERROR)
			setattr(self, paramName, paramValue)
			op(self, *args, **kwargs)
		return get_param
	return method_process