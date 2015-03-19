#!/usr/bin/python
#*-- encoding=utf8 --*
'implemention of logout: let cookie expires at db and client'
import Cookie
import MySQLdb
import modules.util as util
import modules.webconf as conf


def main():
    # let cookie expires at db
    cookie = util.getCookie()
    if cookie:
        mysql_conn = MySQLdb.connect(conf.db_host, conf.db_user,
                                     conf.db_passwd, conf.db_name)
        mysql_cursor = mysql_conn.cursor()
        query = 'update session set expires="1970-01-01 10:00:00" ' + \
                'where uid=%s' % cookie['uid'].value
        mysql_cursor.execute(query)
        mysql_conn.commit()
        mysql_cursor.close()
        mysql_conn.close()

    # tell client the cookie is expired and redirect to login page
    cookie = Cookie.SimpleCookie()
    cookie['sid'] = 'deleted'
    cookie['sid']['expires'] = 0
    cookie['uid'] = 'deleted'
    cookie['uid']['expires'] = 0
    print 'Content-Type: text/html'
    print cookie
    print 'Location: login.py\r\n'


if __name__ == '__main__':
    main()
