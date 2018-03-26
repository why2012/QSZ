### 通过openid获取用户信息
地址: /wx_fetch_userinfo

方法: get

参数
```
openid: string # 用户的微信id，通过微信公众号获取
```

HTTP HEADER
```
```

返回
```
{
    "status": 0,
    "msg": "",
    "ans": {
        "qq": "22222",
        "headimgurl": null,
        "wx_nickname": "Band",
        "wx_city": "广州",
        "virtual_tel_flag": 1,
        "constellations": "呵呵",
        "wx_sex": 1,
        "birthday": "1999-11-11",
        "wechat": "1111111",
        "addressProvince": "sichuan",
        "wx_headimgurl": "data/userphoto/user_6/portrait.jpg",
        "wx_country": "中国",
        "id": 6, # user id
        "addressCity": "chengdu",
        "occupation": "搬砖工",
        "virtual_tel": "1111",
        "education": "小学",
        "wx_province": "广东",
        "token": "a703bd25f111842c77b359d49a2fc5414b9036dccb872f04d3359ec677b5c7c1", # 放置于http header中，登陆
        "wx_openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M"
    }
}
```

### 用户信息录入
地址: /create_userinfo

方法: post

参数
```
nickname: string # 称呼
sex: number # 性别 1 男， 2 女，0 未知
user_type: number # 用户类型, 1 房东, 2 二房东, 3 中介
self_description: string # 介绍
portrait: file # 头像

addressProvince: string: # 所在地区
addressCity: string # 所在地区
birthday: string  #  生日, 格式 0000-00-00
constellations: string  # 星座
education: string  #  教育背景。可选值：['博士', '硕士', '本科', '大专', '中专', '高中', '初中']
occupation: string  #  职业

//  收款账户相关，用户提现时需要用到，包括邀请收入，房租收入，服务费分成。
[account_name: string] # 收款账户对应姓名
[account_number: string] # 收款账户账号
[account_idcardnumber: string] # 收款账户对应身份证号
//  联系方式
[tel: string] # 手机号
[virtual_tel_flag: Boolean] # 是否使用400短号  仅限房东
[virtual_tel: string] # 400短号  仅限房东
[wechat: string] # 微信号
[qq: string] # QQ号
```

HTTP HEADER
```
token
```

返回
```
{
  "status": 0, # 状态为0表示成功
  "msg": "",
  "ans": {}
}
```

### 实名认证
地址: /user_identification

方法: post

参数
```
realname: string
idcardnumber: string
portrait: file # 头像
idcardfront: file # 身份证正面
idcardback: file # 身份证反面
```

HTTP HEADER
```
token
```

返回
```

{
    "ans": [
        "李先生", # 姓名
        "513812188722874655" # 身份证号
    ],
    "status": 0,
    "msg": ""
}
```

### 房东身份认证
地址: /house_identification

方法: post

参数
```
certname: string # 房产证姓名
idcardnumber: string
property_cert_number: string # 房产证号
property_cert_photo: file # 房产证照片
[house_type: string] # 可选值： 1. 自有房屋出租， 2. 租赁房屋出租
lease_agreement_photo_url: file # 租赁合同照片
```

HTTP HEADER
```
token
```

返回
```

{
    "status": 0,
    "msg": "",
    "ans": [
        "房东姓名",
        "111112222233333", # 身份证号
        "123213jdsfjf", # 房产证号
        "data/userphoto/user_6/property_cert_photo-123213jdsfjf.jpg", # 房产证照片
        "data/userphoto/user_6/lease_agreement_photo_url-123213jdsfjf.jpg" # 租赁合同照片
    ] 
}
```

### 创建房源
地址: /house_create

```
关于地区编码的详细信息参考conf/Location.py
需要添加新地区，先查询该地区经纬度信息，按照格式编写地区数据，更新配置代码
```

方法: post

