# !/bin/bash
export FREEWEB_TASK_PATH=$(cd `dirname $0`;pwd)
source $FREEWEB_TASK_PATH/config.sh


if [ $1 -eq 0 ] ; then
    PRE=ssserver6
elif [ $1 -eq 1 ] ; then
    PRE=ssserver7
elif [ $1 -eq 2 ] ; then
    PRE=ssserver8
else
    exit 0
fi


# 删除旧进程
pkill -9 -f "/usr/local/bin/ssserver -c $FREEWEB_TASK_PATH/data/"$PRE 


# 生成端口密码
/bin/bash $FREEWEB_TASK_PATH/genports.sh $1


# 删除旧的配置文件
rm $FREEWEB_TASK_PATH/data/$PRE*.json

# 生成新的配置文件
/usr/bin/env python2.7 $FREEWEB_TASK_PATH/genconfig.py $1



# 启动新进程
for path in `ls $FREEWEB_TASK_PATH/data/$PRE*.json`;do
    if [ $IS_SERVER == true ] ;then
        /usr/local/bin/ssserver -c  $path -d start
        sleep 1
        # 检查是否正确启动,写入数据库
        success_load=`pgrep -f "/usr/local/bin/ssserver -c $path" `
        if [ -n "$success_load" ] ; then
            echo `date` : SUCCESS:$path,pid=$success_load
            state=1
        else
            echo `date` : ERROR:$path
            state=-1
        fi
        mysql -u$SQL_USER -p$SQL_PASSWORD -Dweb_db -s -e "update ssserver set state=$state where port=${path:(-9):4};"
    else
        echo  pretend ssserver run: $path
        mysql -u$SQL_USER -p$SQL_PASSWORD -Dweb_db -s -e "update ssserver set state=1 where port=${path:(-9):4};"
    fi
done


# 更新防火墙规则
# 700/s 相当于1000KB/s
if [ $1 -eq 0 ];then
    /sbin/iptables -F ssserver6
    /sbin/iptables -A ssserver6 -p tcp -m quota --quota $P_TOTAL_QUOTA -m limit --limit 700/s --limit-burst 100 -j ACCEPT 
    /sbin/iptables -A ssserver6 -p tcp -j DROP
    echo `date` : "flushed iptables ssserver6" 
elif [  $1 -eq 1 ] ; then
    /sbin/iptables -F ssserver7
    /sbin/iptables -A ssserver7 -p tcp -m quota --quota $L_TOTAL_QUOTA  -m limit --limit 700/s --limit-burst 100 -j ACCEPT 
    /sbin/iptables -A ssserver7 -p tcp -j DROP
    echo `date` : "flushed iptables ssserver7"
# 对于捐助用户，使用更宽泛的规则
elif [ $1 -eq 2  ] ; then 
    /sbin/iptables -F ssserver8
    for path in `ls $FREEWEB_TASK_PATH/data/$PRE*.json`;do
       /sbin/iptables -A ssserver8 -p tcp --dport ${path:(-9):4} -m  quota --quota $D_PER_QUOTA -m limit --limit 700/s --limit-burst 100 -j ACCEPT 
       /sbin/iptables -A ssserver8 -p tcp --sport ${path:(-9):4} -m  quota --quota $D_PER_QUOTA -m limit --limit 700/s --limit-burst 100 -j ACCEPT 
       /sbin/iptables -A ssserver8 -p tcp --dport ${path:(-9):4} -j DROP
       /sbin/iptables -A ssserver8 -p tcp --sport ${path:(-9):4} -j DROP
    done
    echo `date` : "flushed iptables ssserver8"
else 
    echo `date` : " ERROR flushed iptables" 
fi


