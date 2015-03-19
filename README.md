# Yagra
## 代码结构
- script/: 网站Yagra的python文件，同时也是Yagra的入口文件
  - modules/: script/文件夹下的各python文件共用的一些模块的实现，包括util.py 和 webconf.py
- templates/: html模板文件，模板文件中若干需要形式化的参数，由/script下的.py读出、形式化并最终呈现给用户
- static/: 静态文件，包括用户默认头像(no_pic)和网站图标(Yagra.ico)
- setup.sh: Yagra的安装脚本

## 安装指南
- 配置， 设置script/modules/webconf.py中的各配置项，包括：
  - 数据库相关配置，db_host, db_user, db_passwd, db_name（请不要更改db_name，正确设置host, user, passwd参数）
  - web_path: 网站根目录, 默认是/var/www/，相对应的cgi路径为 /var/www/cgi-bin
  - session_expires: session有效期, 以秒为单位
  - login_expires: 登陆时限（即获取prelogin参数后需在多长时间内完成登陆）,以秒为单位
  - img_max_size: 头像最大的字节数
- 安装
  - sudo ./setup.sh : 请确保当前用户具备在网站根目录(/var/www/）下创建文件/文件夹的权限，建议sudo执行
- 演示
  - 作者在实验室机器上部署了该项目，可通过如下地址访问：http://210.25.189.114/cgi-bin/login.py
