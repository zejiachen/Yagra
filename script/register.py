#!/usr/bin/python
#*-- encoding=utf8 --*
'implemention of registration'
import cgi
import time
import Cookie
import random
import hashlib
import MySQLdb
from os import environ
from sys import maxint
import modules.util as util
import modules.webconf as conf


def main():
    req_method = environ['REQUEST_METHOD']
    if req_method == 'GET':
        util.showpage('register.html')
    else:
        do_register()


def do_register():
    # get input parameters
    form = cgi.FieldStorage()
    username = form['username'].value
    password = form['password'].value

    # check whether the username is used
    mysql_conn = MySQLdb.connect(conf.db_host, conf.db_user,
                                 conf.db_passwd, conf.db_name)
    mysql_cursor = mysql_conn.cursor()
    query = 'select * from user where username="%s"' % username
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchone()
    if result:
        util.showpage('register_err.html', '邮箱被占用')
        mysql_cursor.close()
        mysql_conn.close()
        return

    # get uid for username
    query = 'select max(uid) from user'
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchone()
    cur_max_id = result[0]
    if cur_max_id:
        uid = cur_max_id + 1
    else:
        uid = 1

    # insert into database
    query = 'insert into user values(%s, "%s", "%s", "/")' %\
            (uid, username, password)
    mysql_cursor.execute(query)
    mysql_conn.commit()

    # set cookie and redirect to homepage
    sid = hashlib.md5(str(random.randint(0, maxint))).hexdigest()
    expired_at = int(time.time()) + conf.session_expires
    str_expired_at = time.strftime('%F %T', time.localtime(expired_at))
    ip = environ['REMOTE_ADDR']
    query = 'insert into session values(%s, "%s", "%s", "%s")' %\
            (uid, sid, ip, str_expired_at)
    mysql_cursor.execute(query)
    mysql_conn.commit()
    cookie = Cookie.SimpleCookie()
    cookie['sid'] = sid
    cookie['sid']['expires'] = conf.session_expires
    cookie['uid'] = uid
    util.redirectTo('index.py', cookie)


if __name__ == '__main__':
    main()
