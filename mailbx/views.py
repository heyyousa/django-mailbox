from django.shortcuts import render
from django.core.paginator import Paginator
from mailbx.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

# Create your views here.

# 检查登录状态装饰器
def checklogin(fn):
    def wrap(request, *args, **kwargs):
        userid = request.COOKIES.get('userid')
        if not userid:
            return HttpResponseRedirect('/login')

        return fn(request, *args, **kwargs)

    return wrap

# 调取用户信息的函数,返回user实例
def uinfo(request):
    userid=request.COOKIES.get('userid')
    user=Userinfo.objects.get(id=userid)
    return user

def mainpage(request):
    return render(request,'mailbx/main.html',locals())

