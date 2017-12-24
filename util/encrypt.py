# coding: utf-8
import hashlib
import json
import sys
if sys.version_info[0] < 3:
	reload(sys).setdefaultencoding('utf-8')  
	PY2 = True
else:
	PY2 = False

# key 密钥
def WxParamEncrypt(args, wxkey = ""):
	noEmpty = {}
	for key, value in args.items():
		if not isinstance(value, str):
			if isinstance(value, dict) or isinstance(value, tuple):
				value = json.dumps(value, ensure_ascii = False)
			else:
				value = str(value)
		if value != "" and value is not None:
			noEmpty[key] = value
	keys = noEmpty.keys()
	keys.sort()
	args = []
	for key in keys:
		value = noEmpty[key]
		args.append(key + "=" + value)
	argsString = "&".join(args)
	argsString += "&key=" + wxkey
	# print args
	# print argsString
	md5 = hashlib.md5() 
	md5.update(argsString)
	sign = md5.hexdigest().upper()
	return sign

def AliParamEncrypt(args, secretKey = ""):
	import rsa
	import base64
	noEmpty = {}
	for key, value in args.items():
		if not isinstance(value, str):
			if isinstance(value, dict) or isinstance(value, tuple):
				value = json.dumps(value, ensure_ascii = False)
			else:
				value = str(value)
		if value != "" and value is not None:
			noEmpty[key] = value
	if PY2:
		keys = noEmpty.keys()
	else:
		keys = list(noEmpty.keys())
	keys.sort()
	argsString = ""
	args = []
	for key in keys:
		value = noEmpty[key]
		args.append(key + "=" + value)
	argsString = "&".join(args)
	# print args
	# print argsString
	secretKey = "-----BEGIN RSA PRIVATE KEY-----\n" + secretKey + "\n-----END RSA PRIVATE KEY-----"
	privkey = rsa.PrivateKey.load_pkcs1(secretKey)
	if PY2:
		sign = base64.b64encode(rsa.sign(argsString, privkey, "SHA-256"))
	else:
		sign = base64.b64encode(rsa.sign(argsString.encode("utf-8"), privkey, "SHA-256"))
	# print "--------------", argsString
	# print "++++++++++++++", sign
	return sign

def AliParamVerify(args, publicKey = ""):
	from urllib import unquote
	import rsa
	import base64
	sign = base64.b64decode(args["sign"])
	paymentObj = {}
	for key, value in args.items():
		if key != "sign" and key != "sign_type":
			if not isinstance(value, str):
				value = str(value)
			paymentObj[key] = unquote(value)

	noEmpty = {}
	for key, value in paymentObj.items():
		if value != "" and value is not None:
			noEmpty[key] = value
	if PY2:
		keys = noEmpty.keys()
	else:
		keys = list(noEmpty.keys())
	keys.sort()
	argsString = ""
	args = []
	for key in keys:
		value = noEmpty[key]
		args.append(key + "=" + value)
	argsString = "&".join(args)
	message = argsString
	print("++++++++++")
	print(args)
	print(message)

	publicKey = "-----BEGIN PUBLIC KEY-----\n" + publicKey + "\n-----END PUBLIC KEY-----"
	pubKey = rsa.PublicKey.load_pkcs1_openssl_pem(publicKey)
	return rsa.verify(message, sign, pubKey)










