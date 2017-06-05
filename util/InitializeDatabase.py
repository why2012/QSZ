# coding: utf-8
import MySQLdb as mysql
from conf.Config import *
import warnings
reload(warnings).filterwarnings("ignore")

TABLE_USER_INFO = "user_info"
TABLE_PROPERTY_AUTH = "property_auth"
TABLE_HOUSE_INFO = "house_info"
TABLE_HOUSE_VIDEO = "house_video"
TABLE_HOUSE_PHOTO = "house_photo"
TABLE_PAYMENT = "user_payment"
TABLE_FACILITY = "house_facility"
TABLE_COMMENT = "house_comment"
TABLE_POSITION = "position"
TABLE_INVITE = "user_invite"

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
							wx_privilege TEXT,

							authentication TINYINT UNSIGNED COMMENT '0 未审核, 1 审核中, 2 审核完成, 3 审核失败',
							real_name VARCHAR(100),
							photo_url VARCHAR(150),
							identity_card_number VARCHAR(25),
							id_card_photo_front_url VARCHAR(150),
							id_card_photo_back_url VARCHAR(150),

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
							user_id INT UNSIGNED,
							name VARCHAR(100),
							identity_card_number VARCHAR(25),
							property_auth_number VARCHAR(100),
							property_auth_photo_url VARCHAR(150),

							PRIMARY KEY (id),
							CONSTRAINT property_auth_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_PROPERTY_AUTH, TABLE_USER_INFO) # 房产证信息

CREATE_TABLE_HOUSE_INFO = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							user_id INT UNSIGNED,
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

							house_rent INT UNSIGNED COMMENT '租金',
							payment_type VARCHAR(100) COMMENT '付款方式',

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
							INDEX county_code_index(county_code)
							INDEX district_code_index(district_code)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_HOUSE_INFO, TABLE_USER_INFO) # 房屋信息

CREATE_TABLE_HOUSE_VIDEO = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							house_id BIGINT UNSIGNED,
							user_id INT UNSIGNED,
							video_clip_url VARCHAR(150),

							PRIMARY KEY (id),
							CONSTRAINT house_video_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id),
							CONSTRAINT house_video_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id),
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_HOUSE_VIDEO, TABLE_HOUSE_INFO, TABLE_USER_INFO)

CREATE_TABLE_HOUSE_PHOTO = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							house_id BIGINT UNSIGNED,
							user_id INT UNSIGNED,
							photo_url VARCHAR(150),

							PRIMARY KEY (id),
							CONSTRAINT house_photo_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id),
							CONSTRAINT house_photo_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id),
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_HOUSE_PHOTO, TABLE_HOUSE_INFO, TABLE_USER_INFO)

CREATE_TABLE_PAYMENT = """ 
						CREATE TABLE IF NOT EXISTS %s (
							id BIGINT UNSIGNED AUTO_INCREMENT,
							user_id INT UNSIGNED,
							type TINYINT UNSIGNED COMMENT '1 支付宝, 2 微信支付',
							account VARCHAR(100),

							PRIMARY KEY (id),
							CONSTRAINT payment_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id),
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_PAYMENT, TABLE_USER_INFO)

CREATE_TABLE_FACILITY = """ 
						CREATE TABLE IF NOT EXISTS %s (
							house_id BIGINT UNSIGNED,
							facility TINYINT UNSIGNED COMMENT '1 空调, 2 暖气, 3 洗衣机, 4 冰箱, 5 允许宠物, 6 电视, 7 浴缸, 8 热水淋浴, 9 门禁系统, 10 有线网络, 11 电梯, 12 无线网络, 13 停车位, 14 饮水机',

							CONSTRAINT facility_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id),
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_FACILITY, TABLE_HOUSE_INFO)

CREATE_TABLE_COMMENT = """ 
						CREATE TABLE IF NOT EXISTS %s (
							house_id BIGINT UNSIGNED,
							user_id INT UNSIGNED,
							content TEXT,

							CONSTRAINT comment_house_info_fk FOREIGN KEY (house_id) REFERENCES %s(id),
							CONSTRAINT comment_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id),
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
							id INT UNSIGNED AUTO_INCREMENT,
							user_id INT UNSIGNED,
							my_invite_code VARCHAR(20) DEFAULT '-1' COMMENT '0xid',
							friend_invite_code VARCHAR(20) DEFAULT '-1',
							PRIMARY KEY (id)
							CONSTRAINT invite_user_info_fk FOREIGN KEY (user_id) REFERENCES %s(id),
							INDEX my_invite_code_index(my_invite_code),
							INDEX friend_invite_code_index(friend_invite_code)
						)ENGINE=InnoDB DEFAULT CHARSET=utf8;
				""" % (TABLE_INVITE, TABLE_USER_INFO)

def initDB():
	db, cursor = getDB()
	try:
		cursor.execute(CREATE_DATABASE)
		cursor.execute(USE_DATABASE)
		cursor.execute(CREATE_TABLE_USER_INFO)
		cursor.execute(CREATE_TABLE_PROPERTY_AUTH)
		cursor.execute(CREATE_TABLE_HOUSE_INFO)
		cursor.execute(CREATE_TABLE_HOUSE_VIDEO)
		cursor.execute(CREATE_TABLE_HOUSE_PHOTO)
		cursor.execute(CREATE_TABLE_PAYMENT)
		cursor.execute(CREATE_TABLE_FACILITY)
		cursor.execute(CREATE_TABLE_COMMENT)
		db.commit()
	except Exception, e:
		db.rollback()
		print "failed to create database." + str(e)

def getDB():
	db = mysql.connect(host = db_config["host"], user = db_config["user"], passwd = db_config["pwd"], charset = db_config["charset"], use_unicode = True)
	cursor = db.cursor()
	return db, cursor





