import os
import torndb
import MySQLdb
settings = {
    "cookie_secret": "123123124412341234214321khaksdlfasdfpqwirqwevcvpisfdpqgnpqrngpqerg",
    "login_url": "/login",
    # "xsrf_cookies": True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "debug":True,
}

db=torndb.Connection(host="localhost",user="freeweb",password="123456",database="web_db")
mysql_db=MySQLdb.connect(host="localhost",user="freeweb",passwd="123456",db="web_db")
LOG_FILE_PATH = "/var/log/freeweb.log"
