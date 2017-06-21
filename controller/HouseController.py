# coding: utf-8
from controller.BaseController import *
import dependency.qcloud_video as qcloud

# 房东身份认证
class HouseOwnerIdentification(BaseController):
	@checklogin()
	# 房产证姓名
	@queryparam("certname", "string")
	@queryparam("idcardnumber", "string")
	# 房产证号
	@queryparam("property_cert_number", "string")
	# @userfile("property_cert_photo", "property_cert_photo", uniqueidname = "[trigger]property_cert_number")
	@userfile("property_cert_photo", "property_cert_photo", uniqueidname = "property_cert_number")
	@sql("""
		insert into property_auth
		(user_id, name, identity_card_number, property_auth_number, property_auth_photo_url, authentication) 
		values(%s, %s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE 
		name=%s, identity_card_number=%s, property_auth_number=%s, property_auth_photo_url=%s, authentication=%s 
		""", 
		("self.userId", "self.certname", "self.idcardnumber", "self.property_cert_number", "self.property_cert_photo", 0,
		"self.certname", "self.idcardnumber", "self.property_cert_number", "self.property_cert_photo", 0))
	def execute(self):
		# self.property_cert_number = "123456"
		# self._saveFileFunc(**self._saveFileFuncParams[0])
		self.setResult([self.certname, self.idcardnumber, self.property_cert_number])

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
		self.setResult()

# TODO
# 修改房源照片，一次一张
class UpdateHousePhoto(BaseController):
	@checklogin()
	def execute(self):
		self.setResult()

# TODO
# 修改房源视频
class UpdateHouseVideo(BaseController):
	@checklogin()
	def execute(self):
		self.setResult()

# 下架房源
class PullOffHouse(BaseController):
	@checklogin()
	@queryparam("house_id", "string")
	@sql("update house_info set status=%s where id = %s and user_id = %s", (2, "self.house_id", "self.userId"))
	def execute(self):
		self.setResult()

# 删除房源
class DeleteHouse(BaseController):
	@checklogin()
	@queryparam("house_id", "string")
	@sql("update house_info set status=%s where id = %s and user_id = %s", (3, "self.house_id", "self.userId"))
	def execute(self):
		self.setResult()

# 创建房源
class HouseCreate(BaseController):
	@checklogin()
	# 省
	@queryparam("province_name", "string", optional = True, default = 0)
	@queryparam("province_code", "string", optional = True, default = 0)
	# 市
	@queryparam("city_name", "string", optional = True, default = 0)
	@queryparam("city_code", "string", optional = True, default = 0)
	# 区县
	@queryparam("county_name", "string", optional = True, default = 0)
	@queryparam("county_code", "string", optional = True, default = 0)
	# 小区
	@queryparam("district_name", "string", optional = True, default = 0)
	@queryparam("district_code", "string", optional = True, default = 0)
	# 门牌号
	@queryparam("house_number", "string", optional = True, default = 0)
	# 经纬度
	@queryparam("longitude", "string", optional = True, default = 255)
	@queryparam("latitude", "string", optional = True, default = 255)
	# 出租方式，长租2-短租1
	@queryparam("rent_time_type", "string", optional = True, default = 0)
	# 出租方式，整租1-单间2
	@queryparam("rent_room_type", "string", optional = True, default = 0)
	# 面积
	@queryparam("house_area", "string", optional = True, default = 0)
	# 户型
	@queryparam("house_type", "string", optional = True, default = 0)
	# 楼层
	@queryparam("house_floor", "string", optional = True, default = 0)
	# 朝向
	@queryparam("house_direction", "string", optional = True, default = 0)
	# 装修程度
	@queryparam("house_decoration", "string", optional = True, default = 0)
	# 最大居住人数
	@queryparam("house_max_livein", "string", optional = True, default = 0)
	# 租金
	@queryparam("house_rent", "string", optional = True, default = 0)
	# 付款方式, 1|3 押一付三, 2|6 押二付六, 1|0 无押金
	@queryparam("payment_type", "string", optional = True, default = "1|3")
	# 物业费, 1 房东, 2 租客, 3 待定
	@queryparam("property_management_fee", "string", optional = True, default = 0)
	# 取暖费
	@queryparam("heating_charge", "string", optional = True, default = 0)
	# 介绍标题
	@queryparam("description_title", "string", optional = True, default = "")
	# 特色介绍
	@queryparam("description", "string", optional = True, default = "")
	# 交通情况
	@queryparam("traffic_condition", "string", optional = True, default = "")
	# 周边情况
	@queryparam("around_condition", "string", optional = True, default = "")
	# 房屋设施
	# 1 空调, 2 暖气, 3 洗衣机, 4 冰箱, 5 允许宠物, 6 电视, 7 浴缸, 8 热水淋浴, 9 门禁系统, 10 有线网络, 11 电梯, 12 无线网络, 13 停车位, 14 饮水机
	# 1|2|3
	@queryparam("facility", "string", optional = True, default = 0)
	@sql(""" 
		insert ignore into house_info(user_id, province_name, province_code, city_name, city_code, county_name, county_code, district_name, district_code,
		house_number, longitude, latitude, rent_time_type, rent_room_type, house_size, house_type, house_floor, house_direction, house_decoration, 
		house_max_livein, house_rent, payment_type, property_management_fee, heating_charge, description_title, description, traffic_condition, 
		around_condition)
		values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		""", ("self.userId", "self.province_name", "self.province_code", "self.city_name", "self.city_code", "self.county_name", "self.county_code",
			"self.district_name", "self.district_code", "self.house_number", "self.longitude", "self.latitude", "self.rent_time_type",
			"self.rent_room_type", "self.house_area", "self.house_type", "self.house_floor", "self.house_direction", "self.house_decoration",
			"self.house_max_livein", "self.house_rent", "self.payment_type", "self.property_management_fee", "self.heating_charge",
			"self.description_title", "self.description", "self.traffic_condition", "self.around_condition"), holdon = True)
	def execute(self):
		facilityList = self.facility.strip().split("|")
		house_id = self.lastid
		for facility in facilityList:
			if facility != "":
				self.sqlServ.SQL("replace into house_facility(house_id, facility) values(%s, %s)", (house_id, facility), holdon = True)
		self.db.commit()
		self.setResult({"house_id": house_id})





