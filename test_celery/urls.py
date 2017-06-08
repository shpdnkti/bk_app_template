# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'test_celery.views',
    # 普通任务也没
    (r'^$', 'index'),
    # 执行普通任务
    (r'^excute_general_task/$', 'excute_general_task'),
    # 轮询普通任务执行结果
    (r'^poll_general_task_status/$', 'poll_general_task_status'),
    # 周期任务页面
    (r'^periodic_task/$', 'periodic_task'),
    # 周期任务列表
    (r'^periodic_task_list/$', 'periodic_task_list'),
    # 新增或编辑周期任务
    (r'^periodic_task_edit/(?P<task_id>\d+)/', 'periodic_task_edit'),
    # 检查周期任务配置正确性
    (r'^check_peroid_task/$', 'check_peroid_task'),
    # 保存周期任务配置
    (r'^save_task/$', 'save_task'),
    # 删除周期任务
    (r'^del_peroid_task/$', 'del_peroid_task'),
    # 周期任务 执行记录
    (r'^periodic_task_record/(?P<task_id>\d+)/$', 'periodic_task_record'),
    (r'^get_periodic_task_records/(?P<periodic_task_id>\d+)/$', 'get_periodic_task_records'),
)
