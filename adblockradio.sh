#!/bin/bash

DAEMON=adblockradio.py
PIDFILE=/tmp/adblockradio.lock

. /lib/lsb/init-functions

case "$1" in
    start)
        /usr/bin/python3 $DAEMON --daemon
    ;;
    stop)
        for pid in $(ps x | grep -v "grep" | grep adblockradio.py | awk '{print $1}')
        do
            if [[ $pid =~ ^-?[0-9]+$ ]]; then
                # Send SIGTERM
                kill $pid

                sleep 1

                # Send SIGTERM again
                kill $pid
            fi
        done
    ;;
    *)
        echo "usage: adblockradio.sh {start|stop}"
        exit 1
    ;;
esac

exit 0
