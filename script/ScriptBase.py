# coding: utf-8
import sys
sys.path.append("..")
sys.path.append(".")
from lib.LoggerFilters import *
import logging
import logging.config

class ScriptBase(object):
	def __init__(self):
		logging.config.fileConfig("conf/Logging.conf")

		self.logger = logging.getLogger("controllerInfoDebug")
		self.loggerWaning = logging.getLogger("controllerWarning")
		self.loggerError = logging.getLogger("controllerError")

		self.logger.addFilter(InfoDebugFilter(requestId = -1))
		self.loggerWaning.addFilter(WarngingFilter(requestId = -1))
		self.loggerError.addFilter(ErrorFilter(requestId = -1))
