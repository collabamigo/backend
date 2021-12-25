#!/bin/bash

: ${PORT:=80}

python ./manage.py migrate --noinput
gunicorn backend.wsgi:application --bind 0.0.0.0:"$PORT"
