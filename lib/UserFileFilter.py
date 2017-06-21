# coding: utf-8
import importlib
from util.Exceptions import *
from util.ErrorCode import *
import os

# filename, query param name; newfilename, without extension name; self.useridname; self.uniqueIdname
def userfile(filename, newfilename, useridname = "userId", basepath = "data/userphoto/", overwrite = True, uniqueidname = None):
	if not basepath.endswith("/"):
		basepath += "/"
	def method_process(op):
		def get_param(self, *args, **kwargs):
			if not self.fileExist(filename) or getattr(self, useridname) is None:
				raise ErrorStatusException("file param %s is None" % filename, STATUS_PARAM_ERROR)
			upfilename = self.getUpFileName(filename)
			if upfilename is None:
				raise ErrorStatusException("filename is None or illegal", STATUS_PARAM_ERROR)
			extname = upfilename.split(".")[-1]
			userid = getattr(self, useridname)
			basedir = basepath + "user_" + userid + "/"
			if not os.path.exists(basedir):
				os.makedirs(basedir)
			if uniqueidname is None:
				newfilepath = basedir + newfilename + "." + extname
			else:
				if not uniqueidname.startswith("[trigger]"):
					newfilepath = basedir + newfilename + "-" + getattr(self, uniqueidname) + "." + extname
				else:
					uniqueidnameIndex = uniqueidname.index("]")
					_uniqueidname = uniqueidname[uniqueidnameIndex + 1:]
					newfilepath = basedir + newfilename + "-" + "%s" + "." + extname
					if not hasattr(self, "_saveFileFuncParams"):
						setattr(self, "_saveFileFuncParams", [])
					self._saveFileFunc = saveFileFunc
					self._saveFileFuncParams.append({"self": self, "upfilename": upfilename, "filename": filename, "newfilepath": newfilepath, "overwrite": overwrite, "uniqueidname": _uniqueidname, "newfilename": newfilename})
					# self._saveFileFunc(**self._saveFileFuncParams[0])
					op(self, *args, **kwargs)
					return
			saveFileFunc(self, upfilename, filename, newfilepath, overwrite, None, newfilename)
			op(self, *args, **kwargs)
		return get_param

	def saveFileFunc(self, upfilename, filename, newfilepath, overwrite, uniqueidname = None, newfilename = None):
		if uniqueidname is not None:
			uniqueidname = getattr(self, uniqueidname)
			if uniqueidname is None:
				raise ErrorStatusException("uniqueidname is None", INTERNAL_ERROR)
			newfilepath = newfilepath % uniqueidname
		if overwrite is False:
			if os.path.exists(newfilepath):
				raise ErrorStatusException("file %s already exists" % upfilename, STATUS_FILE_EXISTS)
		filebody = self.processUpFile(filename)
		with open(newfilepath, "w") as ufile:
			ufile.write(filebody)
		if newfilename is not None:	
			setattr(self, newfilename, newfilepath) 
	return method_process