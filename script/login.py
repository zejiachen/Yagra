#!/usr/bin/python
#*-- encoding=utf8 --*
'login script: validate username+password, redirect to index.html if valid'
import os
import cgi
import sys
import time
import random
import Cookie
import hashlib
import MySQLdb
import modules.util as util
import modules.webconf as conf


def main():
    req_method = os.environ['REQUEST_METHOD']
    if req_method == 'GET':
        util.showpage('login.html')
    else:
        do_login()


def do_login():
    # get parameters for login action
    form = cgi.FieldStorage()
    username = form['username'].value
    password = form['password'].value
    servtime = int(form['servtime'].value)
    nonce = form['nonce'].value

    # if servtime is expired
    cur_time = int(time.time())
    if cur_time < servtime or cur_time - servtime > conf.login_expires:
        util.showpage('login_err.html', "登录超时")
        return

    # check whether username is valid
    mysql_conn = MySQLdb.connect(conf.db_host, conf.db_user,
                                 conf.db_passwd, conf.db_name)
    mysql_cursor = mysql_conn.cursor()
    query = 'select * from user where username="%s"' % username
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchone()
    if not result:
        util.showpage('login_err.html', "用户不存在")
        mysql_cursor.close()
        mysql_conn.close()
        return

    # check whether password is right
    real_passwd = result[2]
    uid = result[0]
    encrypt_passwd = hashlib.md5(real_passwd + '|' + str(servtime)
                                 + '|' + str(nonce)).hexdigest()
    if encrypt_passwd != password:
        util.showpage('login_err.html', '密码错误')
        mysql_cursor.close()
        mysql_conn.close()
        return

    # username / password is ok, set cookie, redirect to index.html
    sid = hashlib.md5(str(random.randint(0, sys.maxint))).hexdigest()
    expired_at = int(time.time()) + conf.session_expires
    str_expired_at = time.strftime('%F %T', time.localtime(expired_at))
    ip = os.environ['REMOTE_ADDR']
    query = 'select * from session where uid=' + str(uid)
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchone()
    if result:
        query = 'update session set sid="%s",expires="%s",ip="%s" where uid=%s'\
                % (sid, str_expired_at, ip, uid)
        mysql_cursor.execute(query)
        mysql_conn.commit()
    else:
        query = 'insert into session values(%s, "%s", "%s", "%s")' %\
                (uid, sid, ip, str_expired_at)
        mysql_cursor.execute(query)
        mysql_conn.commit()
    mysql_cursor.close()
    mysql_conn.close()
    cookie = Cookie.SimpleCookie()
    cookie['sid'] = sid
    cookie['sid']['expires'] = conf.session_expires
    cookie['uid'] = uid
    util.redirectTo('index.py', cookie)


if __name__ == '__main__':
    main()
