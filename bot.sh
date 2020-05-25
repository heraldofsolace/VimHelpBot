#!/bin/bash

PIDFILE=/var/run/VimHelpBot.pid

case $1 in
   start)
       # Launch bot as a detached process
       python3 ./bot.py >> /tmp/bot.log 2>&1 &
       # Get its PID and store it
       echo $! > ${PIDFILE} 
   ;;
   stop)
      kill `cat ${PIDFILE}`
      # remove the PID file
      rm ${PIDFILE}
   ;;
   *)
      echo "usage: bot.sh {start|stop}" ;;
esac
exit 0
