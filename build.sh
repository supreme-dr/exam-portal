#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# FORCE create or update the admin user
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u, created = User.objects.get_or_create(username='admin'); u.is_staff = True; u.is_superuser = True; u.set_password('emman12345'); u.save(); print('SUCCESS: Admin user is ready!')"