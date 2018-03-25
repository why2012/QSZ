# coding: utf-8
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
import tornado.web as web
import json
import logging
import traceback
import sys
import random
from util.ErrorCode import *
from lib.LoggerFilters import *
from conf.Config import *
from util.Exceptions import *
import platform
import MySQLdb as mysql
from lib import *

class BaseController(web.RequestHandler):
	def __init__(self, application, request, **kwargs):
		super(BaseController, self).__init__(application, request, **kwargs)

	def initialize(self):
		try:
			self.logger = logging.getLogger("controllerInfoDebug")
			self.loggerWaning = logging.getLogger("controllerWarning")
			self.loggerError = logging.getLogger("controllerError")
			self.infoDebugFilter = InfoDebugFilter(1)
			self.warngingFilter = WarngingFilter(1)
			self.errorFilter = ErrorFilter(1)
			self.logger.addFilter(self.infoDebugFilter)
			self.loggerWaning.addFilter(self.warngingFilter)
			self.loggerError.addFilter(self.errorFilter)
			self.__argsNameMapper = {}
			self.__args = {}

			self.result = None

			self.version = platform.python_version_tuple()

			if sys.version_info[0] < 3:
				self.PY2 = True
			else:
				self.PY2 = False
		
			self.DBSetup()
		except Exception as e:
			print(e)

	def DBSetup(self):
		self.db = mysql.connect(host = db_config["host"], user = db_config["user"], passwd = db_config["pwd"], db = db_config["db"], port = int(db_config["port"]), charset = db_config["charset"], use_unicode = True)
		self.cursor = self.db.cursor()

	def post(self, *args):
		self.invokeExecute(*args)

	def get(self, *args):
		self.invokeExecute(*args)

	def invokeExecute(self, *args):
		if not hasattr(self, "requestId") or self.requestId is None:
			self.requestId = int(random.random() * 1000000000000000)
		self.infoDebugFilter.setRequestId(self.requestId)
		self.warngingFilter.setRequestId(self.requestId)
		self.errorFilter.setRequestId(self.requestId)
		self.logger.filters = [self.infoDebugFilter]
		self.loggerWaning.filters = [self.warngingFilter]
		self.loggerError.filters = [self.errorFilter]

		try:
			jsonobj = self.execute(*args)
			self.jsonobj = jsonobj
		except LoginException as e:
			self.setResult(status = e.getCode(), msg = e.getMsg())
		except ErrorStatusException as e:
			self.setResult(status = e.getCode(), msg = e.getMsg())
			self.loggerWaning.warn("HttpArgs:---" + self.oneLine(str(self.getAllArgs()) + "---; " + e.getMsg() + "\n" + traceback.format_exc()))
		except Exception as e:
			if len(e.args) == 2 and isinstance(e.args[1], int):
				self.setResult(status = e.args[1], msg = str(e.args[0]))
			else:
				if DEV:
					print(traceback.format_exc())
				self.setResult(status = INTERNAL_ERROR, msg = str(e))
				self.loggerError.error("HttpArgs:---" + self.oneLine(str(self.getAllArgs()) + "---; " + str(e) + "\n" + traceback.format_exc()))
		finally:
			if self.db:
				self.db.close()
			if self.result is None and jsonobj is not None:
				self.result = {"status": STATUS_OK, "ans": jsonobj, "msg": ""}
			if self.result is not None:
				self.set_header('Content-Type', 'application/json')
				self.jsonWrite(self.result)
				self.logger.info("HttpArgs:---" + self.oneLine(str(self.getAllArgs())) + "---; " + json.dumps(self.result, ensure_ascii = False))
			if self.result is None and hasattr(self, "resultBody") and self.resultBody is not None:
				self.rawTextWrite(self.resultBody)
				self.logger.info(self.resultBody)
			self.requestId = None

	def execute(self):
		pass

	def jsonWrite(self, data):
		self.write(json.dumps(data, ensure_ascii = False))

	def rawTextWrite(self, text):
		self.write(text)

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

	def getUpFileName(self, name = "file", raiseException = True):
		name = self.__getArgName(name)
		if name in self.request.files:
			fileMetas = self.request.files[name]
			if fileMetas:
				for meta in fileMetas:
					return meta['filename']
		elif raiseException:
			raise ErrorStatusException(name + " must not be None", STATUS_PARAM_ERROR)

	def getUpFileNames(self, name = "file", raiseException = True):
		name = self.__getArgName(name)
		if name in self.request.files:
			fileMetas = self.request.files[name]
			fileNameList = []
			if fileMetas:
				for meta in fileMetas:
					fileNameList.append(meta['filename'])
			return fileNameList
		elif raiseException:
			raise ErrorStatusException(name + " must not be None", STATUS_PARAM_ERROR)

	def processUpFile(self, name = "file", raiseException = True):
		name = self.__getArgName(name)
		if name in self.request.files:
			fileMetas = self.request.files[name]
			if fileMetas:
				for meta in fileMetas:
					return meta['body']
		elif raiseException:
			raise ErrorStatusException(name + " must not be None", STATUS_PARAM_ERROR)

	def processUpFiles(self, name = "file", raiseException = True):
		name = self.__getArgName(name)
		if name in self.request.files:
			fileMetas = self.request.files[name]
			fileBodyList = []
			if fileMetas:
				for meta in fileMetas:
					fileBodyList.append(meta['body'])
			return fileBodyList
		elif raiseException:
			raise ErrorStatusException(name + " must not be None", STATUS_PARAM_ERROR)

	@property
	def remote_ip(self):
		return self.request.remote_ip 

	@property
	def post_body(self):
		return self.request.body

	@property
	def local_ip():
		import socket
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
        	# doesn't even have to be reachable
			s.connect(('10.255.255.255', 0))
			IP = s.getsockname()[0]
		except:
			IP = '127.0.0.1'
		finally:
			s.close()
			return IP

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

