# coding: utf-8
import MySQLdb as mysql
from conf.Config import *
import warnings
reload(warnings).filterwarnings("ignore")

TABLE_USER_INFO = "user_info"; EXECUTE_CREATE_TABLE_USER_INFO = False#T
TABLE_PROPERTY_AUTH = "property_auth"; EXECUTE_CREATE_TABLE_PROPERTY_AUTH = False#T
TABLE_HOUSE_INFO = "house_info"; EXECUTE_CREATE_TABLE_HOUSE_INFO = False#T
TABLE_HOUSE_VIDEO = "house_video"; EXECUTE_CREATE_TABLE_HOUSE_VIDEO = False#T
TABLE_HOUSE_PHOTO = "house_photo"; EXECUTE_CREATE_TABLE_HOUSE_PHOTO = False#T
TABLE_PAYMENT = "user_payment"; EXECUTE_CREATE_TABLE_PAYMENT = False#T
TABLE_FACILITY = "house_facility"; EXECUTE_CREATE_TABLE_FACILITY = False#T
TABLE_COMMENT = "house_comment"; EXECUTE_CREATE_TABLE_COMMENT = False#T
TABLE_POSITION = "position"; EXECUTE_CREATE_TABLE_POSITION = False#T
TABLE_INVITE = "user_invite"; EXECUTE_CREATE_TABLE_INVITE = False#T
TABLE_PRE_ORDER = "pre_order_info"; EXECUTE_CREATE_TABLE_PRE_ORDER = True#T
TABLE_ORDER = "order_info"; EXECUTE_CREATE_TABLE_ORDER = False#T
TABLE_ORDER_PAYMENY = "order_payment"; EXECUTE_CREATE_TABLE_ORDER_PAYMENY = False#T
TABLE_COMPLAINT_REFUND = "complaint_refund"; EXECUTE_CREATE_TABLE_COMPLAINT_REFUND = False#T
TABLE_FINANCE_VIOLATION = "finance_violation"; EXECUTE_CREATE_TABLE_FINANCE_VIOLATION = False#T
TABLE_KEYVALUE_DATA = "keyvalue_data"; EXECUTE_CREATE_TABLE_KEYVALUE_DATA = True#T

CREATE_DATABASE = """ 
						CREATE DATABASE IF NOT EXISTS %s
				""" % db_config['db']

USE_DATABASE = """
						use %s
				""" % db_config['db']

