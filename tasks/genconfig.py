# -*- coding:utf-8 -*-
import sys
import MySQLdb
import json
import os

# 这么写是因为这个项目是共享的，所以会gitignore settings.py
sys.path.insert(0, os.path.abspath(os.path.join(__file__,"../../")))
from settings import mysql_db


base_config = {
    "server_port":1234,
    "password":"123456",
    "server":"0.0.0.0",
    "local_address":"127.0.0.1",
    "local_port":1080,
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":False,
    "pid-file":"/var/run/ssserver8989.pid",
    "log-file":"/var/log/ssserver8989.log"
}


def run(data_type):
    cur=mysql_db.cursor()
    cur.execute("select port, password from ssserver where type=%s"%data_type)
    main_path = os.environ.get('FREEWEB_TASK_PATH')
    for port,password in cur.fetchall():
        base_config["server_port"]=port
        base_config["password"]=password
        base_config["pid-file"]="/var/run/ssserver%s.pid"%port
        base_config["log-file"]="/var/log/ssserver%s.log"%port
        with open(main_path+"/data/ssserver%s.json"%port, "w") as wf:
            wf.write(json.dumps(base_config))

if __name__=="__main__":
    if len(sys.argv)<2:
        print "请输入类型 0 1 2"
        exit(-1)
    run(sys.argv[1])    
