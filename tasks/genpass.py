#! /usr/bin/python
# -*- coding:utf8 -*-
import hashlib
import sys
import getopt


DICT_METHOD = {
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
    "md5": hashlib.md5,
}

def get_config():
    config = {"password":"password","salt":"salt","length":12,"method":"sha256","mode":0}
    detail_mode = False
    try:
        # :表示后面有参数
        shortopts = 'hirp:s:l:m:'
        #  =表示后面有参数
        longopts = ['help','info','raw', 'password=', 'salt=', 'length=','method=']
        optlist, _ = getopt.getopt(sys.argv[1:],shortopts,longopts)
        if not optlist:
            raise getopt.GetoptError("")
        for key, value in optlist:
            if key == '-p' or key == '--password':
                config['password'] = value
            elif key=='-s' or key == '--salt':
                config['salt'] = value
            elif key=='-l' or key == '--length':
                config['length'] = int(value)
            elif key=='-m' or key == '--method':
                config['method'] = value
            elif key=='-h' or key == '--help':
                print_help()
                sys.exit(0)
            elif key=='-i' or key=='--info':
                detail_mode = True
            elif key=='-r' or key=='--raw':
                config['mode'] = 1 
    except getopt.GetoptError as e:
        print_help()
        sys.exit(1)
    if detail_mode:
        print "your config : %s"%config
    return config

def generate_password(password, salt, length, method, mode):
    """ 
        通过哈希，将一段简单的密码转化为复杂到密码
        为了让这个算法容易实现,采用简单的加盐的方式 
    """
    hash_method = DICT_METHOD.get(method, hashlib.sha256)
    return hash_method(password+salt).hexdigest()[:int(length)],mode


def print_help():
    print('''usage: gen_pass [OPTION]...
sample usage: 
    ./genpass -p 123456 -s baidu   
    ./genpass -p 123456 -s baidu -l 12 -m sha256

A simple password generator that helps you generate complicated password
General options:
  -p PASSWORD, --password PASSWORD   original password
  -s SALT, --salt SALT               a string after original password
  -l LENGTH, --length LENGTH         password length 
  -m METHOD, --method METHOD         password hash 
  -h, --help                         show this help message and exit
  -i, --info                         show origanl password
  -r, --raw                          only show the raw password

if you want to use the tool in anywhere,you can config like this
    vim ~/.bashrc (append the code below)
    alias genpass="python $YOURPATH/utils/python/others/genpass"
''')


if __name__=="__main__":
    ans,_ =generate_password(**get_config())
    if not _:
        print "your password : %s"%ans
    else:
        print ans
