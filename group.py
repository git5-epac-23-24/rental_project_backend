import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_permission.settings')

import django

from django.contrib.auth.models import Group


GROUPS = ['owner', 'simple_user', 'super_admin']
MODELS = ['user']

for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)