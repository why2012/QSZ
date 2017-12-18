# coding: utf-8

def parseObjAttr(self, attrNameList):
	attrValueList = []
	globalMap = {"self": self}
	localMap = {}
	for attrName in attrNameList:
		attrName = str(attrName)
		try:
			if "self." in attrName:
				exec("__local_v = %s" % attrName, globalMap, localMap)
				attrValueList.append(localMap["__local_v"]) # globalMap["__local_v"]
			else:
				attrValueList.append(attrName)
		except Exception as e:
			raise Exception("Illegal attribute name %s, because: %s" % (attrName, repr(type(e)) + str(e)))
	return attrValueList
