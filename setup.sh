#!/usr/bin/env bash

#read config
cd script/modules/
str_conf=`
python <<EOF
from webconf import *
print db_host, db_user, db_passwd, web_path
EOF
`
cd ../../
arr_conf=($str_conf)
db_host=${arr_conf[0]}
db_user=${arr_conf[1]}
db_passwd=${arr_conf[2]}
web_path=${arr_conf[3]}


#init database
res=`mysql '-h'$db_host '-u'$db_user '-p'$db_passwd <<EOF
create database if not exists yagra;
use yagra;
drop table if exists user;
drop table if exists session;
create table user (
    uid int primary key auto_increment,
    username varchar(100),
    password char(32),
    img_path char(32)
);
create table session (
    uid int primary key,
    sid char(32),
    ip char(16),
    expires timestamp
);
desc session;
EOF`
#if desc session success, it means execute of sql is success
if [ "$res" != '' ]; then
    echo 'init database successfully'
else
    echo 'Fail to init database, please check config'
    exit 1
fi


#mkdir and copy files
mkdir -p $web_path'/cgi-bin'
mkdir -p $web_path'/templates'
mkdir -p $web_path'/html/avatar'
cp -rf script/* $web_path'/cgi-bin/'
cp -rf templates/* $web_path'/templates/'
cp -rf avatar/* $web_path'/html/avatar/'
chmod a+w $web_path'/html/avatar'
