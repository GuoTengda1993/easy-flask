#!/bin/bash

start() {
  if [ ! -d "logs" ]; then
      mkdir "logs"
  fi
  gunicorn -c start.py app:app
}

stop() {
  ps -fe|grep gunicorn|grep app|grep -v grep|gawk '{print $2}'|xargs kill
  echo "flask-demo stopped"
}

restart() {
  stop

  wn=`ps -fe|grep gunicorn|grep app|grep -v grep|wc -l`
  t=1
  while [ $wn -gt 0 ]; do
      echo "waiting, $t"
      echo "$wn"
      sleep 1
      if [ $t -gt 30 ]; then
          break
      fi
      ((t++))
      wn=`ps -fe|grep wsgi:app|grep -v grep|wc -l`
  done

  start
}

case "$1" in
start)
  start
  ;;
stop)
  stop
  ;;
restart)
  restart
  ;;
*)
  echo "Usage: $0 {start|stop|restart}"
  ;;
esac