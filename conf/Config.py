# coding: utf-8
import lib.ConfigSecHelper as ConfigSecHelper

DEV = True
config_sec_path = ""
if DEV:
	from .DevConfig import * 
	config_sec_path = "dev_db_config"
else:
	from .OnlineConfig import * 
	config_sec_path = "online_db_config"

from .WxPayment import *

from .AliPayment import *

from .Location import *

from .UtilConfig import *

ConfigSecHelper.start_extract({"WxPayment": WxPayment, "AliPayment": AliPayment, config_sec_path: db_config})

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