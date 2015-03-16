#!/usr/bin/python
#*-- encoding=utf8 --*
'upload avatar action'
import cgi
import MySQLdb
import modules.util as util
import modules.webconf as conf


def file_len(fp):
    fp.seek(0, 2)
    fl = fp.tell()
    fp.seek(0, 0)
    return fl


def main():
    #validate cookie and get cookie if valid
    if not util.validateCookie():
        util.redirectTo('login.py')
        return
    cookie = util.getCookie()
    uid = cookie['uid'].value

    # check info of uploaded file
    form = cgi.FieldStorage()
    if 'upfile' not in form:
        util.showpage('upload_err.html', "请选择上传文件")
        return
    upfile = form['upfile']
    filename = upfile.filename
    upfile = upfile.file
    filelen = file_len(upfile)
    if filelen > conf.img_max_size:
        max_size = int(conf.img_max_size / 1024)
        util.showpage('uploa_err.html', "图片大小不能超过%sK", max_size)

    # save avatar
    filename = util.avatarFilename(uid)
    outfile = open('../html/avatar/' + filename, 'w')
    outfile.write(upfile.read(filelen))
    outfile.close()

    #update img_path in mysql
    mysql_conn = MySQLdb.connect(conf.db_host, conf.db_user,
                                 conf.db_passwd, conf.db_name)
    mysql_cursor = mysql_conn.cursor()
    query = 'update user set img_path="%s" where uid=%s' % (filename, uid)
    mysql_cursor.execute(query)
    mysql_conn.commit()
    mysql_cursor.close()
    mysql_conn.close()

    # upload successfully, redirect to home page
    util.redirectTo('index.py')


if __name__ == '__main__':
    main()