CREATE_TABLE_USER_INFO = """
						CREATE TABLE IF NOT EXISTS %s (
							id INT UNSIGNED AUTO_INCREMENT,
							wx_openid VARCHAR(50),
							wx_unionid VARCHAR(50),
							wx_access_token VARCHAR(100),
							wx_nickname VARCHAR(100),
							wx_sex TINYINT UNSIGNED COMMENT '值为1时是男性，值为2时是女性，值为0时是未知',  
							wx_province VARCHAR(100),
							wx_city VARCHAR(100),
							wx_country VARCHAR(50),
							wx_headimgurl VARCHAR(150),
							headimgurl VARCHAR(150),
							wx_privilege TEXT,

							alipay_province VARCHAR(50) COMMENT '省份名称',
							alipay_city VARCHAR(50) COMMENT '市名称',
							alipay_gender TINYINT UNSIGNED COMMENT '值为1时是男性，值为2时是女性，值为0时是未知',  
							alipay_user_type_value VARCHAR(2) COMMENT '用户类型（1/2） 1代表公司账户2代表个人账户',
							alipay_user_status VARCHAR(2) COMMENT '用户状态（Q/T/B/W）. Q代表快速注册用户 T代表已认证用户 B代表被冻结账户 W代表已注册，未激活的账户',
							alipay_is_certified TINYINT UNSIGNED COMMENT '是否通过实名认证',
							alipay_is_student_certified TINYINT UNSIGNED COMMENT '是否是学生',
							alipay_user_id VARCHAR(50s) COMMENT '支付宝用户ID',
							alipay_user_access_token VARCHAR(60) COMMENT 'access token',
							alipay_user_auth_state VARCHAR(60) COMMENT '支付宝用户auth state',
							alipay_zhima_score VARCHAR(10) COMMENT '芝麻分',

							authentication TINYINT UNSIGNED COMMENT '0 未审核, 1 审核中, 2 审核完成, 3 审核失败',
							real_name VARCHAR(100),
							nickname VARCHAR(100) COMMENT '称呼',
							user_type TINYINT UNSIGNED COMMENT '1 房东, 2 二房东, 3 中介',  
							photo_url VARCHAR(150),
							identity_card_number VARCHAR(25),
							id_card_photo_front_url VARCHAR(150),
							id_card_photo_back_url VARCHAR(150),

							addressProvince VARCHAR(100) COMMENT '自填省份',
							addressCity VARCHAR(100) COMMENT '自填市区',
							birthday VARCHAR(100) COMMENT '自填生日',
							constellations VARCHAR(100) COMMENT '自填星座',
							education VARCHAR(100) COMMENT '自填教育背景',
							occupation VARCHAR(100) COMMENT '自填职业',
							tel VARCHAR(100) COMMENT '手机号',
							virtual_tel_flag TINYINT UNSIGNED COMMENT '是否使用400短号  仅限房东',
							virtual_tel VARCHAR(100) COMMENT '400短号  仅限房东',
							wechat VARCHAR(100) COMMENT '微信号',
							qq VARCHAR(100) COMMENT 'QQ号',


							zm_score INT DEFAULT -1 COMMENT '芝麻分',

							self_description TEXT,

							register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
							authentication_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

							PRIMARY KEY (id),
							UNIQUE wx_openid_index(wx_openid),
							INDEX wx_unionid_index(wx_unionid)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % TABLE_USER_INFO # 用户信息

CREATE_TABLE_PROPERTY_AUTH = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id INT UNSIGNED AUTO_INCREMENT,
							user_id INT UNSIGNED NOT NULL,
							name VARCHAR(100) COMMENT '房产证姓名',
							identity_card_number VARCHAR(25),
							property_auth_number VARCHAR(100),
							property_auth_photo_url VARCHAR(150),
							house_type VARCHAR(20) COMMENT '可选值： 1. 自有房屋出租， 2. 租赁房屋出租',
							lease_agreement_photo_url VARCHAR(150) COMMENT "租赁合同照片",
							authentication TINYINT UNSIGNED COMMENT '0 未审核, 1 审核中, 2 审核完成, 3 审核失败',

							PRIMARY KEY (id),
							UNIQUE property_auth_number_index(property_auth_number),
							CONSTRAINT property_auth_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_PROPERTY_AUTH, TABLE_USER_INFO) # 房产证信息

CREATE_TABLE_HOUSE_INFO = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							user_id INT UNSIGNED NOT NULL,
							rent_time_type TINYINT UNSIGNED COMMENT '1 短租, 2 长租',
							rent_room_type TINYINT UNSIGNED COMMENT '1 整租, 2 单间',
							status TINYINT UNSIGNED COMMENT '0: 创建, 1: 发布, 2: 下架, 3: 删除',
							province_code TINYINT UNSIGNED COMMENT '省份代码',
							province_name VARCHAR(100),
							city_code INT UNSIGNED COMMENT '城市代码',
							city_name VARCHAR(100),
							county_code INT UNSIGNED COMMENT '区县代码',
							county_name VARCHAR(100),
							district_code INT UNSIGNED COMMENT '小区代码',
							district_name VARCHAR(100),
							full_address TEXT,
							house_number VARCHAR(100) COMMENT '门牌号',
							longitude DECIMAL(10, 7),
							latitude DECIMAL(10, 7),

							house_size INT UNSIGNED COMMENT '房屋面积',
							house_type VARCHAR(100) COMMENT '户型',
							house_floor VARCHAR(100) COMMENT '楼层',
							house_direction VARCHAR(100) COMMENT '朝向',
							house_decoration VARCHAR(100) COMMENT '装修程度',
							house_max_livein TINYINT UNSIGNED COMMENT '最大居住人数',
							sex_restriction TINYINT UNSIGNED COMMENT '0 无要求, 1 男, 2 女',

							house_rooms INT UNSIGNED COMMENT '卧室数量',
							subdistrict_code INT UNSIGNED COMMENT '街道',
							subway_station_code INT UNSIGNED COMMENT '地铁站',
							house_characteristic TEXT COMMENT '房源特色',

							house_source INT UNSIGNED COMMENT '房源类型',
							all_floor INT UNSIGNED COMMENT '全部楼层',
							extra_fee VARCHAR(100) COMMENT '额外费用',
							release_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
							submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交审核时间',

							house_rent INT UNSIGNED COMMENT '租金',
							payment_type VARCHAR(10) COMMENT '付款方式, 1|3 押一付三, 2|6 押二付六, 1|0 无押金',

							property_management_fee TINYINT UNSIGNED COMMENT '物业费, 1 房东, 2 租客, 3 待定',
							electric_charge TINYINT UNSIGNED COMMENT '电费, 1 房东, 2 租客, 3 待定',
							heating_charge TINYINT UNSIGNED COMMENT '暖气费, 1 房东, 2 租客, 3 待定',

							description_title VARCHAR(300),
							description TEXT,
							traffic_condition TEXT,
							around_condition TEXT COMMENT '周边状况',

							praise_count INT UNSIGNED COMMENT '赞数',

							create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
							update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

							PRIMARY KEY (id),
							CONSTRAINT house_info_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id),
							INDEX province_code_index(province_code),
							INDEX city_code_index(city_code),
							INDEX county_code_index(county_code),
							INDEX district_code_index(district_code)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_HOUSE_INFO, TABLE_USER_INFO) # 房屋信息

CREATE_TABLE_HOUSE_VIDEO = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							house_id BIGINT UNSIGNED NOT NULL,
							user_id INT UNSIGNED NOT NULL,
							video_clip_url VARCHAR(150),

							PRIMARY KEY (id),
							CONSTRAINT house_video_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id),
							CONSTRAINT house_video_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_HOUSE_VIDEO, TABLE_HOUSE_INFO, TABLE_USER_INFO)

CREATE_TABLE_HOUSE_PHOTO = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							house_id BIGINT UNSIGNED,
							user_id INT UNSIGNED NOT NULL,
							photo_url VARCHAR(150),

							PRIMARY KEY (id),
							CONSTRAINT house_photo_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id),
							CONSTRAINT house_photo_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_HOUSE_PHOTO, TABLE_HOUSE_INFO, TABLE_USER_INFO)

CREATE_TABLE_PAYMENT = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							user_id INT UNSIGNED NOT NULL,
							type TINYINT UNSIGNED COMMENT '1 支付宝, 2 微信支付, 3 银行卡',
							account VARCHAR(100),
							account_name VARCHAR(200) COMMENT '收款账户对应姓名',
							account_idcardnumber VARCHAR(100) COMMENT '收款账户对应身份证号',

							PRIMARY KEY (id),
							UNIQUE INDEX payment_unique(user_id, type),
							CONSTRAINT payment_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_PAYMENT, TABLE_USER_INFO)

CREATE_TABLE_FACILITY = """ 
						CREATE TABLE IF NOT EXISTS %s (
							house_id BIGINT UNSIGNED NOT NULL,
							facility TINYINT UNSIGNED COMMENT '1 空调, 2 暖气, 3 洗衣机, 4 冰箱, 5 允许宠物, 6 电视, 7 浴缸, 8 热水淋浴, 9 门禁系统, 10 有线网络, 11 电梯, 12 无线网络, 13 停车位, 14 饮水机',

							PRIMARY KEY(house_id, facility),
							CONSTRAINT facility_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_FACILITY, TABLE_HOUSE_INFO)

