# coding: utf-8
from controller.BaseController import *
import dependency.qcloud_video as qcloud

# TODO
# 房东身份认证
class HouseOwnerIdentification(BaseController):
	@checklogin()
	@queryparam("realname", "string")
	@queryparam("idcardnumber", "string")
	# 房产证号
	@queryparam("property_cert_number", "string")
	# @userfile("property_cert_photo", "property_cert_photo", uniqueidname = "[trigger]property_cert_number")
	@userfile("property_cert_photo", "property_cert_photo", uniqueidname = "property_cert_number")
	def execute(self):
		# self.property_cert_number = "123456"
		# self._saveFileFunc(**self._saveFileFuncParams)
		self.setResult([self.realname, self.idcardnumber, self.property_cert_number])

# TODO
# 房东房源列表
class MyHouseList(BaseController):
	@checklogin()
	def execute(self):
		pass

# TODO
# 修改房源信息
class UpdateHouseInfo(BaseController):
	@checklogin()
	def execute(self):
		pass

# TODO
# 下架房源
class PullOffHouse(BaseController):
	@checklogin()
	def execute(self):
		pass

# TODO
# 删除房源
class DeleteHouse(BaseController):
	@checklogin()
	def execute(self):
		pass

# TODO
# 创建房源
class HouseCreate(BaseController):
	@checklogin()
	# 省
	@queryparam("province_name", "string")
	@queryparam("province_code", "string")
	# 市
	@queryparam("city_name", "string")
	@queryparam("city_code", "string")
	# 区县
	@queryparam("county_name", "string")
	@queryparam("county_code", "string")
	# 小区
	@queryparam("district_name", "string", optional = True)
	@queryparam("district_code", "string", optional = True)
	# 门牌号
	@queryparam("house_number", "string", optional = True)
	# 经纬度
	@queryparam("longitude", "string")
	@queryparam("latitude", "string")
	# 出租方式，长租2-短租1
	@queryparam("rent_time_type", "string")
	# 出租方式，整租1-单间2
	@queryparam("rent_room_type", "string")
	# 面积
	@queryparam("house_area", "string", optional = True)
	# 户型
	@queryparam("house_type", "string", optional = True)
	# 楼层
	@queryparam("house_floor", "string", optional = True)
	# 朝向
	@queryparam("house_direction", "string", optional = True)
	# 装修程度
	@queryparam("house_decoration", "string", optional = True)
	# 最大居住人数
	@queryparam("house_max_livein", "string", optional = True)
	# 租金
	@queryparam("house_rent", "string")
	# 付款方式, 1|3 押一付三, 2|6 押二付六, 1|0 无押金
	@queryparam("payment_type", "string")
	# 物业费, 1 房东, 2 租客, 3 待定
	@queryparam("property_management_fee", "string")
	# 取暖费
	@queryparam("heating_charge", "string")
	# 介绍标题
	@queryparam("description_title", "string", optional = True)
	# 特色介绍
	@queryparam("description", "string", optional = True)
	# 交通情况
	@queryparam("traffic_condition", "string", optional = True)
	# 周边情况
	@queryparam("around_condition", "string", optional = True)
	# 房屋设施
	# 1 空调, 2 暖气, 3 洗衣机, 4 冰箱, 5 允许宠物, 6 电视, 7 浴缸, 8 热水淋浴, 9 门禁系统, 10 有线网络, 11 电梯, 12 无线网络, 13 停车位, 14 饮水机
	# 1|2|3
	@queryparam("facility", "string", optional = True)
	def execute(self):
		pass





