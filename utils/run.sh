#!/bin/bash

set -e

: ${PORT:=80}

until cd /opt/deploy/collabamigo
do
    echo "Waiting for server volume..."
done

# Apply database migrations
echo "Waiting for db to be ready...."
#python manage.py makemigrations
if [[ $DEBUG == "True" ]] && [[ $DJANGO_TEST_SERVER == "True" ]];
then
    echo "Skipping migrate and collectstatic"
else
    python manage.py migrate
    python manage.py collectstatic --noinput
fi
# Collect static files


echo "------------------------------"
echo "DEBUG: " "$DEBUG"
echo "DJANGO_TEST_SERVER: " "$DJANGO_TEST_SERVER"
echo "------------------------------"

if [[ $DEBUG == "True" ]] && [[ $DJANGO_TEST_SERVER == "True" ]];
then
    NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python manage.py runserver 0.0.0.0:80
else
    gunicorn backend.wsgi:application --bind 0.0.0.0:"$PORT"
fi
