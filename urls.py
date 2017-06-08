# -*- coding: utf-8 -*-
"""
urls config
"""
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()
from django.conf import settings
# 公共URL配置
urlpatterns = patterns(
    '',
    # Django后台数据库管理
    url(r'^admin/', include(admin.site.urls)),
    # 用户登录鉴权--请勿修改
    url(r'^account/', include('account.urls')),
    # 应用功能开关控制--请勿修改
    url(r'^app_control/', include('app_control.urls')),
    # 在home_application(根应用)里开始开发你的应用的主要功能
    url(r'^', include('home_application.urls')),
    # 组件样例
    url(r'^test_component/', include('test_component.urls')),
    # 后台任务样例
    url(r'^test_celery/', include('test_celery.urls')),
    # 通用Tags样例
    url(r'^test_app_tags/', include('test_app_tags.urls')),
)


handler404 = 'error_pages.views.error_404'
handler500 = 'error_pages.views.error_500'
handler403 = 'error_pages.views.error_403'
handler401 = 'error_pages.views.error_401'
