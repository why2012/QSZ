# coding: utf-8
import importlib
from util.Exceptions import *
from util.ErrorCode import *
import os

# filename, query param name; newfilename, without extension name; self.useridname; self.uniqueIdname
def userfiles(filename, newfilenamePrototype, useridname = "userId", basepath = "data/userphoto/", overwrite = True, uniqueidname = None):
	if not basepath.endswith("/"):
		basepath += "/"
	def method_process(op):
		def get_param(self, *args, **kwargs):
			newfilename = newfilenamePrototype
			if not self.fileExist(filename) or getattr(self, useridname) is None:
				raise ErrorStatusException("file param %s is None" % filename, STATUS_PARAM_ERROR)
			upfilenames = self.getUpFileNames(filename)
			if upfilenames is None or len(upfilenames) == 0:
				raise ErrorStatusException("filename is None or illegal", STATUS_PARAM_ERROR)
			extnames = [upfilename.split(".")[-1] for upfilename in upfilenames]
			userid = getattr(self, useridname)
			basedir = basepath + "user_" + userid + "/"
			if not os.path.exists(basedir):
				os.makedirs(basedir)
			newfilenames = [newfilename + "-" + str(i) for i in range(len(upfilenames))]
			if uniqueidname is None:
				newfilepathes = [basedir + newfilename + "." + extnames[i] for i, newfilename in enumerate(newfilenames)]
			else:
				if not uniqueidname.startswith("[trigger]"):
					newfilepathes = [basedir + newfilename + "-" + getattr(self, uniqueidname) + "." + extnames[i] for i, newfilename in enumerate(newfilenames)]
				else:
					uniqueidnameIndex = uniqueidname.index("]")
					_uniqueidname = uniqueidname[uniqueidnameIndex + 1:]
					newfilepathes = [basedir + newfilename + "-" + "%s" + "." + extname for newfilename in newfilenames]
					if not hasattr(self, "_saveFileFuncParams"):
						setattr(self, "_saveFileFuncParams", [])
					self._saveFileFunc = saveFileFunc
					self._saveFileFuncParams.append({"self": self, "upfilenames": upfilenames, "filename": filename, "newfilepathes": newfilepathes, "overwrite": overwrite, "uniqueidname": _uniqueidname, "newfilenames": newfilenames, "newfilenamePrototype": newfilenamePrototype})
					# self._saveFileFunc(**self._saveFileFuncParams[0])
					_fresult = op(self, *args, **kwargs)
					return _fresult
			saveFileFunc(self, upfilenames, filename, newfilepathes, overwrite, None, newfilenames, newfilenamePrototype)
			_fresult = op(self, *args, **kwargs)
			return _fresult
		return get_param

	def saveFileFunc(self, upfilenames, filename, newfilepathes, overwrite, uniqueidname = None, newfilenames = None, newfilenamePrototype = None):
		if uniqueidname is not None:
			uniqueidname = getattr(self, uniqueidname)
			if uniqueidname is None:
				raise ErrorStatusException("uniqueidname is None", INTERNAL_ERROR)
			newfilepathes = [newfilepath % uniqueidname for newfilepath in newfilepathes]
		if overwrite is False:
			for i, newfilepath in enumerate(newfilepathes):
				if os.path.exists(newfilepath):
					raise ErrorStatusException("file %s already exists" % upfilename[i], STATUS_FILE_EXISTS)
		filebodyList = self.processUpFiles(filename)
		if self.PY2:
			for i, newfilepath in enumerate(newfilepathes):
				with open(newfilepath, "w") as ufile:
					ufile.write(filebodyList[i])
		else:
			for i, newfilepath in enumerate(newfilepathes):
				with open(newfilepath, "wb") as ufile:
					ufile.write(filebodyList[i])
		if newfilenamePrototype is not None:	
			setattr(self, newfilenamePrototype, newfilepathes) 
	return method_process


