# -*- coding: utf-8 -*-
from django.db import models


class TimingTaskRecord(models.Model):
    """
    定时任务执行记录
    """
    username = models.CharField(u"用户", max_length=64)
    title = models.TextField(u"消息标题", blank=True, null=True)
    content = models.TextField(u"消息内容", blank=True, null=True)
    create_time = models.DateTimeField(u"任务创建时间", blank=True, null=True)
    excute_time = models.DateTimeField(u"执行时间", blank=True, null=True)
    is_excuted = models.IntegerField(u"是否执行", default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"定时任务执行记录"
        verbose_name_plural = u"定时任务执行记录"


class PeroidTaskRecord(models.Model):
    """
    周期任务纪录
    """
    excute_param = models.TextField(u"任务执行参数")
    excute_result = models.TextField(u"任务执行结果")
    excute_time = models.DateTimeField(u"任务执行时间", auto_now_add=True)
    periodic_task_id = models.IntegerField(u"周期性任务的id", default=0)

    def __unicode__(self):
        return '%s--%s--%s' % (self.periodic_task_id, self.excute_param, self.excute_time)

    class Meta:
        verbose_name = u"周期性任务执行记录"
        verbose_name_plural = u"周期性任务执行记录"
        ordering = ['-excute_time']
