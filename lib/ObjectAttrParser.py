# coding: utf-8

def parseObjAttr(self, attrNameList):
	attrValueList = []
	globalMap = {"self": self}
	localMap = {}
	for attrName in attrNameList:
		attrName = str(attrName)
		try:
			exec("__local_v = %s" % attrName, globalMap, localMap)
			attrValueList.append(localMap["__local_v"]) # globalMap["__local_v"]
		except Exception, e:
			raise Exception("Illegal attribute name %s, because: %s" % (attrName, repr(type(e)) + str(e)))
	return attrValueList
