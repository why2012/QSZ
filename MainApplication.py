# coding: utf-8
import tornado.ioloop as ioloop
import tornado.web as web 
import logging.config
from UrlMapper import *
import Setting
import os
import platform

class MakeApp(object):

	def __init__(self):
		self.urlMapper = UrlMapper()

	def make(self):
		LOG_PATH = "./logs/tornado/"
		if "Windows" in platform.system():
			pass
		if not os.path.exists(LOG_PATH):
			os.mkdir(LOG_PATH)
		logging.config.fileConfig("conf/Logging.conf")
		return web.Application(self.urlMapper.getMapper(), **Setting.Conf)

if __name__ == "__main__":
	app = MakeApp().make()
	app.listen(20001)
	ioloop.IOLoop.current().start()