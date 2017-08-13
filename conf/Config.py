# coding: utf-8
DEV = True
if DEV:
	from DevConfig import * 
else:
	from OnlineConfig import * 

from WxPayment import *

from Location import *

AES_KEY = "skitfn,.|1-AJ*2^"
TOKEN_HEADER = "QSZ_TOKEN"
TOKEN_EXPIRE = 3600 * 24 * 5
TOKEN_NAME = "token"

MCH_NAME = "QSZ" # 商户名
WX_ACCESS_TOKEN_KEY = "wx_access_token"
WX_APPID = ""
WX_SECRET = ""
WX_ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={appid}&secret={secret}"
WX_USER_INFO_URL = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang=zh_CN"
WX_PAY_UNIFIEDORDER = "https://api.mch.weixin.qq.com/pay/unifiedorder"
WX_SEND_REDPACK = "https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack"