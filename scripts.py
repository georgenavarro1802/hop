#!/usr/bin/env python
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

your_djangoproject_home=os.path.split(BASE_DIR)[0]

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'hop.settings'

import django
django.setup()

from app.models import *


if __name__ == '__main__':

    # for work in Works.objects.filter(created_by__isnull=True):
    #     if work.id in [114, 115, 116, 133]:
    #         work.created_by_id = 37     # victor_hotwire
    #     else:
    #         work.created_by_id = 25     # hop_dispatch
    #     work.save()
    #
    #     print('Update created by: {}'.format(work.id))

    # Works.objects.filter(created_by_id=37).update(created_by_id=30)
    print('Updated User - Work')