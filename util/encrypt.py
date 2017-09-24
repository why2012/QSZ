# coding: utf-8
import hashlib

# key 密钥
def WxParamEncrypt(args, wxkey = ""):
	noEmpty = {}
	for key, value in args.items():
		if not isinstance(value, str):
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
			value = str(value)
		if value != "" and value is not None:
			noEmpty[key] = value
	keys = noEmpty.keys()
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
	sign = base64.b64encode(rsa.sign(argsString, privkey, "SHA-256"))
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
	keys = noEmpty.keys()
	keys.sort()
	argsString = ""
	args = []
	for key in keys:
		value = noEmpty[key]
		args.append(key + "=" + value)
	argsString = "&".join(args)
	message = argsString
	# print args
	# print message

	publicKey = "-----BEGIN PUBLIC KEY-----\n" + publicKey + "\n-----END PUBLIC KEY-----"
	pubKey = rsa.PublicKey.load_pkcs1_openssl_pem(publicKey)
	return rsa.verify(message, sign, pubKey)










