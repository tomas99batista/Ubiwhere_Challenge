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

echo "--- LOADING DATA ---"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_user('userteste', 'userteste@example.com', 'userteste')" | python manage.py shell
python manage.py loaddata loaddata.json

echo "--- TESTS ---"

python3 manage.py test ubiwhere_challenge_app/tests/

echo "--- TESTS DONE ---"

python manage.py collectstatic --no-input --clear

exec "$@"