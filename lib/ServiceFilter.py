# coding: utf-8
import importlib

def service(serviceName, variableName, servicePath = "service", **servkwargs):
	def method_process(op):
		def get_service(self, *args, **kwargs):
			servModule = importlib.import_module(servicePath + "." + serviceName)
			serv = getattr(servModule, serviceName)
			setattr(self, variableName, serv(self.db, self.cursor, **servkwargs))
			op(self, *args, **kwargs)
		return get_service
	return method_process