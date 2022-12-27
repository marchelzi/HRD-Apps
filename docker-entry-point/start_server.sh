#!/usr/bin/env bash
# start-server.sh
cd web_apps

DB_WAIT_TIMEOUT=${DB_WAIT_TIMEOUT-3}
MAX_DB_WAIT_TIME=${MAX_DB_WAIT_TIME-30}
CUR_DB_WAIT_TIME=0

while ! ./manage.py migrate --no-input 2>&1 && [ "${CUR_DB_WAIT_TIME}" -lt "${MAX_DB_WAIT_TIME}" ]; do
  echo "⏳ Waiting on DB... (${CUR_DB_WAIT_TIME}s / ${MAX_DB_WAIT_TIME}s)"
  sleep "${DB_WAIT_TIMEOUT}"
  CUR_DB_WAIT_TIME=$(( CUR_DB_WAIT_TIME + DB_WAIT_TIMEOUT ))
done
if [ "${CUR_DB_WAIT_TIME}" -ge "${MAX_DB_WAIT_TIME}" ]; then
  echo "❌ Waited ${MAX_DB_WAIT_TIME}s or more for the DB to become ready."
  exit 1
fi
./manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate --no-input
python manage.py remove_stale_contenttypes --no-input
cp -r staticfiles/* core/static/

if [ "$WORKER_ONLY" == "1" ];then
  rm /etc/supervisor/conf.d/task_beat_celery.conf
  rm /etc/supervisor/conf.d/task_gunicorn.conf
fi
if [ "$SCHEDULER_ONLY" == "1" ];then
  rm /etc/supervisor/conf.d/task_gunicorn.conf
  rm /etc/supervisor/conf.d/task_celery.conf
fi
if [ "$WEB_ONLY" == "1" ];then
  rm /etc/supervisor/conf.d/task_beat_celery.conf
  rm /etc/supervisor/conf.d/task_celery.conf
  nginx
fi
if [ "$FULL_VER" == "1" ];then
    nginx
fi
exec $@