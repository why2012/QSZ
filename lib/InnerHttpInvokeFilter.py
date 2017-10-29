# coding: utf-8
import importlib
from conf.Config import *
from util.Exceptions import *
from util.ErrorCode import *
import tornado.web as web
import tornado.httputil as httputil
from lib.ObjectAttrParser import *

#@innerhttp("TestController", {"A": 1, "B": [2]})
def innerhttp(_conrtollername, queryparams, postparams = {}, headers = {}, controllerpath = "controller", conrtollerbucket = "controller_bucket"):
	def method_process(op):
		class FakeConnection(object):
			def set_close_callback(self, *args, **kwargs):
				pass
		def convert2StrList(self, vlist):
			for i, v in enumerate(vlist):
				if not isinstance(v, str):
					v = str(v)
				vlist[i] = parseObjAttr(self, [str(v)])[0]
			return vlist

		def get_param(self, *args, **kwargs):
			conrtollername = _conrtollername
			modulename = conrtollername
			if "." in conrtollername:
				modulename, conrtollername = conrtollername.split(".", 1)
			contrModule = importlib.import_module(controllerpath + "." + modulename)
			contr = getattr(contrModule, conrtollername)
			for k, v in queryparams.items():
				if not isinstance(v, list):
					queryparams[k] = parseObjAttr(self, [str(v)])
				else:
					queryparams[k] = convert2StrList(self, v)
			for k, v in postparams.items():
				if not isinstance(v, list):
					postparams[k] = parseObjAttr(self, [str(v)])
				else:
					postparams[k] = convert2StrList(self, v)
			for k, v in headers.items():
				headers[k] = parseObjAttr(self, [str(v)])[0]

			httpRequest = httputil.HTTPServerRequest("INNER", "inner://local", connection=FakeConnection())
			httpRequest.query_arguments = queryparams
			httpRequest.body_arguments = postparams
			httpRequest.arguments = queryparams
			for k, v in postparams.items():
				httpRequest.arguments.setdefault(k, []).extend(v)
			for k, v in headers.items():
				httpRequest.headers.add(k, v)
				
			webApplication = UtilConfig.get("WebApplication")
			httpcontr = contr(webApplication, httpRequest)

			bucket = getattr(self, conrtollerbucket, None)
			if bucket == None or type(bucket) != "dict":
				setattr(self, conrtollerbucket, {})
			bucket = getattr(self, conrtollerbucket)
			httpcontr.invokeExecute()
			bucket[conrtollername] = httpcontr

			_fresult = op(self, *args, **kwargs)
			return _fresult
		return get_param
	return method_process

	