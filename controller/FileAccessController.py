# coding: utf-8
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from controller.BaseController import *

class FileAccessController(BaseController):
	def execute(self, filepath):
		if not (filepath.startswith("data")):
			raise Exception("Illegal path.")
		with open(filepath) as file:
			rawData = file.read()
			if filepath.endswith("html") or filepath.endswith("htm"):
				self.set_header('Content-Type', 'text/html')
			elif filepath.endswith("css"):
				self.set_header('Content-Type', 'text/css')
			elif filepath.endswith("js"):
				self.set_header('Content-Type', 'application/x-javascript')
			else:
				self.set_header('Content-Type', 'image/jpeg')
			self.write(rawData)
			self.flush()