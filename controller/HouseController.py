# coding: utf-8
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from controller.BaseController import *
import dependency.qcloud_video as qcloud
import uuid
import time
import datetime

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

# 房东房源列表
class MyHouseList(BaseController):
	@checklogin()
	@sql("""select id, house_size, house_type, house_rent, payment_type, praise_count, status, create_date
		from house_info where user_id=%s""", ("self.userId",), "house_info")
	@checkparam("self.house_info", errMsg = "用户无房源", strict = True)
	def execute(self):
		for house_info in self.house_info:
			create_unixtime_dur = time.time() - time.mktime(house_info["create_date"].timetuple()) 
			house_info["create_date"] = house_info["create_date"].strftime("%Y-%d-%m")
			house_info["create_time_duration"] = int(create_unixtime_dur)
			house_id = house_info["id"]
			house_photo = self.sqlServ.SQL("""select id, photo_url from house_photo where house_id=%s""", (house_info['id'],))
			house_video = self.sqlServ.SQL("""select id, video_clip_url from house_video where house_id=%s""", (house_info['id'],))
			house_info["house_photo"] = house_photo
			house_info["house_video"] = house_video
		self.setResult(self.house_info)

# WARN
# 修改房源信息
class UpdateHouseInfo(BaseController):
	@checklogin()
	@queryparam("attr_name")
	@queryparam("attr_value")
	@queryparam("house_id")
	@sql("update house_info set %s=%s where id=%s",("self.attr_name", "self.attr_value", "self.house_id"))
	def execute(self):
		self.setResult()

# 添加房源照片，一次一张
class CreateHousePhoto(BaseController):
	@checklogin()
	@queryparam("house_id")
	@invoke("import uuid; self.uuid = str(uuid.uuid1());")
	#@checkparam("self.uuid", default = str(uuid.uuid1()))
	@userfile("house_photo", "house_photo", uniqueidname = "uuid")
	@sql("insert into house_photo(house_id, user_id, photo_url) values(%s, %s, %s)", ("self.house_id", "self.userId", "self.house_photo"))
	def execute(self):
		print self.uuid
		self.setResult({"id": self.lastid, "url": self.house_photo})

# 修改房源照片，一次一张
class UpdateHousePhoto(BaseController):
	@checklogin()
	@queryparam("photo_id")
	@invoke("import uuid; self.uuid = str(uuid.uuid1());")
	#@checkparam("self.uuid", default = str(uuid.uuid1()))
	@userfile("house_photo", "house_photo", uniqueidname = "uuid")
	@sql("select-one photo_url from house_photo where id = %s", ("self.photo_id",), "old_photo")
	@sql("update house_photo set photo_url = %s where id = %s", ("self.house_photo", "self.photo_id"))
	@invoke("""
		import os
		if os.path.exists(self.old_photo["photo_url"]) and os.path.isfile(self.old_photo["photo_url"]):
			os.remove(self.old_photo["photo_url"])
		""")
	def execute(self):
		self.setResult({"url": self.house_photo})

# todo: 修改房源视频
class CreateHouseVideo(BaseController):
	@checklogin()
	@queryparam("house_id")
	@userfile("house_video", "house_video")
	@sql("insert into house_video(house_id, user_id, video_clip_url) values(%s, %s, %s)", ("self.house_id", "self.userId", "self.house_video"))
	def execute(self):
		self.setResult({"id": self.lastid, "url": self.house_video})

# todo: 添加房源视频
class UpdateHouseVideo(BaseController):
	@checklogin()
	@queryparam("video_id")
	@userfile("house_video", "house_video")
	@sql("update house_video set video_clip_url = %s where id = %s", ("self.house_video", "self.video_id"))
	def execute(self):
		self.setResult({"url": self.house_video})

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
	@queryparam("house_size", "string", optional = True, default = 0)
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
		around_condition, status, praise_count)
		values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		""", ("self.userId", "self.province_name", "self.province_code", "self.city_name", "self.city_code", "self.county_name", "self.county_code",
			"self.district_name", "self.district_code", "self.house_number", "self.longitude", "self.latitude", "self.rent_time_type",
			"self.rent_room_type", "self.house_size", "self.house_type", "self.house_floor", "self.house_direction", "self.house_decoration",
			"self.house_max_livein", "self.house_rent", "self.payment_type", "self.property_management_fee", "self.heating_charge",
			"self.description_title", "self.description", "self.traffic_condition", "self.around_condition", 0, 0), holdon = True)
	@invoke("""
		facilityList = self.facility.strip().split("|")
		self.house_id = self.lastid
		for facility in facilityList:
			if facility != "":
				self.sqlServ.SQL("replace into house_facility(house_id, facility) values(%s, %s)", (self.house_id, facility), holdon = True)
		self.db.commit()
		""")
	def execute(self):
		self.setResult({"house_id": self.house_id})





