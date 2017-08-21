# coding: utf-8

AliPayment = {
	"appid": "",
	"secret_key": "",
	"format": "JSON",
	"charset": "utf-8",
	"sign_type": "RSA2",
	"version": "1.0",
	"payment": { # 付款参数
		"domain_url": "https://openapi.alipay.com/gateway.do",
		"method": "alipay.trade.wap.pay",
		"notify_url": "",
		"return_url": "",
		"product_code": "QUICK_WAP_WAY",
		"goods_type": 0,
	}	
}