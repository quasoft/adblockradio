#!/bin/sh

DAEMON=adblockradio.py
PIDFILE=/tmp/adblockradio.lock

. /lib/lsb/init-functions

case "$1" in
    start)
        /usr/bin/python3 $DAEMON
    ;;
    stop)
        PID=`ps x | grep adblockradio.py | head -1 | awk '{print $1}'`
        kill $PID
    ;;
    *)
        echo "usage: adblockradio.sh {start|stop}"
        exit 1
    ;;
esac

exit 0