CREATE_TABLE_COMMENT = """ 
						CREATE TABLE IF NOT EXISTS %s (
							house_id BIGINT UNSIGNED NOT NULL,
							user_id INT UNSIGNED NOT NULL,
							content TEXT,
							create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

							CONSTRAINT comment_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id),
							CONSTRAINT comment_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_COMMENT, TABLE_HOUSE_INFO, TABLE_USER_INFO)

CREATE_TABLE_POSITION = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id INT UNSIGNED AUTO_INCREMENT,
							type TINYINT UNSIGNED COMMENT '1 省, 2 市, 3 县/区, 4 小区',
							name VARCHAR(200),
							PRIMARY KEY (id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_POSITION)

CREATE_TABLE_INVITE = """ 
						CREATE TABLE IF NOT EXISTS %s (
							user_id INT UNSIGNED NOT NULL,
							my_invite_code VARCHAR(20) DEFAULT '00000000' COMMENT '0xid',
							friend_invite_code VARCHAR(20) DEFAULT '-1',
							PRIMARY KEY (user_id),
							CONSTRAINT invite_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id),
							INDEX my_invite_code_index(my_invite_code),
							INDEX friend_invite_code_index(friend_invite_code)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_INVITE, TABLE_USER_INFO)

CREATE_TABLE_PRE_ORDER = """
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							owner_id INT UNSIGNED NOT NULL,
							renter_id INT UNSIGNED NOT NULL,
							house_id BIGINT UNSIGNED NOT NULL,
							status TINYINT UNSIGNED COMMENT '1 租客提交, 2 支付完成, 3 完成看房, 4 投诉退款, 5 退款成功',
							create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
							update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

							PRIMARY KEY (id),
							UNIQUE INDEX owner_renter_house(owner_id, renter_id, house_id)
							CONSTRAINT pre_order_owner_user_info_fk FOREIGN KEY (owner_id) REFERENCES %s(id),
							CONSTRAINT pre_order_renter_user_info_fk FOREIGN KEY (renter_id) REFERENCES %s(id),
							CONSTRAINT pre_order_house_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_PRE_ORDER, TABLE_USER_INFO, TABLE_USER_INFO, TABLE_HOUSE_INFO)

CREATE_TABLE_ORDER = """
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							owner_id INT UNSIGNED NOT NULL,
							renter_id INT UNSIGNED NOT NULL,
							house_id BIGINT UNSIGNED NOT NULL,
							status TINYINT UNSIGNED COMMENT '1 租客提交, 2 房东确认, 3 支付完成, 4 确定入住, 5 投诉退款, 6 退款成功',
							create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
							update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

							PRIMARY KEY (id),
							CONSTRAINT order_owner_user_info_fk FOREIGN KEY (owner_id) REFERENCES %s(id),
							CONSTRAINT order_renter_user_info_fk FOREIGN KEY (renter_id) REFERENCES %s(id),
							CONSTRAINT order_house_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_ORDER, TABLE_USER_INFO, TABLE_USER_INFO, TABLE_HOUSE_INFO)

