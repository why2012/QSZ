# coding: utf-8
from controller.TestController import *
from controller.UserController import *
from controller.HouseController import *

class UrlMapper(object):

	def __init__(self):
		self.mapper = [
			(r"/test", TestController),
			
			(r"/create_userinfo", UserInfoCreate), # 用户信息录入
			(r"/wx_fetch_userinfo", WxFetchUserInfo), # openid换取用户信息
			(r"/user_identification", UserRealNameIdentification), # 实名认证
			(r"/house_identification", HouseOwnerIdentification), # 房东身份认证
			(r"/house_create", HouseCreate), # 创建房源
			(r"/my_house_list", MyHouseList), # 房东房源列表
			(r"/update_house_info", UpdateHouseInfo), # 修改房源信息
			(r"/pulloff_house", PullOffHouse), # 下架房源
			(r"/delete_house_info", DeleteHouse), # 删除房源
		]	

	def getMapper(self):
		return self.mapper