参数
```
[province_name: string] # 省
[province_code: number] # 省
[city_name: string] # 市
[city_code: number] # 市
[county_name: string] # 区县
[county_code: number] # 区县
[district_name: string] # 小区
[district_code: number] # 小区
[house_number: number] # 门牌号
[longitude: number] # 经纬度
[latitude: number] # 经纬度
[rent_time_type: number] #  出租方式，长租2 短租1
[rent_room_type: number] # 出租方式，整租1 单间2
[house_size: number] # 面积
[house_type: string] # 户型
[house_floor: string] # 楼层
[house_direction: string] # 朝向
[house_decoration: string] # 装修程度
[house_max_livein: number] # 最大居住人数
[house_rent: number] # 租金
[payment_type: string] # 付款方式, 1|1 押一付一, 1|3 押一付三, 1|6 押一付六
[property_management_fee: number] # 物业费归属, 1 房东, 2 租客, 3 待定
[heating_charge: number] # 取暖费归属, 1 房东, 2 租客, 3 待定
[description_title: string] # 介绍标题
[description: string] # 特色介绍
[traffic_condition: string] # 交通情况
[around_condition: string] # 周边情况
[facility: string] # 房屋设施, 1. 空调， 2. 电视， 3. 洗衣机， 4. 冰箱， 5. 微波炉， 6. 热水淋浴， 7.有线网络， 8. 无线网络， 9. 暖气， 10. 门禁系统， 11. 电梯， 12. 停车位; 1|2|3

[house_rooms: number] # 卧室数量
[subdistrict_code: number] # 街道
[subway_station_code: number] # 地铁站
[house_characteristic: string] # 房源特色

[house_source: number] # 房源类型，1. 房东直租， 2. 二房东合租， 3.租客租期内转租
[all_floor: number] # 全部楼层
[earliest_checkin_time: string] # 最早入住时间
[release_time: string] # 发布时间
[submission_time: string] # 提交审核时间
[extra_fee: string] # 额外费用。 1. 水费， 2. 电费， 3. 燃气费， 4. 网费， 5. 取暖费， 6. 卫生费， 7. 电视费， 8. 物业费； 1|2|3
```

HTTP HEADER
```
token
```

返回
```
{
    "msg": "",
    "status": 0,
    "ans": {
        "house_id": 22
    }
}
```

### 发布房源
地址: /house_release

方法: post

参数
```
house_id: number
```

HTTP HEADER
```
token
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 房东房源列表
地址: /my_house_list

```
所有有关图片获取的操作均通过 /file 接口实现
```

方法: post

参数
```
```

HTTP HEADER
```
token
```

返回
```
{
    "msg": "",
    "status": 0,
    "ans": [
        {
            "create_time_duration": 15643101,
            "house_rent": 0,
            "status": null,
            "payment_type": "1|3",
            "house_size": 0,
            "house_photo": [],
            "praise_count": null,
            "house_video": [],
            "create_date": "2017-21-06",
            "house_type": "0",
            "id": 19
        },
        {
            "create_time_duration": 28822,
            "house_rent": 0,
            "status": 0,
            "payment_type": "1|3",
            "house_size": 0,
            "house_photo": [],
            "praise_count": 0,
            "house_video": [],
            "create_date": "2017-19-12",
            "house_type": "0",
            "id": 22
        }
    ]
}
```

### 修改房源信息
地址: /update_house_info

方法: post

参数
```
attr_name: string
attr_value: string
house_id: number
```

HTTP HEADER
```
token
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 下架房源
地址: /pulloff_house

方法: post

参数
```
house_id: number
```

HTTP HEADER
```
token
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 删除房源
地址: /delete_house_info

方法: post

参数
```
house_id
```

HTTP HEADER
```
token
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 修改房源照片，一次一张
地址: /update_house_photo

方法: post

参数
```
photo_id: number # 添加照片时可获取id，需要记录下来
house_photo: file
```

HTTP HEADER
```
token
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 添加房源照片，一次一张或多张
地址: /create_house_photo

方法: post

参数
```
house_id: number
house_photo: file
rooms_type: number   # 房间类型： 1. 主卧， 2. 次卧， 3. 客厅， 4. 厨房， 5. 卫生间， 6. 阳台， 7. 其他房间
rooms_area: number  # 房间的面积，只有主卧、次卧类型的房间有这一字段
rooms_orientation: string  # 房间的朝向，只有主卧、次卧类型的房间有这一字段，房间内最大采光面即窗户的朝向。
```

HTTP HEADER
```
token
```

返回
```

{
    "status": 0,
    "msg": "",
    "ans": {
        "url": [
            "data/userphoto/user_6/house_photos-0-a1055b7a-3003-11e8-81cf-a45e60b7d88f.jpg",
            "data/userphoto/user_6/house_photos-1-a1055b7a-3003-11e8-81cf-a45e60b7d88f.jpg"
        ],
        "id": [
            10,
            11
        ]
    }
}
```

### 修改房源视频
地址: /update_house_video

方法: post

参数
```
video_id: number
house_video: file
```

HTTP HEADER
```
token
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 添加房源视频
地址: /create_house_video

方法: post

参数
```
house_id: number
house_video: file
```

HTTP HEADER
```
token
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {"id": 1, "url": ""}
}
```

### 搜索房源
地址: /search_house

方法: post

