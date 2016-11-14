# !/bin/bash 
source ../config.sh

# 初始化iptables
# 统计输入输出的流量
# 注意一条语句最多包含15个端口
if [ x$1 = x ] ; then
    echo -e '请输入一个参数:\n 0 安装 1 删除'
    exit -1
elif [ $1 -eq 0 ] ; then

    echo "建立数据库和表..."
    mysql -u$SQL_USER -p$SQL_PASSWORD < database.sql
    echo "完成"

    echo "配置iptables ..."
    PORTS=$P_PORT
    for (( i=P_PORT+1;i<=P_M_PORT && i<P_PORT+P_NUM;++i  )) do PORTS=$PORTS,$i;done
    iptables -N $P_TABLE
    iptables -A OUTPUT -p tcp -m multiport --sports $PORTS -j $P_TABLE
    iptables -A INPUT -p tcp -m multiport --dports $PORTS -j $P_TABLE
    PORTS=$L_PORT
    for (( i=L_PORT+1;i<=L_M_PORT && i<L_PORT+L_NUM;++i  )) do PORTS=$PORTS,$i;done
    iptables -N $L_TABLE
    iptables -A OUTPUT -p tcp -m multiport --sports $PORTS -j $L_TABLE
    iptables -A INPUT -p tcp -m multiport --dports $PORTS -j $L_TABLE
    PORTS=$D_PORT
    for (( i=D_PORT+1;i<=D_M_PORT && i<D_PORT+D_NUM;++i  )) do PORTS=$PORTS,$i;done
    iptables -N $D_TABLE
    iptables -A OUTPUT -p tcp -m multiport --sports $PORTS -j $D_TABLE
    iptables -A INPUT -p tcp -m multiport --dports $PORTS -j $D_TABLE
    echo "完成"

elif [ $1 -eq 1 ] ; then

    echo "删除iptables ..."
    PORTS=$P_PORT
    for (( i=P_PORT+1;i<=P_M_PORT && i<P_PORT+P_NUM;++i  )) do PORTS=$PORTS,$i;done
    iptables -D OUTPUT -p tcp -m multiport --sports $PORTS -j $P_TABLE
    iptables -D INPUT -p tcp -m multiport --dports $PORTS -j $P_TABLE
    iptables -F $P_TABLE
    iptables -X $P_TABLE
    PORTS=$L_PORT
    for (( i=L_PORT+1;i<=L_M_PORT && i<L_PORT+L_NUM;++i  )) do PORTS=$PORTS,$i;done
    iptables -D OUTPUT -p tcp -m multiport --sports $PORTS -j $L_TABLE
    iptables -D INPUT -p tcp -m multiport --dports $PORTS -j $L_TABLE
    iptables -F $L_TABLE
    iptables -X $L_TABLE
    PORTS=$D_PORT
    for (( i=D_PORT+1;i<=D_M_PORT && i<D_PORT+D_NUM;++i  )) do PORTS=$PORTS,$i;done
    iptables -D OUTPUT -p tcp -m multiport --sports $PORTS -j $D_TABLE
    iptables -D INPUT -p tcp -m multiport --dports $PORTS -j $D_TABLE
    iptables -F $D_TABLE
    iptables -X $D_TABLE
    echo "完成"

else
    echo -e '请输入一个参数:\n 0 安装 1 删除'
    exit -1
fi




