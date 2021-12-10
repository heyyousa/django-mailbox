import json
from django.core import serializers
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from mailbx.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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

# 主页
def mainpage(request):
    if request.COOKIES.get('userid'):

        # paginator=Paginator(emails,10)
        # page_num=request.GET.get('page',1)
        # c_page=paginator.page(int(page_num))

        return render(request,'mailbx/main.html')
    else:
        return redirect('/login/')


# 院长主页
def receive(request):
    return render(request,'mailbx/receive.html')


# 注销功能，cookie的设置都交给后端
def logout(request):
    resp=HttpResponse('1')
    resp.delete_cookie('userid')
    return resp


def wemail(request):
    if request.method=='GET':
        if request.COOKIES.get('userid'):
            return render(request,'mailbx/wemail.html')
        else:
            return redirect('/login/')
    elif request.method=='POST':
        return


# ————————非页面函数————————————————
# 返回邮件json数据
def main_back_emails(request):
    userid = request.COOKIES.get('userid')

    emails = Emailinfo.objects.filter(Q(poster=userid))

    jsondata = serializers.serialize('json',emails)
    # 用HttpResponse返回序列化好的数据，前端接收到用JSON.parse能转换成json格式

    return HttpResponse(jsondata)

def main_back_comments(request):
    email_id=request.GET.get('emailid')
    comments=Comments.objects.filter(Q(email_index=email_id))

    jsondata = serializers.serialize('json',comments)

    return HttpResponse(jsondata)