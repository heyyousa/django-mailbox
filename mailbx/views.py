from django.shortcuts import render,redirect
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
    emails=Emailinfo.objects.filter(poster='001')

    paginator=Paginator(emails,10)
    page_num=request.GET.get('page',1)
    c_page=paginator.page(int(page_num))

    return render(request,'mailbx/main.html',locals())

def logout(request):
    resp=redirect('/login')
    resp.delete_cookie('userid')
    resp.delete_cookie('userpsw')
    return resp

def wemail(request):
    return render(request,'mailbx/wemail.html')