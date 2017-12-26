# coding: utf-8
import logging 

class BaseFilter(logging.Filter):
	def __init__(self, requestId):
		self.requestId = str(requestId)

	def setRequestId(self, requestId):
		self.requestId = requestId

	def getRequestId(self):
		return "[rid:%s] " % (self.requestId, )

class WarngingFilter(BaseFilter):
	def filter(self, record):
		if not hasattr(record, "request_id_in_msg"):
			record.msg = self.getRequestId() + record.msg
			record.request_id_in_msg = True
		return record.levelno == logging.WARNING

class ErrorFilter(BaseFilter):
	def filter(self, record):
		if not hasattr(record, "request_id_in_msg"):
			record.msg = self.getRequestId() + record.msg
			record.request_id_in_msg = True
		return record.levelno == logging.ERROR

class InfoDebugFilter(BaseFilter):
	def filter(self, record):
		if not hasattr(record, "request_id_in_msg"):
			record.msg = self.getRequestId() + record.msg
			record.request_id_in_msg = True
		return (record.levelno == logging.INFO or record.levelno == logging.DEBUG)