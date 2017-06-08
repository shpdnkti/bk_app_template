# -*- coding: utf-8 -*-
from django.contrib import admin
from test_celery.models import TimingTaskRecord


admin.site.register(TimingTaskRecord)
