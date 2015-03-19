#!/usr/bin/python
# *-- encoding=utf8 --*
'some config for the Yagra website running and installation'

# config for database, please set db_name to 'yagra'
db_host = 'localhost'
db_user = 'root'
db_passwd = 'zejiachen'
db_name = 'yagra'

# root of the website
web_path = '/var/www/'

# the period of the validity of the prelogin parameters
login_expires = 60
# the session would be expired in session_expires seconds later
session_expires = 4 * 3600

# the max size of the uploaded avatar
img_max_size = 204800
