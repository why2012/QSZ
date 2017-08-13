# coding: utf-8
import hashlib

# key 密钥
def WxParamEncrypt(args, wxkey = ""):
	noEmpty = {}
	for key, value in args.items():
		if type(type) != "str":
			value = str(value)
		if value != "" and value is not None:
			noEmpty[key] = value
	noEmpty.keys().sort()
	argsString = ""
	args = []
	for key, value in noEmpty.items():
		args.append(key + "=" + value)
	argsString = "&".join(args)
	argsString += "&key=" + wxkey
	# print args
	# print argsString
	md5 = hashlib.md5() 
	md5.update(argsString)
	sign = md5.hexdigest().upper()
	return sign