参数
```
[house_name: string] # 房屋介绍标题
[house_type: string] # 户型
[house_rent_time_type: string] # 类型，1 短租, 2 长租
[house_rent_room_type: number] # 类型，1 整租, 2 单间, e.g., 1   2  1|2
[house_rent_fee: string] # 租金, 区间形式, [100, 500] [,800] [1000,]
[house_source: number] # 来源，1 房东, 2 二房东, 3 中介, e.g., 1   2  1|2  1|2|3
[house_size: number] # 面积, [20, 50] [,100] [100,]
[house_direction: string] # 朝向, 多个用 | 隔开
[house_decoration: string] # 装修情况, 多个用 | 隔开
[radius: number] # 筛选距离半径, km
[shift: number] # 筛选偏移, 返回[shift:]区间内的查询结果, 默认0
[count: number] # 筛选数目
[sort: number] # 排序，1 距离升，2 时间降，3 关注度降，4 租金升， 5 租金降 6 面积升

[house_rooms: string] # 卧室数量, 支持多选. e.g, 1    2    1|3     3|4|5
[subdistrict_code: number] # 按街道筛选, 单选
[subway_station_code: number] # 按地铁站筛选,单选
[house_characteristic: string] # 房源特色, 支持多选, 多个用 | 隔开

longitude: number # 经度
latitude: number # 纬度
```

HTTP HEADER
```
token
```

返回
```

{
    "status": 0,
    "msg": "",
    "ans": [
        {
            "house_rent": 0,
            "status": null,
            "create_date": "2017-21-06",
            "distance": 8.90555926346204,
            "house_size": 0,
            "user_type": 1,
            "photos": [
                "data/userphoto/user_6/house_photo-4d4a58e6-3000-11e8-a15e-a45e60b7d88f.jpg",
                "data/userphoto/user_6/house_photo-e70133dc-5749-11e7-b617-a45e60b7d88f.jpg",
                "data/userphoto/user_6/house_photo-e70133dc-5749-11e7-b617-a45e60b7d88f.jpg",
                "data/userphoto/user_6/house_photo-0c11c970-574a-11e7-990f-a45e60b7d88f.jpg",
                "data/userphoto/user_6/house_photo-0c11c970-574a-11e7-990f-a45e60b7d88f.jpg",
                "data/userphoto/user_6/house_photo-0c11c970-574a-11e7-990f-a45e60b7d88f.jpg",
                "data/userphoto/user_6/house_photo-2133324c-574a-11e7-9535-a45e60b7d88f.jpg"
            ],
            "duration": 23937811,
            "payment_type": "1|3",
            "praise_count": null,
            "house_type": "0",
            "house_id": 18
        },
        {
            "house_rent": 0,
            "status": null,
            "create_date": "2017-21-06",
            "distance": 8.90555926346204,
            "house_size": 90,
            "user_type": 1,
            "photos": [
                "data/userphoto/user_6/house_photos-0-8af48880-3003-11e8-9e95-a45e60b7d88f.jpg",
                "data/userphoto/user_6/house_photos-1-8af48880-3003-11e8-9e95-a45e60b7d88f.jpg",
                "data/userphoto/user_6/house_photos-0-a1055b7a-3003-11e8-81cf-a45e60b7d88f.jpg",
                "data/userphoto/user_6/house_photos-1-a1055b7a-3003-11e8-81cf-a45e60b7d88f.jpg"
            ],
            "duration": 23937700,
            "payment_type": "1|3",
            "praise_count": null,
            "house_type": "1",
            "house_id": 19
        }
    ]
}
```

### 获取邀请码
地址: /invitation/getcode

方法: get

参数
```
```

HTTP HEADER
```
token
```

返回
```
{
    "status": 0,
    "msg": "",
    "ans": {
        "friend_invite_code": "0000000A", # 注册时填写的邀请码
        "my_invite_code": "00000006" # 自己的邀请码
    }
}
```

### 填写邀请码
地址: /invitation/setcode

方法: get

参数
```
invite_code: string # 邀请码
```

HTTP HEADER
```
token
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 创建看房申请
地址: /order/create_preorder

方法: post

参数
```
owner_id: 房东id
house_id: 房屋id
```

HTTP HEADER
```
token
```

返回
```

{
  "status": 0,
  "msg": "OK",
  "ans": 7 # pre_order_id
}
```

### 获取看房申请支付url,  看房信息费
地址: /order/get_preorder_paymenturl

方法: post

参数
```
pre_order_id: 看房申请id
return_url: 支付成功或失败后，把结果带给前端, url是包括域名完整链接,例如http://domain/
# 返回携带以下参数
#示例1: http://domain/?total_amount=0.01&timestamp=2011-11-11+23%3A11%3A46&sign=&trade_no=&sign_type=RSA2&auth_app_id=&charset=utf-8&seller_id=&method=alipay.trade.wap.pay.return&app_id=&out_trade_no=71&version=1.0

