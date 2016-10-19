#!/bin/sh

DAEMON=adblockradio.py
PIDFILE=/tmp/adblockradio.lock

. /lib/lsb/init-functions

case "$1" in
    start)
        /usr/bin/python3 $DAEMON --daemon
    ;;
    stop)
        for pid in $(ps x | grep adblockradio.py | awk '{print $1}'); do kill $pid; done
    ;;
    *)
        echo "usage: adblockradio.sh {start|stop}"
        exit 1
    ;;
esac

exit 0
