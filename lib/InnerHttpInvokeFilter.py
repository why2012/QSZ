# coding: utf-8
import importlib
from conf.Config import *
from util.Exceptions import *
from util.ErrorCode import *
import tornado.web as web
import tornado.httputil as httputil

def innerhttp(conrtollername, queryparams, postparams = {}, controllerpath = "controller", conrtollerbucket = "controller_bucket"):
	def method_process(op):
		class FakeConnection(object):
			def set_close_callback(self, *args, **kwargs):
				pass
		def convert2StrList(vlist):
			for i, v in enumerate(vlist):
				if not isinstance(v, str):
					vlist[i] = str(v)
			return vlist

		def get_param(self, *args, **kwargs):
			contrModule = importlib.import_module(controllerpath + "." + conrtollername)
			contr = getattr(contrModule, conrtollername)
			for k, v in queryparams.items():
				if not isinstance(v, list):
					queryparams[k] = [str(v)]
				else:
					queryparams[k] = convert2StrList(v)
			for k, v in postparams.items():
				if not isinstance(v, list):
					postparams[k] = [str(v)]
				else:
					postparams[k] = convert2StrList(v)

			httpRequest = httputil.HTTPServerRequest("INNER", "inner://local", connection=FakeConnection())
			httpRequest.query_arguments = queryparams
			httpRequest.body_arguments = postparams
			httpRequest.arguments = queryparams
			for k, v in postparams:
				httpRequest.arguments.setdefault(k, []).extend(v)
				
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

	