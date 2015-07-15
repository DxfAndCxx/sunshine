#!/bin/sh


getpid(){
    PID=$(pgrep -f "python sweb.py")
    if [ "x$?" != "x0" ]
    then
        PID=''
    fi
    echo $PID
}


start()
{
    echo '\033[31m start ... \033[0m'

    PID=$(getpid)
    if [ "x$PID" != "x" ]
    then
        echo "\033[34m sweb.py is running"
        exit 0
    fi
    filepath=$(cd "$(dirname "$0")";pwd)
    cd $filepath
    nohup python sweb.py &
    sleep 1
}

stop()
{
    echo '\033[31m stop ... \033[0m'
    PID=$(getpid)
    while [ "x$PID" != "x" ]
    do
        for p in $PID;
        do
            kill $p
        done
        sleep 1
        PID=$(getpid)
    done
}

case $1 in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        echo "\033[31m restart ... \033[0m"
        stop
        start
        ;;
    status)
        getpid
        ;;
esac






