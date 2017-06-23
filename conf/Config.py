# coding: utf-8
DEV = False
if DEV:
	from DevConfig import * 
else:
	from OnlineConfig import * 

from Location import *

AES_KEY = "skitfn,.|1-AJ*2^"
TOKEN_HEADER = "QSZ_TOKEN"
TOKEN_EXPIRE = 3600 * 24 * 5
TOKEN_NAME = "token"

WX_ACCESS_TOKEN_KEY = "wx_access_token"
WX_APPID = ""
WX_SECRET = ""
WX_ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={appid}&secret={secret}"
WX_USER_INFO_URL = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang=zh_CN"