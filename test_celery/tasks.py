# -*- coding: utf-8 -*-
import json
import datetime

from celery import task
from djcelery.models import PeriodicTask

from common.log import logger
from test_celery.models import TimingTaskRecord, PeroidTaskRecord
from test_celery.constants import TASK


@task()
def send_msg(record_id, **kwargs):
    """
    @summary: 改变消息记录内容和状态
    """
    try:
        message = kwargs.get('message')
        schedule_time = kwargs.get('schedule_time')
        record = TimingTaskRecord.objects.get(id=record_id)
        if schedule_time:
            content = u"定时时间：%s\n消息：%s" % (schedule_time, message)
        else:
            content = u"消息：%s" % message
        record.content = content
        record.excute_time = datetime.datetime.now()
        record.is_excuted = 1
        record.save()
        res = True
    except Exception, e:
        logger.error(u"执行（定时）后台任务出错：%s" % e)
        res = False
    return res


@task()
# @periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def add(x, y):
    """
    @summary: celery 示例任务
    @note: @periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))：每5分钟执行1次任务
              periodic_task 装饰器程序运行时自定触发定时任务
    """
    sums = x + y
    # 以下操作是保存任务的执行记录
    # 查询任务的对应的周期任务
    try:
        task = TASK
        args = [x, y]
        args = json.dumps(args)
        periodic_task = PeriodicTask.objects.filter(task=task, args=args)[0]
        periodic_task_id = periodic_task.id
    except:
        logger.error(u"查询任务的对应的周期任务出错")
        periodic_task_id = 0
    # 将执行记录保存到数据库中
    try:
        excute_param = "x:%s, y:%s" % (x, y)
        PeroidTaskRecord.objects.create(
            excute_param=excute_param,
            excute_result=sums,
            periodic_task_id=periodic_task_id
        )
    except:
        logger.error(u"保存周期性任务执行记录出错")
    return sums
