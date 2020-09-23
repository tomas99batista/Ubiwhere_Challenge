#!/bin/bash

if [ "$DATABAS" = "postgis" ]
then
    echo "Waiting for postgis..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "Postgis started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"
