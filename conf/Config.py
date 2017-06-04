# coding: utf-8
DEV = True
if DEV:
	from DevConfig import * 
else:
	from OnlineConfig import * 

AES_KEY = "skitfn,.|1-AJ*2^"
TOKEN_HEADER = "QSZ_TOKEN"
TOKEN_EXPIRE = 3600 * 24
TOKEN_NAME = "token"