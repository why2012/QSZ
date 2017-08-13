# coding: utf-8
import importlib

def service(serviceName, variableName, servicePath = "service", **servkwargs):
	def method_process(op):
		def get_service(self, *args, **kwargs):
			servModule = importlib.import_module(servicePath + "." + serviceName)
			serv = getattr(servModule, serviceName)
			for k, v in servkwargs.items():
				if isinstance(v, str) and v.strip() == "self":
					servkwargs[k] = self
			setattr(self, variableName, serv(self.db, self.cursor, **servkwargs))
			_fresult = op(self, *args, **kwargs)
			return _fresult
		return get_service
	return method_process