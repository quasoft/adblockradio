#!/bin/bash

DAEMON=adblockradio.py
PIDFILE=/tmp/adblockradio.lock

. /lib/lsb/init-functions

case "$1" in
    start)
        if [ ! -f $PIDFILE ]; then
            touch $PIDFILE
            /usr/bin/python3 $DAEMON --console
        fi
    ;;
    stop)
        for pid in $(ps x | grep -v "grep" | grep adblockradio.py | awk '{print $1}')
        do
            if [[ $pid =~ ^-?[0-9]+$ ]]; then
                # Send SIGINT
                kill -INT $pid

                # Send SIGTERM
                kill $pid
            fi
        done

        rm $PIDFILE
    ;;
    *)
        echo "usage: adblockradio.sh {start|stop}"
        exit 1
    ;;
esac

exit 0
