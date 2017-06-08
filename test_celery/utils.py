# -*- coding: utf-8 -*-
from djcelery.models import PeriodicTask

from test_celery.constants import TASK


def get_peroid_task_detail(task_id):
    """
    @summary: 查询周期任务和相关参数
    @param task_id:  周期任务id
    @return: {
           'task_args': 任务args参数,
           'task_kwargs': 任务kwargs参数,
           'cron_schedule':CrontabSchedule
           }
    """
    #  查询周期任务的信息
    try:
        period_task = PeriodicTask.objects.get(id=task_id)
        task = period_task.task
        task_args = period_task.args
        task_kwargs = period_task.kwargs
        cron_schedule = period_task.crontab   # 周期时间参数
    except:
        task = TASK
        task_args = '[]'
        task_kwargs = '{}'
        cron_schedule = None
    task_info = {
        'task_id': task_id,
        'task': task,
        'task_args': task_args,
        'task_kwargs': task_kwargs,
        'cron_schedule': cron_schedule
    }
    return task_info
