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
  	"token": 10effdbde7224e80b7d157e9cf8f2fc54888035d1aebfa31347924794353927d, # 放置于http header中，登陆
    "headimgurl": "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
    "wx_nickname": "Band",
    "wx_city": "广州",
    "wx_province": "广东",
    "wx_sex": 1,
    "wx_openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M",
    "wx_country": "中国"
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
[payment_type: string] # 付款方式, 1|3 押一付三, 2|6 押二付六, 1|0 无押金
[property_management_fee: number] # 物业费归属, 1 房东, 2 租客, 3 待定
[heating_charge: number] # 取暖费归属, 1 房东, 2 租客, 3 待定
[description_title: string] # 介绍标题
[description: string] # 特色介绍
[traffic_condition: string] # 交通情况
[around_condition: string] # 周边情况
[facility: string] # 房屋设施, 1 空调, 2 暖气, 3 洗衣机, 4 冰箱, 5 允许宠物, 6 电视, 7 浴缸, 8 热水淋浴, 9 门禁系统, 10 有线网络, 11 电梯, 12 无线网络, 13 停车位, 14 饮水机; 1|2|3
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

### 添加房源照片，一次一张
地址: /create_house_photo

方法: post

参数
```
house_id: number
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
  "ans": {"id": 1, "url": ""}
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
[house_rent_time_type: number] # 类型，1 短租, 2 长租
[house_rent_room_type: number] # 类型，1 整租, 2 单间
[house_rent_fee: string] # 租金, 区间形式, [100, 500] [,800] [1000,]
[house_source: number] # 来源，1 房东, 2 二房东, 3 中介
[house_size: number] # 面积, [20, 50] [,100] [100,]
[house_direction: string] # 朝向
[house_decoration: string] # 装修情况
[radius: number] # 筛选距离半径, km
[shift: number] # 筛选偏移, 返回[shift:]区间内的查询结果, 默认0
[count: number] # 筛选数目
[sort: number] # 排序，1 距离升，2 时间降，3 关注度降，4 租金升， 5 租金降 6 面积升
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
  "ans": {}
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
