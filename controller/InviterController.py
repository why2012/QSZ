# coding: utf-8
from controller.BaseController import *

#获取邀请码
class GetInvitationCode(BaseController):
	@checklogin()
	@sql("select-one my_invite_code, friend_invite_code from user_invite where user_id=%s", ("self.userId",), "inviteInfo")
	def execute(self):
		resultData = {"my_invite_code": -1, "friend_invite_code": -1}
		mycode = "%08x" % int(self.userId)
		invitecode = -1;
		if self.inviteInfo is None or len(self.inviteInfo) == 0:
			self.sqlServ.SQL("insert ignore into user_invite(user_id, my_invite_code) values(%s, %s)", (self.userId, mycode))
		elif self.inviteInfo["my_invite_code"] == "00000000":
			self.sqlServ.SQL("update user_invite set my_invite_code=%s where user_id=%s", (mycode, self.userId))
		if self.inviteInfo is not None and len(self.inviteInfo) != 0 and self.inviteInfo["friend_invite_code"] != "-1":
			invitecode = self.inviteInfo["friend_invite_code"]
		resultData["my_invite_code"] = mycode
		resultData["friend_invite_code"] = invitecode
		return resultData

#填写邀请码
class SetInvitationCode(BaseController):
	@checklogin()
	@queryparam("invite_code")
	@invoke("self.invite_code = self.invite_code.upper()")
	@sql("select-one my_invite_code, friend_invite_code from user_invite where user_id=%s", ("self.userId",), "inviteInfo")
	def execute(self):
		mycode = "%08x" % int(self.userId)
		if self.inviteInfo is None or len(self.inviteInfo) == 0:
			self.sqlServ.SQL("insert ignore into user_invite(user_id, my_invite_code, friend_invite_code) values(%s, %s, %s)", (self.userId, mycode, self.invite_code))
		elif self.inviteInfo["friend_invite_code"] == "-1":
			self.sqlServ.SQL("update user_invite set friend_invite_code=%s where user_id=%s", (self.invite_code, self.userId))
		else:
			raise Exception("不要重复填写邀请码", STATUS_PARAM_ERROR)
		return {"my_invite_code": mycode, "friend_invite_code": self.invite_code}
