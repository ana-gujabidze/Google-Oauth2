#!/bin/sh

python manage.py migrate --noinput --settings=core.settings
python manage.py makemigrations --noinput --settings=core.settings