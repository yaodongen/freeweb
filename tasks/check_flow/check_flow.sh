
FREEWEB_TASK_PATH=$(cd `dirname $0`/../ ;pwd)

# 更新iptables数据
/sbin/iptables -nxvL > $FREEWEB_TASK_PATH/check_flow/iptables.out

# 更新数据库
/usr/bin/python $FREEWEB_TASK_PATH/check_flow/record.py $FREEWEB_TASK_PATH/check_flow/iptables.out






