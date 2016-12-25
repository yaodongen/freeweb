


PORT=9000

if [ x$1 == x ] ; then
    echo "输入start stop kill restart state"
    exit -1
elif [ $1 = "start" ] ; then
    rm err.log
    nohup python main.py -port=$PORT > err.log 2>&1 &
elif [ $1 = "stop" -o $1 = "kill" ] ; then
    pkill -f "python main.py -port=$PORT"
elif [ $1 = "restart" ]; then
    pkill -f "python main.py -port=$PORT"
    rm err.log
    nohup python main.py -port=$PORT > err.log 2>&1 &
elif [ $1 = "state" ]; then
    ps -ef|grep  "python main.py -port=$PORT"
    
else 
    echo "输入start stop kill restart state"
    exit -1
fi

