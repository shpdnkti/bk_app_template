# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'test_app_tags.views',
    (r'^$', 'index'),
)
