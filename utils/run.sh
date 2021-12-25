#!/bin/bash

if [ -z ${PORT+x} ]; then PORT=80;  fi

python ./manage.py migrate --noinput
gunicorn backend.wsgi:application --bind 0.0.0.0:"$PORT"
