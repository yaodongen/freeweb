# !/usr/python
import re
import time
import sys








"""
tcp        0      0 45.63.124.217:48764     8.8.8.8:53              TIME_WAIT  
tcp        0      0 45.63.124.217:8002      61.148.243.34:20617     ESTABLISHED
tcp        0      0 45.63.124.217:7002      180.162.160.69:47499    TIME_WAIT  
tcp        0      0 45.63.124.217:60173     216.58.200.202:443      ESTABLISHED
"""




def run(filename=""):
    with open(filename, "r") as  rf:
        server_cli=set()
        for line in rf.readlines():
            if line[:3]!="tcp":
                continue
            items = line.split()
            port = items[3].split(":")[-1]
            ip = items[4].split(":")[0]
            if 6000<=int(port)<=9000:
                server_cli.add((port,ip))
        print time.ctime()
        print server_cli

if __name__=="__main__":
    if len(sys.argv)<2:
        sys.exit(0)
    run(sys.argv[1])
