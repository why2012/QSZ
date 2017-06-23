# coding: utf-8
import importlib
from util.Exceptions import *
from util.ErrorCode import *
from service.GenericSqlService import *
from lib.ObjectAttrParser import *

def invoke(codeString):
	def method_process(op):
		def get_param(self, *args, **kwargs):
			lines = codeString.split("\n")
			lineOne = ""
			# fine first line code
			for line in lines:
				_line = line.strip()
				if not _line.startswith("#") and _line != "":
					lineOne = line
					break
			tCount = 0
			for ch in lineOne:
				if ch == "\t":
					tCount += 1
				else:
					break
			# replace code \t
			for index, line in enumerate(lines):
				lines[index] = line.replace("\t", "", tCount)
			_codeString = "\n".join(lines)
			exec _codeString in globals(), locals()
			_fresult = op(self, *args, **kwargs)
			return _fresult
		return get_param
	return method_process