CREATE_TABLE_ORDER_PAYMENY = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							order_id BIGINT UNSIGNED NOT NULL,
							amount INT UNSIGNED NOT NULL COMMENT '金额',
							type TINYINT UNSIGNED COMMENT '1 支付宝, 2 微信支付',
							payer_id INT UNSIGNED NOT NULL,
							payee_id INT UNSIGNED NOT NULL,
							status TINYINT UNSIGNED COMMENT '1 创建, 2 完成支付, 3 退款完成',
							order_type TINYINT UNSIGNED COMMENT '1 看房红包订单, 2 租房订单',
							create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
							update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

							PRIMARY KEY (id),
							CONSTRAINT order_payment_payer_user_info_fk FOREIGN KEY (payer_id) REFERENCES %s(id),
							CONSTRAINT order_payment_payee_user_info_fk FOREIGN KEY (payee_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_ORDER_PAYMENY, TABLE_USER_INFO, TABLE_USER_INFO)

CREATE_TABLE_COMPLAINT_REFUND = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							user_id INT UNSIGNED NOT NULL,
							order_id BIGINT UNSIGNED NOT NULL,
							operation VARCHAR(200),
							type VARCHAR(200),
							content TEXT,
							status TINYINT UNSIGNED COMMENT '1 投诉提交, 2 处理中, 3 处理完成',
							create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
							update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

							PRIMARY KEY (id),
							CONSTRAINT complaint_refund_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id),
							CONSTRAINT complaint_refund_order_info_fk FOREIGN KEY (order_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_COMPLAINT_REFUND, TABLE_USER_INFO, TABLE_ORDER)

CREATE_TABLE_FINANCE_VIOLATION = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							user_id INT UNSIGNED NOT NULL,
							order_id BIGINT UNSIGNED NOT NULL,
							payment_id BIGINT UNSIGNED NOT NULL,
							amount INT UNSIGNED NOT NULL COMMENT '金额',
							status TINYINT UNSIGNED COMMENT '1 提交, 2 处理完成',
							create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
							update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

							PRIMARY KEY (id),
							CONSTRAINT finance_violation_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id),
							CONSTRAINT finance_violation_order_info_fk FOREIGN KEY (order_id) REFERENCES %s(id),
							CONSTRAINT finance_violation_order_payment_fk FOREIGN KEY (payment_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_FINANCE_VIOLATION, TABLE_USER_INFO, TABLE_ORDER, TABLE_ORDER_PAYMENY)

