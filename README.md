### 通过openid获取用户信息
地址: /wx_fetch_userinfo

方法: get

参数
```
openid
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {
  	"token": 10effdbde7224e80b7d157e9cf8f2fc54888035d1aebfa31347924794353927d,
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
openid
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 实名认证
地址: /user_identification

方法: post

参数
```
openid
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 房东身份认证
地址: /house_identification

方法: post

参数
```
openid
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

方法: post

参数
```
openid
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

方法: post

参数
```
openid
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 修改房源信息
地址: /update_house_info

方法: post

参数
```
openid
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
openid
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
openid
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
openid
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
openid
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 修改房源视频
地址: /update_house_video

方法: post

参数
```
openid
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
openid
```

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 搜索房源
地址: /search_house

方法: post

参数
```
openid
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

返回
```

{
  "status": 0,
  "msg": "",
  "ans": {}
}
```

### 填写邀请码
地址: /invitation/setcode

方法: get

参数
```
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

返回
```

{
  "status": 0,
  "msg": "OK",
  "ans": 7 # pre_order_id
}
```

### 获取看房申请支付url
地址: /order/get_preorder_paymenturl

方法: post

参数
```
pre_order_id: 看房申请id
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
