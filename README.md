# Yagra
## 代码结构
- script/: 网站Yagra的python文件，同时也是Yagra的入口文件
  - modules/: script/文件夹下的各python文件共用的一些模块的实现，包括util.py 和 webconf.py
- templates/: html模板文件，模板文件中若干需要形式化的参数，由/script下的.py读出、形式化并最终呈现给用户
- static/: 静态文件，包括用户默认头像(no\_pic)和网站图标(Yagra.ico)
- setup.sh: Yagra的安装脚本

## 安装指南
- 配置， 设置script/modules/webconf.py中的各配置项，包括：
  - 数据库相关配置，db\_host, db\_user, db\_passwd, db\_name（请不要更改db\_name，正确设置host, user, passwd参数）
  - web\_path: 网站根目录, 默认是/var/www/，相对应的cgi路径为 /var/www/cgi-bin
  - session\_expires: session有效期, 以秒为单位
  - login\_expires: 登陆时限（即获取prelogin参数后需在多长时间内完成登陆）,以秒为单位
  - img\_max\_size: 头像最大的字节数
- 安装
  - sudo ./setup.sh : 请确保当前用户具备在网站根目录(/var/www/）下创建文件/文件夹的权限，建议sudo执行
  - apache的相关配置: 即设置cgi-bin为cgi脚本存放路径, 另外禁止对modules文件夹的访问, 以保护modules文件夹下的配置信息不被非法读取
- 演示
  - 作者在实验室机器上部署了该项目，可通过如下地址访问：http://210.25.189.114/cgi-bin/login.py

## 实现逻辑
### Cookie 设计
Cookie包含以下两个字段
- uid: 标识用户的唯一ID
- sid: Session ID, 当用户新建一个session时, 服务端为该session生成的随机串, 有效期默认为4小时

### 数据库设计
数据库包含两个表:
- user表:

        +----------+------------+-------------+-----------+
        |    uid   |  username  |   password  | img_path  |
        +----------+------------+-------------+-----------+
        |  用户id   |    用户名   |  密码的md5值 | 头像文件名  |
        +----------+------------+-------------+-----------+

- session表:

        +----------+------------+------------+-----------------+
        |    uid   |     sid    |     ip     |     expires     |
        +----------+------------+------------+-----------------+
        |   用户id  | Session ID |  上次登录IP | Session失效时间  |
        +----------+------------+------------+-----------------+

### 登录
登录由以下步骤完成:
- 预登录(prelogin): 向服务端请求预登录参数, servtime(服务端当前时间) 和 nonce(随机数), 用于Cookie超时判断, 防止重放攻击
- 浏览器端对密码进行加密: enc\_passwd = md5(md5(passwd) + '|' + servtime + '|' + nonce)
- 浏览器端提交 四个参数: username, enc\_passwd, servtime, nonce
- 服务端校验用户名/密码对: 若用户存在, 取出数据库中存储的 md5(passwd) -- 为安全起见, 不存明文; 计算并校验 enc\_passwd
- 若用户名/密码 正确, 则为该用户生成sid(random出来的32字节随机串), 并set cookie, 重定向到用户首页(index.py)

### 登出
登出由以下步骤完成:
- 服务端将数据库Session中相应的Cookie的状态置为过期
- 服务端返回带set cookie的包, 令 cookie['sid']['expires'] 为1970-01-01 10:00:00, 浏览器收到响应后删除过时cookie

### 注册
注册由以下步骤完成:
- 客户端在提交注册请求时, 提交的参数包括user\_name, md5(passwd)
- 服务器检查用户名是否已经被占用, 如被占用, 提示错误, 返回
- 如用户名未被占用, 服务端将user\_name, md5(passwd)存储到数据库中
- 服务端为当前用户生成sid, Set Cookie, 并重定向到用户首页 (index.py)

### 头像
- 头像文件名的生成: md5(user\_name)
- 头像文件的存储: 存储在网站根目录静态文件夹下, 默认为 /var/www/html/avatar/ 下
- 头像的链接: http://网站地址/avatar/md5(user\_name), 代码见: http://210.25.189.114/cgi-bin/api.py
