#!/bin/bash

cd /home/ubuntu/django/database_api
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
