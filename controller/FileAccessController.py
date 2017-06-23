# coding: utf-8
from controller.BaseController import *

class FileAccessController(BaseController):
	def execute(self, filepath):
		if not (filepath.startswith("data")):
			raise Exception("Illegal path.")
		with open(filepath) as file:
			rawData = file.read()
			self.set_header('Content-Type', 'image/jpeg')
			self.write(rawData)
			self.flush()