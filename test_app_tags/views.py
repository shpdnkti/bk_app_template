# -*- coding: utf-8 -*-
from common.mymako import render_mako_context


def index(request):
    return render_mako_context(request, "/test_app_tags/index.html")
