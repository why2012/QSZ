# coding: utf-8
from service.BaseService import *
from model.GenericModel import GenericModel

class GenericSqlService(BaseService):
	def __init__(self, db, cursor, targetObj):
		self.genericModel = GenericModel(db, cursor)
		self.targetObj = targetObj
		
	def reinit(self):
		self.attrmap = []
		self.select_one = False;

	# scopeType: object|array
	def SQL(self, sqlString, sqlParams, scope = "sqlResult", scopeType = "array", affectId = "lastid", holdon = False):
		self.reinit()
		sqlString = self.preProcess(sqlString)
		sqlTokenList = sqlString.strip().replace('\n', ' ').replace('\t', ' ').split(" ")
		sqlTokenList = filter(lambda t: t.strip() != "", sqlTokenList)
		originalSqlTokenList = sqlTokenList
		sqlTokenList = map(lambda t: t.upper(), sqlTokenList)
		sqlTokenList, originalSqlTokenList = self.preProcessTokenList(sqlTokenList, originalSqlTokenList)
		self.parseSqlTokens(sqlTokenList, originalSqlTokenList)
		# print sqlTokenList
		if sqlTokenList[0] == "SELECT":
			if sqlTokenList[1] == "*":
				raise Exception("Unsupport oprand: %s after SELECT" % sqlTokenList[1])
			if not self.select_one: 
				selectResult = self.genericModel.SELECT(" ".join(originalSqlTokenList), sqlParams, self.attrmap)
			else:
				selectResult = self.genericModel.SELECT_ONE(" ".join(originalSqlTokenList), sqlParams, self.attrmap)
			if self.targetObj is not None:
				if scopeType.lower() == "array":
					if not hasattr(self.targetObj, scope):
						setattr(self.targetObj, scope, [])
					sqlResult = getattr(self.targetObj, scope)
					sqlResult.append(selectResult)
				else:
					setattr(self.targetObj, scope, selectResult)
			return selectResult
		elif sqlTokenList[0] == "UPDATE":
			updateResult = self.genericModel.UPDATE(" ".join(originalSqlTokenList), sqlParams, holdon)
			return updateResult
		elif sqlTokenList[0] == "INSERT" or sqlTokenList[0] == "REPLACE":
			insertResult = self.genericModel.INSERT(" ".join(originalSqlTokenList), sqlParams, holdon)
			setattr(self.targetObj, affectId, insertResult)
			return insertResult
		elif sqlTokenList[0] == "DELETE":
			deleteResult = self.genericModel.DELETE(" ".join(originalSqlTokenList), sqlParams, holdon)
			return deleteResult
		else:
			raise Exception("Illegal sql token: " + sqlTokenList[0])

	# 处理操作符粘连问题
	def preProcess(self, sqlString):
		sqlCharList = []
		for s in sqlString:
			if s == ",":
				sqlCharList.append(" ")
				sqlCharList.append(s)
				sqlCharList.append(" ")
				continue
			sqlCharList.append(s)
		return "".join(sqlCharList)

	# 自定义token处理
	def preProcessTokenList(self, sqlTokenList, originalSqlTokenList):
		_sqlTokenList = []
		_originalSqlTokenList = []
		for index, token in enumerate(sqlTokenList):
			_token = originalSqlTokenList[index]
			if token == "SELECT-ONE":
				self.select_one = True
				token = "SELECT"
				_token = "SELECT"
			_sqlTokenList.append(token)
			_originalSqlTokenList.append(_token)
		return _sqlTokenList, _originalSqlTokenList

	def parseSqlTokens(self, sqlTokenList, originalSqlTokenList):
		tokenTypeMap = {"SELECT": 1, "UPDATE": 2, "INSERT": 3, "OTHER": 4}
		sqlStatusMap = {"START": 0, "AFTER_FIRST_OPRAND": 1, "AFTER_FROM": 2};
		token_type = tokenTypeMap["OTHER"]
		local_sql_status = sqlStatusMap["START"]
		local_sql_vars = {}
		for index, token in enumerate(sqlTokenList):

			if local_sql_status == sqlStatusMap["START"]:
				local_sql_status = sqlStatusMap["AFTER_FIRST_OPRAND"]
				if token == "SELECT":
					token_type = tokenTypeMap["SELECT"]
				elif token == "UPDATE":
					token_type = tokenTypeMap["UPDATE"]
				elif token == "INSERT":
					token_type = tokenTypeMap["INSERT"]
				else:
					token_type = tokenTypeMap["OTHER"]
				continue
			if local_sql_status == sqlStatusMap["AFTER_FIRST_OPRAND"]:
				if token == "FROM":
					if token_type == tokenTypeMap["SELECT"]:
						self.retrieveAttrMap(index, token, local_sql_vars, sqlTokenList, originalSqlTokenList)
					local_sql_status = sqlStatusMap["AFTER_FROM"]
					continue
				if token_type == tokenTypeMap["SELECT"]:
					if token == ",":
						self.retrieveAttrMap(index,token, local_sql_vars, sqlTokenList, originalSqlTokenList)
						local_sql_vars["last_comma_index"] = index
						continue
					if token == "AS":
						local_sql_vars["last_as_index"] = index
						continue

	# 获取sql字段名
	def retrieveAttrMap(self, index, token, local_sql_vars, sqlTokenList, originalSqlTokenList):
		if "last_comma_index" in local_sql_vars:
			last_comma_index = local_sql_vars["last_comma_index"]
		else:
			last_comma_index = -1
		if "last_as_index" in local_sql_vars:
			last_as_index = local_sql_vars["last_as_index"]
		else:
			last_as_index = -1
		last_split_index = last_comma_index
		if last_as_index != -1 and last_as_index > last_comma_index:
			last_split_index = last_as_index
		if last_split_index == -1:
			self.attrmap.append(" ".join(originalSqlTokenList[1: index]))
		else:
			self.attrmap.append(" ".join(originalSqlTokenList[last_split_index + 1: index]))
















