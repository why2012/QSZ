# coding: utf-8
import tornado.web as web
import json
import logging
import traceback
from util.ErrorCode import *
from lib.LoggerFilters import *
from conf.Config import *
from util.Exceptions import *
import platform
import MySQLdb as mysql
from lib.LoginFilter import *
from lib.ServiceFilter import *
from lib.QueryparamFilter import *

class BaseController(web.RequestHandler):
	def initialize(self):
		try:
			self.logger = logging.getLogger("controllerInfoDebug")
			self.loggerWaning = logging.getLogger("controllerWarning")
			self.loggerError = logging.getLogger("controllerError")

			self.logger.addFilter(InfoDebugFilter())
			self.loggerWaning.addFilter(WarngingFilter())
			self.loggerError.addFilter(ErrorFilter())
			self.__argsNameMapper = {}
			self.__args = {}

			self.result = None

			self.version = platform.python_version_tuple()
		
			self.DBSetup()
		except Exception, e:
			print e

	def DBSetup(self):
		self.db = mysql.connect(host = db_config["host"], user = db_config["user"], passwd = db_config["pwd"], db = db_config["db"], port = db_config["port"], charset = db_config["charset"], use_unicode = True)
		self.cursor = self.db.cursor()

	def post(self):
		self.invokeExecute()

	def get(self):
		self.invokeExecute()

	def invokeExecute(self):
		try:
			self.execute()
		except LoginException, e:
			self.setResult(status = e.getCode(), msg = e.getMsg())
		except ErrorStatusException, e:
			self.setResult(status = e.getCode(), msg = e.getMsg())
			self.loggerWaning.warn(self.oneLine(str(self.getAllArgs()) + "; " + e.getMsg() + "\n" + traceback.format_exc()))
		except Exception, e:
			self.setResult(status = STATUS_SCAN_ERROR, msg = "Internal Error: " + repr(type(e)) + ", " + str(e))
			self.loggerError.error(self.oneLine(str(self.getAllArgs()) + "; " + str(e) + "\n" + traceback.format_exc()))
		finally:
			if self.result is not None:
				self.set_header('Content-Type', 'application/json')
				self.jsonWrite(self.result)

	def execute(self):
		pass

	def jsonWrite(self, data):
		self.write(json.dumps(data, ensure_ascii = False))

	def jsonDump(self, data):
		return json.dumps(data, ensure_ascii = False)

	def jsonLoad(self, data):
		return json.loads(data)

	def setResult(self, ans = [], status = STATUS_OK, msg = ""):
		self.result = {"status": status, "ans": ans, "msg": msg}

	def getResult(self):
		if self.result:
			return self.result
		else:
			return None

	def fileExist(self, name = "file"):
		name = self.__getArgName(name)
		if name in self.request.files:
			return True
		else: 
			return False

	def processUpFile(self, name = "file", raiseException = True):
		name = self.__getArgName(name)
		if name in self.request.files:
			fileMetas = self.request.files[name]
			if fileMetas:
				for meta in fileMetas:
					return meta['body']
		elif raiseException:
			raise ErrorStatusException(name + " must not be None", STATUS_PARAM_ERROR)

	def getIntArg(self, key, default = -1):
		arg = self.getArg(key, default)
		if not arg or arg is None:
			return default
		return int(float(arg))

	def getIntArgs(self, key, default = [], sep = ","):
		arg = self.getArg(key, default)
		if not arg or arg is None:
			return default
		args = arg.split(sep)
		return [int(float(i)) for i in args]

	def getFloatArg(self, key, default = -1):
		arg = self.getArg(key, default)
		if not arg or arg is None:
			return default
		return float(arg)

	def getStrArg(self, key, default = ""):
		return self.getArg(key, default)

	def getArg(self, key, default = None):
		key = self.__getArgName(key)
		if key in self.__args:
			return self.__args[key]
		arg = self.get_argument(key, default)
		return arg

	def setArg(self, key, value):
		self.__args[key] = value

	def getAllArgs(self):
		argNames = self.request.arguments
		args = {}
		for argName in argNames:
			args[argName] = self.get_argument(argName)
		return args

	def changeArgName(self, key, newName):
		self.__argsNameMapper[key] = newName

	def __getArgName(self, name):
		if name in self.__argsNameMapper:
			return self.__argsNameMapper[name]
		else:
			return name 

	def oneLine(self, msg):
		msg = msg.replace("\n", " | ")  
		return msg

