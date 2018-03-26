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

PAYMENT_GLOBAL_CONFIG = {
	"NOTIFY_MID_PATH": "/payment/ali/nontify/",
	"PRE_ORDER_PAYMENT": "pre_order_payment",
	"APP_AUTH_NOTIFY": "app_auth_notify",
	"USER_AUTH_NOTIFY": "user_auth_notify",
}

AES_KEY = "skitfn,.|1-AJ*2^"
TOKEN_HEADER = "QSZ_TOKEN"
TOKEN_EXPIRE = 3600 * 24 * 5
TOKEN_NAME = "token"

VERIFY_HTTPS = False

MCH_NAME = "QSZ" # 商户名
WX_ACCESS_TOKEN_KEY = "wx_access_token"
WX_APPID = WxPayment["appid"]
WX_SECRET = WxPayment["wxkey"]
WX_ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={appid}&secret={secret}"
WX_USER_INFO_URL = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang=zh_CN"
WX_PAY_UNIFIEDORDER = "https://api.mch.weixin.qq.com/pay/unifiedorder"
WX_SEND_REDPACK = "https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack"

# ALI_APP_AUTH_TOKEN_NAME = "ali_app_auth_token"