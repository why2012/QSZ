# coding: utf-8

# checkparam 无法执行动态赋值语句，函数参数在import后就已经确定
def checkparam(attrName, errMsg = "Oops, an error has occured", strict = False, default = None):
	def method_process(op):
		def get_param(self, *args, **kwargs):
			_attrName = attrName
			if _attrName.startswith("self."):
				_attrName = _attrName[5:]
			if default is None:
				if not hasattr(self, _attrName):
					raise Exception(errMsg)
				if strict:
					attr = getattr(self, _attrName)
					if attr is None:
						raise Exception(errMsg)
					if isinstance(attr, list) and len(attr) == 0:
						raise Exception(errMsg)
					if isinstance(attr, tuple) and len(attr) == 0:
						raise Exception(errMsg)
					if isinstance(attr, dict) and len(attr) == 0:
						raise Exception(errMsg)
				else:
					if getattr(self, _attrName) is None:
						raise Exception(errMsg)
			else:
				if not hasattr(self, _attrName):
					setattr(self, _attrName, default)
			op(self, *args, **kwargs)
		return get_param
	return method_process