import os
import torndb
settings = {
    "cookie_secret": "qqqqqqqqqqqqqqqqqqqq",
    "login_url": "/login",
    # "xsrf_cookies": True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "debug":True,
}

db=torndb.Connection(host="localhost",user="freeweb",password="123456",database="web_db")
