source /home/yde/freeweb/tasks/config.sh

# 选择生成密码的类型
TYPE=-1
if [ x$1 = x ] ; then
    echo -e '请输入一个参数type:\n 0 1 2 '
    exit -1
elif [ $1 -ge 0 -a $1 -le 2 ] ; then
    TYPE=$1
else
    echo -e '请输入一个参数type:\n 0 1 2 '
    exit -1
fi

if [ $TYPE = 0 ]; then
    PORT=$P_PORT
    M_PORT=$P_M_PORT
    NUM=$P_NUM
    TABLE=$P_TABLE
elif [ $TYPE = 1 ]; then
    PORT=$L_PORT
    M_PORT=$L_M_PORT
    NUM=$L_NUM
    TABLE=$L_TABLE
elif [ $TYPE = 2 ]; then
    PORT=$D_PORT
    M_PORT=$D_M_PORT
    NUM=$D_NUM
    TABLE=$D_TABLE
fi


# 删除原来的数据库内容
mysql -u$SQL_USER -p$SQL_PASSWORD  -Dweb_db -s -e  "delete from ssserver where type=$TYPE"

# 遇到问题端口继续分配
while [ $NUM -gt 0 -a $PORT -le $M_PORT ]
do
    if [ -n "$(lsof -i:$PORT)" ] ; then
        echo "DISCARDED PORT:" $PORT
    else
        NUM=$((NUM-1))
        PASSWORD=$(python2.7 $FREEWEB_TASK_PATH/genpass.py -p $FREEWEB_BASE_PASS$PORT -s `date "+%s"` -l 6 -r)
        mysql -u$SQL_USER -p$SQL_PASSWORD -Dweb_db -s -e "insert into ssserver(port,password,type,create_time) values ($PORT,\"$PASSWORD\",$TYPE,current_timestamp) on duplicate key update password=\"$PASSWORD\" ,type=$TYPE;"
        echo ===== $PORT $PASSWORD =====
    fi
    PORT=$((PORT+1))
done


