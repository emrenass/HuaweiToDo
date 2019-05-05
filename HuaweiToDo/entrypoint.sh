#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('user1', 'user1@example.com', 'pass')" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_superuser('user2', 'user2@example.com', 'pass')" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_superuser('user3', 'user3@example.com', 'pass')" | python manage.py shell
python manage.py collectstatic --no-input --clear

exec "$@"