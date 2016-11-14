# -*- coding:utf8 -*-
import sys
import re
import torndb

sys.path.insert(0, os.path.abspath(os.path.join(__file__,"../../../")))
from settings import db


def run(file_name):
    """ 这里只限制输出流量 """
    db_data={}
    with open(file_name,"r") as rf:
        chain_name=""
        for line in rf.readlines():
            if line[:5] == "Chain":
                chain_name=line[6:15]
            elif chain_name=="ssserver8":
                mat = re.match("^\s*(\d+)\s*(\d+)\s*ACCEPT.*spt:(\d+).*$",line)
		if not mat:
		    mat = re.match("^\s*(\d+)\s*(\d+)\s*ACCEPT.*dpt:(\d+).*$",line)
                if mat:
                    used_flow = int(mat.group(2))*1.0/1000/1000
                    port = mat.group(3)
		    db_data.setdefault(port,0)
	            db_data[port]+=used_flow
    for port,used_flow in db_data.items():
        db.execute("update user set used_flow=%s where user.user=(select owner from ssserver where port=%s);",used_flow,port)
                


if __name__=="__main__":
    if len(sys.argv)>=2:
        run(sys.argv[1])




