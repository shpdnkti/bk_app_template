# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_mako_context, render_json


def index(request):
    """
    组件样例页面
    """
    return render_mako_context(request, '/test_component/index.html')


def app_list(request):
    """
    获取业务
    """
    # 默认从django settings中获取APP认证信息：应用ID和应用TOKEN
    # 默认从django request中获取用户登录态bk_token
    client = get_client_by_request(request)
    # 组件参数
    kwargs = {}
    result = client.cc.get_app_list(kwargs)
    return render_json(result)
