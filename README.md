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
