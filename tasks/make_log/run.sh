
FREEWEB_TASK_PATH=$(cd `dirname $0`/../ ;pwd)

# 更新iptables数据
/bin/netstat -nt > $FREEWEB_TASK_PATH/make_log/netstat.out

# 更新数据库
/usr/bin/python $FREEWEB_TASK_PATH/make_log/get_current_user_ip.py $FREEWEB_TASK_PATH/make_log/netstat.out >> $FREEWEB_TASK_PATH/../log/netstat.log

rm $FREEWEB_TASK_PATH/make_log/netstat.out



