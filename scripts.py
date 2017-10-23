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

    # Delete examples works
    for work in Works.objects.filter(id__in=[58, 80, 88, 87, 86, 85, 84]):
        if work.workstypes_set.exists():
            work.workstypes_set.all().delete()

        print('Deleted work: {}'.format(work.id))
        work.delete()
