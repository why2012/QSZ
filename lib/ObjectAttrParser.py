# coding: utf-8

def parseObjAttr(self, attrNameList):
	attrValueList = []
	for attrName in attrNameList:
		attrName = str(attrName)
		if not attrName.startswith("self."):
			attrValueList.append(attrName)
			continue
		else:
			attrName = attrName[5:]
		try:
			realName = attrName
			itemIndex = -1
			attrValue = None
			# for list attribute
			if '[' in attrName and ']' in attrName:
				realName = attrName[:attrName.index('[')]
				itemIndex = attrName[attrName.index('[') + 1: attrName.index(']')]
			attrSelf = getattr(self, realName)
			attrValue = attrSelf
			if itemIndex != -1:
				attrValue = attrSelf[itemIndex]
			attrValueList.append(attrValue)
		except:
			raise Exception("Illegal attribute name %s" % attrName)
	return attrValueList
