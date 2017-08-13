# coding: utf-8
import importlib
from util.Exceptions import *
from util.ErrorCode import *
from conf.Config import *

def checklocation():
	def method_process(op):
		def get_param(self, *args, **kwargs):
			longitude = self.getFloatArg("longitude", None)
			latitude = self.getFloatArg("latitude", None)
			city = self.getIntArg("loccity", None)
			if str(city) in city_code:
				city = city_code[str(city)]
			else:
				city = None
			if (longitude is None or latitude is None) and city is None:
				raise Exception("Location unconfirmed.")
			if longitude is not None and latitude is not None:
				ll_city = findCityByLL(longitude, latitude)
			if city is None:
				city = ll_city
			if (longitude is None or latitude is None) and city is not None:
				longitude = city["longitude"]
				latitude = city["latitude"]
			self._loc = {"longitude": longitude, "latitude": latitude, "city": city}
			_fresult = op(self, *args, **kwargs)
			return _fresult
		return get_param
	return method_process