#示例2: https://m.alipay.com/Gk8NF23?total_amount=9.00&timestamp=2016-08-11+19%3A36%3A01&sign=ErCRRVmW%2FvXu1XO76k%2BUr4gYKC5%2FWgZGSo%2FR7nbL%2FPU7yFXtQJ2CjYPcqumxcYYB5x%2FzaRJXWBLN3jJXr01Icph8AZGEmwNuzvfezRoWny6%2Fm0iVQf7hfgn66z2yRfXtRSqtSTQWhjMa5YXE7MBMKFruIclYVTlfWDN30Cw7k%2Fk%3D&trade_no=2016081121001004630200142207&sign_type=RSA2&charset=UTF-8&seller_id=2088111111116894&method=alipay.trade.wap.pay.return&app_id=2016040501024706&out_trade_no=70501111111S001111119&version=1.0

#文档参考: https://docs.open.alipay.com/203/107090
```

HTTP HEADER
```
token
```

返回
```

{
    "status": 0,
    "msg": "",
    "ans": {
        "result": "SUCCESS",
        "payment_url": "https://openapi.alipay.com/gateway.do?format=JSON&timestamp=2017-10-29+19%3A32%3A29&charset=utf-8&app_id=2017081508207837&biz_content=%7B%22body%22%3A+%22pre+order+fee%22%2C+%22out_trade_no%22%3A+%227%22%2C+%22product_code%22%3A+%22QUICK_WAP_WAY%22%2C+%22total_amount%22%3A+10.0%2C+%22subject%22%3A+%22%E4%BF%A1%E6%81%AF%E8%B4%B9%22%7D&sign=y%2BNHVnVL6iIb8rnK%2BM1RhK34Dwka08RGXbYXHp0tlWHWaEojpgX7soJo04tX0Jt%2BRb2oiEjw6KJAjQ48Xb2vy42F1%2FzwT1IHNIhtNBFl3xfl6twMtuDsV0PQ1TABgZXWVLaRzF79PNWeNbkDAxPEOcHD5EodEWzwmCLVLhmYyjc37cbESemBqH9pnif9V30F6BZleMGFNo53q%2BmjQMGvWoXDkrNth1HgEg0RJ3i0%2BGEQKLy83JRmhtUf9mEpWTC8OEh8ZRW306TGvhuHQT7iOo2QEOz36lFW20j2szaM%2Fymvg9YJEaPlx6q%2BwjhA7y72FJB%2B3MgglyrvoOHzBqYqGg%3D%3D&version=1.0&notify_url=&sign_type=RSA2&method=alipay.trade.wap.pay&return_url="
    }
}
```

### 获取用户授权
地址: /payment/ali/get_auth_url

方法: post

参数
```
```

HTTP HEADER
```
token
```

返回
```
{
    "status": 0,
    "msg": "",
    "ans": {
        # 引导用户授权
        "auth_url": "https://openauth.alipay.com/oauth2/publicAppAuthorize.htm?scope=auth_user&state=adf598e6c57dc973a85e733e880414eb&redirect_uri=http%3A%2F%2F119.29.113.28%3A20001%2Fpayment%2Fali%2Fauth_notify&domain_url=https%3A%2F%2Fopenauth.alipay.com%2Foauth2%2FpublicAppAuthorize.htm&app_id=2017081408197189",
        "result": "SUCCESS"
    }
}
```

### 查看用户是否已经绑定支付宝账号
地址: /payment/ali/binding_status

方法: post

如果没有绑定，需要调用用户授权接口

参数
```
```

HTTP HEADER
```
token
```

返回
```
{
    "status": 0,
    "msg": "",
    "ans": 1 # or -1
}
```

### 获取用户芝麻分
地址: /payment/ali/zhima

方法: post

参数
```
[refresh: string] # 默认值 AUTO, N 只是用缓存，Y 强制刷新, AUTO 若没有缓存则刷新。默认获取缓存值，若没有，则调用蚂蚁金服接口获取，若参数设置为Y，则强制调用接口获取最新值
# 如果refresh = Y 则必须先调用获取用户授权接口，否则无法获取芝麻分
# 若果如果refresh = AUTO，且是该用户第一次调用此接口，则必须先调用获取用户授权接口，否则无法获取芝麻分
# 判断是否是该用户第一次调用此接口，设置refresh = N, 若返回值ans=-1，则说明是第一次调用
```

HTTP HEADER
```
token
```

返回
```

{
    "status": 0,
    "msg": "",
    "ans": "750"
}
```

### 支付宝企业向个人转账(内部接口，不开放)
地址: /payment/ali/pay_to_customer

方法: post

参数
```
order_id: string # 订单id
payee_type: string # 账户类型，1、ALIPAY_USERID：支付宝账号对应的支付宝唯一用户号。以2088开头的16位纯数字组成。 2、ALIPAY_LOGONID：支付宝登录号，支持邮箱和手机号格式。
payee_acount: string # 账户
amount: float # 金额, 最小金额0.1
[remark]: string # 备注
```

HTTP HEADER
```
token
```

返回
```

{
    "status": 0,
    "msg": "",
    "ans": "750"
}
```
