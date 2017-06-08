# -*- coding: utf-8 -*-
from common.mymako import render_mako_tostring
from blueking.component.shortcuts import get_client_by_request


def cc_app_select(context, px='300'):
    """
    @summary: 业务选择框（下拉）
    @param px: 下拉框的width像素值 (类型：string or int)
    @usage: 在模板页面加入 ： <%namespace name="tags_cc" module="tags.cc"/>
                                    然后添加：
                            ${ tags_cc.cc_app_select('300') }   有初始值 (支持字符串)
                            ${ tags_cc.cc_app_select(300) }    有初始值 (支持整型)
                        or
                            ${ tags_cc.cc_app_select() }  无初始值
    """
    request = context._kwargs.get('request', {})
    # 创建调用组件的通用client
    client = get_client_by_request(request)
    # 组件参数
    result = client.cc.get_app_list({})
    data = result.get('data', [])
    app_list = [{'id': i['ApplicationID'], 'text': i['ApplicationName']} for i in data]
    width_px = "width:%spx" % px
    ctx = {
        'app_list': app_list,
        'width_px': width_px,
    }
    return render_mako_tostring('tags/cc/cc_app_select.html', ctx)
