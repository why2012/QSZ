# coding: utf-8
import tornado.httpserver as httpserver
import tornado.ioloop as ioloop
import tornado.web as web 
import logging.config
from UrlMapper import *
#from conf.Config import *
import Setting
import os
import platform
import argparse
#import warnings
#warnings.filterwarnings("ignore")

class MakeApp(object):

	def __init__(self):
		self.urlMapper = UrlMapper()

	def make(self):
		LOG_PATH = "./logs/tornado/"
		if "Windows" in platform.system():
			pass
		if not os.path.exists(LOG_PATH):
			os.makedirs(LOG_PATH)
		logging.config.fileConfig("conf/Logging.conf")
		webApplication = web.Application(self.urlMapper.getMapper(), **Setting.Conf)
		UtilConfig["WebApplication"] = webApplication
		return webApplication

def initDatabase():
	print "init database."
	from util.InitializeDatabase import initDB
	initDB()
	print "done."

def startupServer():
	app = MakeApp().make()
	if Setting.Conf["debug"]:
		app.listen(20001)
		ioloop.IOLoop.current().start()
	else:
		httpServer = httpserver.HTTPServer(app)
		httpServer.bind(20001)
		httpServer.start(num_processes = 0) 
		ioloop.IOLoop.current().start()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', help = 'initdb or startup', default = "startup")
	args = parser.parse_args()
	mode = args.mode.lower()
	if mode == 'initdb':
		initDatabase()
	elif mode == 'startup':
		startupServer()
	else:
		parser.print_help()