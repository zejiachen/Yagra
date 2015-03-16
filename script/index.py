#!/usr/bin/python
'check whether sid is valid, show index.html or login.html'
import cgi
import time
import Cookie
import MySQLdb
from os import environ
from datetime import datetime
import modules.util as util
import modules.webconf as conf


def main():
    if not util.validateCookie():
        util.redirectTo('login.py')
        return
    else:
        cookie = util.getCookie()
        mysql_conn = MySQLdb.connect(conf.db_host, conf.db_user,
                                     conf.db_passwd, conf.db_name)
        mysql_cursor = mysql_conn.cursor()
        query = 'select * from user where uid=%s' % cookie['uid'].value
        mysql_cursor.execute(query)
        result = mysql_cursor.fetchone()
        filename = result[3]
        if filename == '/':
            filename = 'no_pic'
        util.showpage('index.html', '../avatar/' + filename)


if __name__ == '__main__':
    main()
