# coding: utf-8
from controller.TestController import *
from controller.FileAccessController import *
from controller.UserController import *
from controller.HouseController import *
from controller.FindHouseController import *
from controller.InviterController import *
from controller.OrderProcedureController import *
from controller.PaymentController import AliPaymentNotifyController

class UrlMapper(object):

	def __init__(self):
		self.mapper = [
			(r"/test", TestController),
			(r"/file/(.*)", FileAccessController),

			(r"/create_userinfo", UserInfoCreate), # 用户信息录入
			(r"/wx_fetch_userinfo", WxFetchUserInfo), # openid换取用户信息
			(r"/user_identification", UserRealNameIdentification), # 实名认证
			(r"/house_identification", HouseOwnerIdentification), # 房东身份认证

			(r"/house_create", HouseCreate), # 创建房源
			(r"/my_house_list", MyHouseList), # 房东房源列表
			(r"/update_house_info", UpdateHouseInfo), # 修改房源信息
			(r"/pulloff_house", PullOffHouse), # 下架房源
			(r"/delete_house_info", DeleteHouse), # 删除房源
			(r"/update_house_photo", UpdateHousePhoto), # 修改房源照片，一次一张
			(r"/create_house_photo", CreateHousePhoto), # 添加房源照片，一次一张
			(r"/update_house_video", UpdateHouseVideo), # 修改房源视频
			(r"/create_house_video", CreateHouseVideo), # 添加房源视频

			(r"/search_house", SearchHouseByName),# 搜索房源

			(r"/invitation/getcode", GetInvitationCode), # 获取邀请码
			(r"/invitation/setcode", SetInvitationCode), # 填写邀请码

			(r"/payment/ali/nontify/(.*)", AliPaymentNotifyController), # 支付回调接口
			(r"/payment/ali/nontify/userauth", AliPaymentNotifyController), # 用户授权回调接口

			(r"/order/create_preorder", CreatePreOrderController), # 创建看房申请			
			(r"/order/get_preorder_paymenturl", GetPreOrderPaymentUrlController), # 获取看房申请支付url
		]	

	def getMapper(self):
		return self.mapper