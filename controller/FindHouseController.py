# coding: utf-8
from controller.BaseController import *

class SearchHouseByName(BaseController):
	@checklocation()
	@queryparam("house_name", ptype = "string", optional = True)#房屋介绍标题
	@queryparam("house_type", ptype = "string", optional = True)#户型
	@queryparam("house_rent_time_type", ptype = "int", optional = True)#类型，1 短租, 2 长租
	@queryparam("house_rent_room_type", ptype = "int", optional = True)#类型，1 整租, 2 单间
	@queryparam("house_rent_fee", ptype = "int", optional = True)#租金,[100, 500] [,800] [1000,]
	@queryparam("house_source", ptype = "int", optional = True)#来源，1 房东, 2 二房东, 3 中介
	@queryparam("house_size", ptype = "int", optional = True)#面积,[20, 50] [,100] [100,]
	@queryparam("house_direction", ptype = "string", optional = True)#朝向
	@queryparam("house_decoration", ptype = "string", optional = True)#朝向
	@queryparam("sort", ptype = "int", optional = True, default = 1)#排序，1 距离升，2 时间升，3 关注度降，4 租金升， 5 租金降 6 面积升
	@service("GenericSqlService", "sqlServ")
	def execute(self):
		sqlstring = "select house_info.id as id, house_size, house_type, house_rent, payment_type, praise_count, house_info.status as status, house_info.create_date as create_date, user_type from house_info inner join user_info on house_info.user_id=user_info.id where"
		queryparams = []
		if self.house_name is not None:
			sqlstring += " description_title like %%%s%% and"
			queryparams.append(self.house_name)
		if self.house_type is not None:
			sqlstring += " house_type like %%%s%% and"
			queryparams.append(self.house_type)
		if self.house_rent_time_type is not None:
			sqlstring += " house_rent_time_type=%s and"
			queryparams.append(self.house_rent_time_type)
		if self.house_rent_room_type is not None:
			sqlstring += " house_rent_room_type=%s and"
			queryparams.append(self.house_rent_room_type)
		if self.house_rent_fee is not None:

			sqlstring += " house_rent=%s and"
			queryparams.append(self.house_rent_fee)
		if self.house_source is not None:
			sqlstring += " user_type=%s and"
			queryparams.append(self.house_source)
		if self.house_size is not None:

			sqlstring += " house_size=%s and"
			queryparams.append(self.house_size)
		if self.house_direction is not None:
			sqlstring += " house_direction like %%%s%% and"
			queryparams.append(self.house_direction)
		if self.house_decoration is not None:
			sqlstring += " house_decoration like %%%s%% and"
			queryparams.append(self.house_decoration)

		if sqlstring.endswith("and"):
			sqlstring = sqlstring[:-3]

		if self.sort is not None:
			if self.sort == 1:
				pass
			elif self.sort == 2:
				pass
			elif self.sort == 3:
				pass
			elif self.sort == 4:
				pass
			elif self.sort == 5:
				pass
			elif self.sort == 6:
				pass

		queryresult = self.sqlServ.SQL(sqlstring, queryparams)
		return queryresult




