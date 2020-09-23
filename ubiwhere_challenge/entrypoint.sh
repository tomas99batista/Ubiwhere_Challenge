#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py makemigrations ubiwhere_challenge_app
python manage.py migrate
#python manage.py loaddata loaddata.json
python manage.py collectstatic --no-input --clear

exec "$@"