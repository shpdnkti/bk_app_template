# -*- coding: utf-8 -*-
import json
import time
import datetime

from djcelery.models import PeriodicTask

from common.mymako import render_mako_context, render_json
from common.log import logger
from test_celery.models import TimingTaskRecord, PeroidTaskRecord
from test_celery.tasks import send_msg
from test_celery.constants import TASK
from test_celery.utils import get_peroid_task_detail
from test_celery.celery_utils import add_peroid_task, edit_peroid_task_by_id, del_peroid_task_by_id


def index(request):
    """
    普通后台任务页面
    """
    return render_mako_context(request, '/test_celery/index.html')


def excute_general_task(request):
    """
    执行普通任务或定时任务
    @note: 调用celery任务方法:
            task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
            task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
            delay(): 简便方法，类似调用普通函数
            apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                  详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    username = request.user.username
    msg_param = {
        'message': request.POST.get('message')
    }
    do_schedule = int(request.POST.get('do_schedule', 0))
    schedule_time = request.POST.get('schedule_time', '').replace('&nbsp;', ' ') if do_schedule else ''
    # 定时时间格式化
    if schedule_time:
        try:
            schedule_time = datetime.datetime.strptime(schedule_time, '%Y-%m-%d %H:%M:%S')
        except Exception, e:
            msg = u"定时时间(%s)格式错误:%s" % (schedule_time, e)
            logger.error(msg)
            return render_json({'result': False, 'message': msg})
    # 任务执行参数
    title = u"蓝鲸开发样例——定时任务" if do_schedule else u"蓝鲸开发样例——普通后台任务"
    msg_param['schedule_time'] = schedule_time
    # 写入数据库
    timing_record = TimingTaskRecord.objects.create(username=username,
                                                      title=title,
                                                      content=msg_param.get('message', ''),
                                                      create_time=datetime.datetime.now(),
                                                      is_excuted=0)
    # 执行 celery 任务
    if schedule_time:
        # 后台定时执行
        send_msg.apply_async(args=[timing_record.id], kwargs=msg_param, eta=schedule_time)
    else:
        # 后台任务
        send_msg.delay(timing_record.id, **msg_param)
    return render_json({'result': True, 'record_id': timing_record.id})


def poll_general_task_status(request):
    """
    轮询普通任务状态
    """
    record_id = request.GET.get('record_id', '')
    try:
        record = TimingTaskRecord.objects.get(id=record_id)
        if record.is_excuted == 0:
            result = {'status': 2, 'message': u"未执行定时任务"}
        else:
            result = {'status': 1, 'title': record.title, 'content': record.content.replace('\n', '<br>')}
    except TimingTaskRecord.DoesNotExist:
        logger.error(u"任务记录[%s]不存在" % record_id)
        result = {'status': 0, 'message': u"轮询定时任务状态出错"}
    return render_json(result)


def periodic_task(request):
    """
    周期任务页面
    """
    return render_mako_context(request, '/test_celery/periodic_task.html')


def periodic_task_list(request):
    """
    周期任务列表
    """
    draw = int(request.GET.get('draw'))
    # 每页记录数
    record_num = int(request.GET.get('length'))
    # 分片起始位置
    start = int(request.GET.get('start'))
    # 分片结束位置
    end = start + record_num
    peroid_tasks = PeriodicTask.objects.filter(task=TASK)
    total = peroid_tasks.count()
    task_set = peroid_tasks[start:end]
    data_list = []
    for task in task_set:
        data_list.append({
            'id': task.id,
            'task': task.task,
            'args': task.args,
            'kwargs': task.kwargs,
            'crontab': str(task.crontab)
        })
    result = {'data': data_list, 'recordsTotal': total, 'recordsFiltered': total, 'draw': draw, 'error': ''}
    return render_json(result)


def periodic_task_edit(request, task_id):
    """
    启动、编辑任务页面，显示任务详情
    @todo: 通过task_id获取任务
    """
    task_info = get_peroid_task_detail(task_id)
    # 解析任务参数
    task_args = task_info.get('task_args', [])
    # 解析任务参数
    try:
        task_args = json.loads(task_args)
        task_args1 = task_args[0]
        task_args2 = task_args[1] if len(task_args) > 1 else 0
    except:
        task_args1 = 0
        task_args2 = 0
    task_info['task_args1'] = task_args1
    task_info['task_args2'] = task_args2
    return render_mako_context(request, '/test_celery/periodic_task_edit.html', task_info)


def check_peroid_task(requets):
    """
    检查任务参数是否已存在（相同任务，相同参数的周期任务只允许有一条记录）
    相同任务，相同参数、不同调度策略的任务可以通过crontab策略的配置合并为一个任务
    """
    task = requets.POST.get('task', TASK)
    task_args_old = requets.POST.get('task_args_old', '[]')
    task_args1 = requets.POST.get('task_args1', '')
    task_args2 = requets.POST.get('task_args2', '')
    flag = False
    message = ''
    # 任务参数
    try:
        task_args1 = int(task_args1)
        task_args2 = int(task_args2)
        task_args_list = [task_args1, task_args2]
        task_args = json.dumps(task_args_list)
    except:
        logger.error(u"解析任务参数出错, task_args1;%s, task_args2;%s" %
                     (task_args1, task_args2))
    else:
        # 参数未改变，则不用检查
        if task_args_old == task_args:
            flag = True
        else:
            count = PeriodicTask.objects.filter(
                task=task, args=task_args).count()
            if count == 0:
                flag = True
    if not flag:
        message = "任务名为：%s\n任务参数为：X:%s,Y:%s\n的周期任务已存在！" % (
            task, task_args1, task_args2)
    return render_json({'result': flag, 'message': message})


def save_task(request):
    """
    创建/编辑周期性任务 并 运行
    """
    periodic_task_id = request.POST.get('periodic_task_id', '0')
    params = request.POST.get('params', {})
    try:
        params = json.loads(params)
        add_param = params.get('add_task', {})
    except:
        msg = u"参数解析出错"
        logger.error(msg)
        result = {'result': False, 'message': msg}
        return render_json(result)
    task_args1 = add_param.get('task_args1', '0')
    task_args2 = add_param.get('task_args2', '0')
    # 任务参数
    try:
        task_args1 = int(task_args1)
        task_args2 = int(task_args2)
        task_args_list = [task_args1, task_args2]
        task_args = json.dumps(task_args_list)
    except:
        task_args = '[0,0]'
        logger.error(u"解析任务参数出错")
    #  周期参数
    minute = add_param.get('minute', '*')
    hour = add_param.get('hour', '*')
    day_of_week = add_param.get('day_of_week', '*')
    day_of_month = add_param.get('day_of_month', '*')
    month_of_year = add_param.get('month_of_year', '*')
    # 创建周期任务时，任务名必须唯一
    now = int(time.time())
    task_name = "%s_%s" % (TASK, now)
    if periodic_task_id == '0':
        # 创建任务并运行
        res, msg = add_peroid_task(TASK, task_name, minute, hour,
                                   day_of_week, day_of_month,
                                   month_of_year, task_args)
    else:
        # 修改任务
        res, msg = edit_peroid_task_by_id(periodic_task_id, minute, hour,
                                          day_of_week, day_of_month,
                                          month_of_year, task_args)
    return render_json({'result': res, 'message': msg})


def del_peroid_task(request):
    """
    删除周期性任务
    """
    task_id = request.POST.get('id')
    res, msg = del_peroid_task_by_id(task_id)
    if res:
        msg = u"任务删除成功"
    return render_json({'result': res, 'message': msg})


def periodic_task_record(request, task_id):
    """
    显示周期性任务执行记录页面
    """
    #  查询周期任务的信息
    task_info = get_peroid_task_detail(task_id)
    return render_mako_context(request, '/test_celery/periodic_task_record.html', task_info)


def get_periodic_task_records(request, periodic_task_id):
    """
    获取周期性任务执行记录
    @todo: 查找指定任务的执行记录
    """
    draw = int(request.GET.get('draw'))
    # 每页记录数
    record_num = int(request.GET.get('length'))
    # 分片起始位置
    start = int(request.GET.get('start'))
    # 分片结束位置
    end = start + record_num
    peroid_tasks = PeroidTaskRecord.objects.all()
    if periodic_task_id:
        peroid_tasks = peroid_tasks.filter(periodic_task_id=periodic_task_id)
    total = peroid_tasks.count()
    task_set = peroid_tasks[start:end]
    data_list = []
    for task in task_set:
        data_list.append({
            'excute_time': task.excute_time.strftime('%Y-%m-%d %H:%M:%S') if task.excute_time else '--',
            'excute_result': task.excute_result,
            'excute_param': task.excute_param
        })
    result = {'data': data_list, 'recordsTotal': total, 'recordsFiltered': total, 'draw': draw, 'error': ''}
    return render_json(result)
