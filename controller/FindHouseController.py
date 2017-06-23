# coding: utf-8
from controller.BaseController import *

class SearchHouseByName(BaseController):
	@checklocation()
	def execute(self):
		return self._loc