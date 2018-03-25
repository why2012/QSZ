# coding: utf-8
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from controller.BaseController import *

class SearchHouseByName(BaseController):
	@checklocation()
	@queryparam("house_name", ptype = "string", optional = True)#房屋介绍标题
	@queryparam("house_type", ptype = "string", optional = True)#户型
	@queryparam("house_rent_time_type", ptype = "int", optional = True, default = -1)#类型，1 短租, 2 长租
	@queryparam("house_rent_room_type", ptype = "string", optional = True)#类型，1 整租, 2 单间,多个用 | 隔开
	@queryparam("house_rent_fee", ptype = "string", optional = True)#租金,[100, 500] [,800] [1000,]
	@queryparam("house_source", ptype = "string", optional = True)#来源，1 房东, 2 二房东, 3 中介,多个用 | 隔开
	@queryparam("house_size", ptype = "string", optional = True)#面积,[20, 50] [,100] [100,]
	@queryparam("house_direction", ptype = "string", optional = True)#朝向,多个用 | 隔开
	@queryparam("house_decoration", ptype = "string", optional = True)#装修情况,多个用 | 隔开
	@queryparam("radius", ptype = "int", optional = True, default = 10)#筛选距离半径, km
	@queryparam("shift", ptype = "int", optional = True, default = 0)#筛选偏移
	@queryparam("count", ptype = "int", optional = True, default = 1000)#筛选数目
	@queryparam("sort", ptype = "int", optional = True, default = 1)#排序，1 距离升，2 时间降，3 关注度降，4 租金升， 5 租金降 6 面积升
	
	@queryparam("house_rooms", ptype = "string", optional = True)#卧室数量,多个用 | 隔开
	@queryparam("subdistrict_code", ptype = "int", optional = True, default = -1)#按街道筛选
	@queryparam("subway_station_code", ptype = "int", optional = True, default = -1)#按地铁站筛选
	@queryparam("house_characteristic", ptype = "string", optional = True)#卧室数量,多个用 | 隔开

	@service("GenericSqlService", "sqlServ", targetObj = "self")
	def execute(self):
		sqlstring = "select house_info.id as id, house_size, house_type, house_rent, payment_type, praise_count, house_info.status as status, house_info.create_date as create_date, user_type, [(%s)] as distance from house_info inner join user_info on house_info.user_id=user_info.id where (%s)<=%s"
		a = "(%s * pi() / 180 - latitude * pi() / 180)" % self._loc["latitude"]
		b = "(%s * pi() / 180 - longitude * pi() / 180)" % self._loc["longitude"]
		sqldistance = " (2 * asin(sqrt( pow(sin({a} / 2), 2) + cos({lat} * pi() / 180) * cos(latitude * pi() / 180) * pow(sin({b} / 2), 2) )) * 6378.137) "
		sqldistance = sqldistance.format(a = a, b = b, lat = self._loc["latitude"])
		sqlstring = sqlstring % (sqldistance, sqldistance, self.radius)
		sqlstring += " and"
		queryparams = []
		if self.house_name != "":
			sqlstring += " description_title like %s and"
			queryparams.append("%" + self.house_name + "%")
		if self.house_type != "":
			sqlstring += " house_type like %s and"
			queryparams.append("%" + self.house_type + "%")
		if self.house_rent_time_type != -1:
			sqlstring += " house_rent_time_type=%s and"
			queryparams.append(self.house_rent_time_type)
		if self.house_rent_room_type != "":
			house_rent_room_type_list = self.house_rent_room_type.strip().split('|')
			if len(house_rent_room_type_list) == 1:
				sqlstring += " rent_room_type=%s and"
			else:
				sqlstring += "("
				for i, house_rent_room_type in enumerate(house_rent_room_type_list):
					sqlstring += " rent_room_type=%s "
					if i != len(house_rent_room_type_list) - 1:
						sqlstring += " or "
				sqlstring += ") and"
			queryparams.extend(house_rent_room_type_list)
		if self.house_rent_fee != "":
			lowValue, highValue = self.parseInterval(self.house_rent_fee)
			sqlstring += " house_rent>=%s and house_rent<=%s"
			queryparams.append(lowValue)
			queryparams.append(highValue)
		if self.house_source != "":
			house_source_list = self.house_source.strip().split('|')
			if len(house_source_list) == 1:
				sqlstring += " user_type=%s and"
			else:
				sqlstring += "("
				for i, house_source in enumerate(house_source_list):
					sqlstring += " user_type=%s "
					if i != len(house_source_list) - 1:
						sqlstring += " or "
				sqlstring += ") and"
			queryparams.extend(house_source_list)
		if self.house_size != "":
			lowValue, highValue = self.parseInterval(self.house_size)
			sqlstring += " house_size>=%s and house_size<=%s"
			queryparams.append(lowValue)
			queryparams.append(highValue)
		if self.house_direction != "":
			house_direction_list = self.house_direction.strip().split('|')
			if len(house_direction_list) == 1:
				sqlstring += " house_direction like %s and"
			else:
				sqlstring += "("
				for i, house_direction in enumerate(house_direction_list):
					sqlstring += " house_direction like %s "
					if i != len(house_direction_list) - 1:
						sqlstring += " or "
				sqlstring += ") and"
			queryparams.extend(house_direction_list)
		if self.house_decoration != "":
			house_decoration_list = self.house_decoration.strip().split('|')
			if len(house_decoration_list) == 1:
				sqlstring += " house_decoration like %s and"
			else:
				sqlstring += "("
				for i, house_decoration in enumerate(house_decoration_list):
					sqlstring += " house_decoration like %s "
					if i != len(house_decoration_list) - 1:
						sqlstring += " or "
				sqlstring += ") and"
			queryparams.extend(house_decoration_list)
		if self.house_rooms != "":
			house_rooms_list = self.house_rooms.strip().split('|')
			if len(house_rooms_list) == 1:
				sqlstring += " house_rooms = %s and"
			else:
				sqlstring += "("
				for i, house_rooms in enumerate(house_rooms_list):
					sqlstring += " house_rooms = %s "
					if i != len(house_rooms_list) - 1:
						sqlstring += " or "
				sqlstring += ") and"
			queryparams.extend(house_rooms_list)
		if self.house_characteristic != "":
			house_characteristic_list = self.house_characteristic.strip().split('|')
			if len(house_characteristic_list) == 1:
				sqlstring += " house_characteristic like %s and"
			else:
				sqlstring += "("
				for i, house_characteristic in enumerate(house_characteristic_list):
					sqlstring += " house_characteristic like %s "
					if i != len(house_characteristic_list) - 1:
						sqlstring += " or "
				sqlstring += ") and"
			queryparams.extend(house_characteristic_list)
		if self.subdistrict_code != -1:
			sqlstring += " subdistrict_code=%s and"
			queryparams.append(self.subdistrict_code)
		if self.subway_station_code != -1:
			sqlstring += " subway_station_code=%s and"
			queryparams.append(self.subway_station_code)

		sqlstring += " status=1"

		if sqlstring.endswith("and"):
			sqlstring = sqlstring[:-3]

		if self.sort != -1:
			orderstring = " order by"
			if self.sort == 1:
				orderstring += " distance asc,"
			elif self.sort == 2:#时间降
				orderstring += " house_info.create_date desc,"
			elif self.sort == 3:#关注度降
				orderstring += " praise_count desc,"
			elif self.sort == 4:#租金升
				orderstring += " house_rent asc,"
			elif self.sort == 5:#租金降
				orderstring += " house_rent desc,"
			elif self.sort == 6:#面积升
				orderstring += " house_size asc,"

			if orderstring.endswith(","):
				orderstring = orderstring[:-1]
			sqlstring += orderstring

		sqlstring += " limit %s, %s" % (self.shift, self.count)
		queryresult = self.sqlServ.SQL(sqlstring, queryparams)
		for item in queryresult:
			house_id = item["id"]
			del item["id"]
			item["house_id"] = house_id
			if item["create_date"]:
				item["duration"] = int(time.time() - time.mktime(item["create_date"].timetuple()))
				item["create_date"] = item["create_date"].strftime("%Y-%d-%m")
			photos_data = self.sqlServ.SQL("select photo_url from house_photo where house_id=%s", (house_id, ))
			photos = []
			for photos_data_item in photos_data:
				photos.append(photos_data_item["photo_url"])
			item["photos"] = photos
			
		return queryresult
		#return sqlstring

	def parseInterval(self, intervalStr):
		lowValue = 0
		highValue = 0
		intervalStr = intervalStr.strip()
		try:
			if intervalStr.startswith("[") and intervalStr.endswith("]"):
				intervalStr = intervalStr[1:][:-1]
				lowValue, highValue = intervalStr.split(",")
				if lowValue .strip() == "":
					lowValue = -1
				if highValue .strip() == "":
					highValue = -1
				lowValue = int(lowValue)
				highValue = int(highValue)
		except:
			lowValue = highValue = 0
		finally:
			return (lowValue, highValue)



