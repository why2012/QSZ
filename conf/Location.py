# coding: utf-8
from math import asin, sin, cos, pow, sqrt, radians

# 默认东经，北纬, 半径单位km
# level 1 省 2 市 3 区县
city_code = {
	"100": {},
	"100010": {"name": "四川", "code": 10, "parentCode": "1", "level": 1, "abbr": "sc", "longitude": 104, "latitude": 30, "radius": 500},
	"100010001": {"name": "成都", "code": 100010001, "parentCode": "100010", "level": 2, "abbr": "cd", "longitude": 104.06, "latitude": 30.67, "radius": 30},
}

def loc_distance(longA, latA, longB, latB):
	a = float(radians(latA) - radians(latB))
	b = float(radians(longA) - radians(longB))
	S = 2 * asin(sqrt( pow(sin(a / 2), 2) + cos(latA) * cos(latB) * pow(sin(b / 2), 2) )) * 6378.137
	return S

def loc_distance_obj(objA, objB):
	return loc_distance(objA["longitude"], objA["latitude"], objB["longitude"], objB["latitude"])

def findCityByLL(longi, lati):
	resultCity = None;
	level = 1
	for city in city_code.values():
		if len(city) == 0:
			continue
		dis = loc_distance_obj(dict(longitude = longi, latitude = lati), city)
		if city["level"] >= level and dis <= city["radius"]:
			if resultCity is None:
				resultCity = city
				resultCity["dis"] = dis
				level = city["level"]
				continue
			if resultCity["level"] == city["level"]:
				if dis < resultCity["dis"]:
					resultCity = city
					resultCity["dis"] = dis
					level = city["level"]
			elif resultCity["level"] < city["level"]:
				resultCity = city
				resultCity["dis"] = dis
				level = city["level"]
	if resultCity is not None:
		del resultCity['dis']
	return resultCity