# coding: utf-8

AliPayment = {
	"appid": "",
	"secret_key": "",
	# 应用公钥, 无作用
	"public_key": "",
	"format": "JSON",
	"charset": "utf-8",
	"sign_type": "RSA2",
	"version": "1.0",
	"app_auth_token_db_key": "ali_payment_app_authtoken",
	"app_startup_auth_token": "",
	"notify_url_domain": "",
	"return_url_domain": "",
	"payment": { # 付款参数
		# 支付宝公钥，验签用
		"public_key": "",
		"domain_url": "https://openapi.alipay.com/gateway.do",
		"method": "alipay.trade.wap.pay",
		"notify_url": "",
		"return_url": "",
		"product_code": "QUICK_WAP_WAY",
		"goods_type": 0,
	},
	"transfer": {
		"domain_url": "https://openapi.alipay.com/gateway.do",
		"method": "alipay.fund.trans.toaccount.transfer",
		"charset": "utf-8",
		"sign_type": "RSA2",
		"version": "1.0",
	},
	"usercode": {
		"domain_url": "https://openauth.alipay.com/oauth2/publicAppAuthorize.htm",
		"scope": "auth_user",
		"redirect_uri": ""
	},
	"userauth": {
		"domain_url": "https://openapi.alipay.com/gateway.do",
		"method": "alipay.system.oauth.token",
		"charset": "utf-8",
		"sign_type": "RSA2",
		"version": "1.0",
		"grant_type": "authorization_code",
	}
}