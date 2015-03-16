#!/usr/bin/python
import cgi
import time
import Cookie
import hashlib
import MySQLdb
from os import environ
from datetime import datetime
import webconf as conf


def showpage(filename, *args):
    filename = '../templates/' + filename
    html = open(filename, 'r')
    print 'Content-Type: text/html;charset=utf8\r\n'
    print html.read() % args
    html.close()


def redirectTo(url, cookie=None):
    print 'Content-Type: text/html;charset=utf8'
    if cookie:
        print cookie
    print 'Location: %s\r\n' % url


def validateCookie():
    if 'HTTP_COOKIE' not in environ:
        return False
    cookie = Cookie.SimpleCookie(environ['HTTP_COOKIE'])
    if 'uid' not in cookie or 'sid' not in cookie:
        return False
    mysql_conn = MySQLdb.connect(conf.db_host, conf.db_user,
                                 conf.db_passwd, conf.db_name)
    mysql_cursor = mysql_conn.cursor()
    query = 'select * from session where uid=%s' % cookie['uid'].value
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchone()
    mysql_cursor.close()
    mysql_conn.close()
    if not result or result[1] != cookie['sid'].value:
        return False
    cur_time = datetime.fromtimestamp(time.time())
    if cur_time > result[3]:
        return False
    return True


def getCookie():
    if not validateCookie():
        return None
    cookie = Cookie.SimpleCookie(environ['HTTP_COOKIE'])
    return cookie


def avatarFilename(uid):
    # get username from db
    mysql_conn = MySQLdb.connect(conf.db_host, conf.db_user,
                                 conf.db_passwd, conf.db_name)
    mysql_cursor = mysql_conn.cursor()
    query = 'select * from user where uid=%s' % uid
    mysql_cursor.execute(query)
    result = mysql_cursor.fetchone()
    username = result[1]
    mysql_cursor.close()
    mysql_conn.close()

    # filename is the hash of username
    filename = hashlib.md5(username).hexdigest()
    return filename


def main():
    showpage('login.html')


if __name__ == '__main__':
    main()
