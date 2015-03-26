#!/bin/bash

warn () {
        echo 'try supervisorctl '
        exit 0
        }

VERSION='0.1'
usage()
{
    echo "Usage: $0 command module [localdev_name] num"
    echo "       command            start or stop or debug or list"
    echo "       module             online or dev or localdev"
    echo "       num                process num "
    echo "                            online default 8"
    echo "                            dev default 2"
}

echo "DMovie Service Boot Script Version($VERSION)"

if (($# == 0))
then
    usage
    exit
fi

cd ..

TIME=`date '+%Y-%m-%d_%H:%M:%S'`
CONFIG_PATH='conf/'

PROCESS_NUM=4

case $1 in
    start)
    warn
	COMMAND=1
	;;
    stop)
    warn
	COMMAND=2
	;;
    debug)
	COMMAND=3
	;;
    list)
    warn
	COMMAND=4
	;;
    *)
	usage
	exit 0
esac

case $2 in
    local)
	CONFIG_FILE=$2'_conf.py'
    LOG_PATH='../log'
	DEBUG_SERVICE_PORT=8910
	COMMAND=5
	;;
    dev)
    LOG_PATH="/alidata1/logs/dev/lms"
	MODULE=$2
	CONFIG_FILE='dev_lms.py'
	SERVICE_PORT=14400
	DEBUG_SERVICE_PORT=14410
	APP_PORT_BASE=14400
	PROCESS_NUM=2
	if (($# == 3))
	then
	    PROCESS_NUM=$3
	fi
	;;
    online)
    LOG_PATH="/alidata1/logs/online/lms"
	MODULE=$2
	CONFIG_FILE='online_lms.py'
	SERVICE_PORT=14500
	DEBUG_SERVICE_PORT=14510
	APP_PORT_BASE=14500
	PROCESS_NUM=4
	if (($# == 3))
	then
	    PROCESS_NUM=$3
	fi
	;;
    *)
        usage
        exit 0
esac

CONFIG=$CONFIG_PATH$CONFIG_FILE

echo "ConfigFile: $CONFIG"
echo "pid list:";ps aux | grep $CONFIG | grep -v 'grep'

if [[ $COMMAND -eq 4 ]]
then
    exit 0
fi

ps aux | grep $CONFIG | grep -v 'grep' | awk '{print $2}' | xargs kill -9

if [[ $COMMAND -eq 2 ]]
then
    echo 'exit success'
    exit 0
fi

if [[ $COMMAND -eq 3 ]]
then
    python dm.py --server_port=$DEBUG_SERVICE_PORT --app_port=$DEBUG_SERVICE_PORT --debug=True $CONFIG
    echo $DEBUG_SERVICE_PORT
    exit 0
fi

if [[ $COMMAND -eq 5 ]]
then
    python dm.py --app_port=$DEBUG_SERVICE_PORT --debug=True $CONFIG
    exit 0
fi

echo "Porcess Number: $PROCESS_NUM"

for i in `seq 1 $PROCESS_NUM`
do
    PORT=$((APP_PORT_BASE+i))
    echo "Start Process $i At Port $PORT"
    nohup python dm.py --app_port=$PORT --log_file_prefix=$LOG_PATH/lms.log.$PORT.$TIME $CONFIG > /dev/null &
done

# debug
nohup python dm.py --server_port=$DEBUG_SERVICE_PORT --app_port=$DEBUG_SERVICE_PORT

echo "new pid:";ps aux | grep $CONFIG | grep -v 'grep'
echo "Run Module: "$MODULE
echo "Service Port: "$SERVICE_PORT
echo "Service Debug Port: "$DEBUG_SERVICE_PORT
