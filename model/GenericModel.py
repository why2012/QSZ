# coding: utf-8
from model.BaseModel import *

class GenericModel(BaseModel):
	def __init__(self, db, cursor):
		self.db = db
		self.cursor = cursor

	def SELECT_ONE(self, sqlString, sqlParams, attrmap):
		self.cursor.execute(sqlString, sqlParams)
		item = self.cursor.fetchone()
		resultMap = {}
		if item is not None:
			for index, attr in enumerate(attrmap):
				resultMap[attr] = item[index]
		return resultMap

	def SELECT(self, sqlString, sqlParams, attrmap):
		self.cursor.execute(sqlString, sqlParams)
		itemList = self.cursor.fetchall()
		resultList = []
		if itemList is not None:
			for item in itemList:
				resultMap = {}
				for index, attr in enumerate(attrmap):
					resultMap[attr] = item[index]
				resultList.append(resultMap)
		return resultList

	def UPDATE(self, sqlString, sqlParams):
		self.cursor.execute(sqlString, sqlParams)
		self.db.commit()
		return True

	def INSERT(self, sqlString, sqlParams):
		self.cursor.execute(sqlString, sqlParams)
		self.db.commit()
		return True