CREATE_TABLE_KEYVALUE_DATA = """
						CREATE TABLE IF NOT EXISTS %s (
							id INT UNSIGNED AUTO_INCREMENT,
							vkey VARCHAR(200),
							value TEXT,
							remark TEXT,
							remarkInt INT,

							PRIMARY KEY (id),
							UNIQUE vkey_unique_index(vkey)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % TABLE_KEYVALUE_DATA

def initDB():
	db, cursor = getDB()
	try:
		cursor.execute(CREATE_DATABASE)
		cursor.execute(USE_DATABASE)
		EXECUTE_CREATE_TABLE_USER_INFO and cursor.execute(CREATE_TABLE_USER_INFO) ; print TABLE_USER_INFO, "done."
		EXECUTE_CREATE_TABLE_PROPERTY_AUTH and cursor.execute(CREATE_TABLE_PROPERTY_AUTH) ; print TABLE_PROPERTY_AUTH, "done."
		EXECUTE_CREATE_TABLE_HOUSE_INFO and cursor.execute(CREATE_TABLE_HOUSE_INFO) ; print TABLE_HOUSE_INFO, "done."
		EXECUTE_CREATE_TABLE_HOUSE_VIDEO and cursor.execute(CREATE_TABLE_HOUSE_VIDEO) ; print TABLE_HOUSE_VIDEO, "done."
		EXECUTE_CREATE_TABLE_HOUSE_PHOTO and cursor.execute(CREATE_TABLE_HOUSE_PHOTO) ; print TABLE_HOUSE_PHOTO, "done."
		EXECUTE_CREATE_TABLE_PAYMENT and cursor.execute(CREATE_TABLE_PAYMENT) ; print TABLE_PAYMENT, "done."
		EXECUTE_CREATE_TABLE_FACILITY and cursor.execute(CREATE_TABLE_FACILITY) ; print TABLE_FACILITY, "done."
		EXECUTE_CREATE_TABLE_COMMENT and cursor.execute(CREATE_TABLE_COMMENT) ; print TABLE_COMMENT, "done."
		EXECUTE_CREATE_TABLE_POSITION and cursor.execute(CREATE_TABLE_POSITION) ; print TABLE_POSITION, "done."
		EXECUTE_CREATE_TABLE_INVITE and cursor.execute(CREATE_TABLE_INVITE) ; print TABLE_INVITE, "done."
		EXECUTE_CREATE_TABLE_PRE_ORDER and cursor.execute(CREATE_TABLE_PRE_ORDER) ; print TABLE_PRE_ORDER, "done."
		EXECUTE_CREATE_TABLE_ORDER and cursor.execute(CREATE_TABLE_ORDER) ; print TABLE_ORDER, "done."
		EXECUTE_CREATE_TABLE_ORDER_PAYMENY and cursor.execute(CREATE_TABLE_ORDER_PAYMENY) ; print TABLE_ORDER_PAYMENY, "done."
		EXECUTE_CREATE_TABLE_COMPLAINT_REFUND and cursor.execute(CREATE_TABLE_COMPLAINT_REFUND) ; print TABLE_COMPLAINT_REFUND, "done."
		EXECUTE_CREATE_TABLE_FINANCE_VIOLATION and cursor.execute(CREATE_TABLE_FINANCE_VIOLATION) ; print TABLE_FINANCE_VIOLATION, "done."
		EXECUTE_CREATE_TABLE_KEYVALUE_DATA and cursor.execute(CREATE_TABLE_KEYVALUE_DATA) ; print TABLE_KEYVALUE_DATA, "done."
		db.commit()
	except Exception, e:
		db.rollback()
		print "failed to create database." + str(e)

def getDB():
	db = mysql.connect(host = db_config["host"], user = db_config["user"], passwd = db_config["pwd"], charset = db_config["charset"], use_unicode = True)
	cursor = db.cursor()
	return db, cursor





