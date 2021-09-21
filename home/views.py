from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from mailbx.models import *


def login(request):
    if request.method=="GET":
        return render(request, 'home.html')

    elif request.method == "POST":
        userid=request.POST.get('userid')
        userpsw=request.POST.get('userpsw')

        if userid=='' or userpsw=='':
            return render(request,'home.html')

        user=Userinfo.objects.get(id=userid)

        if not user.is_active:
            return HttpResponse('账号被禁用')

        if userid==user.id and userpsw==user.password:
            responds=redirect('/mailbx/main')
            responds.set_cookie('userid',user.id)
            responds.set_cookie('userpsw',user.password)
            return responds
        else:
            return HttpResponse('账号密码不对')

def create_user(request):
    Userinfo.objects.create(id='001',name='王豪',sex='男',password='123',keshi='信息科',duty='职员')
    return HttpResponse('创建成功')

def create_mail(request):
    for i in range(0, 40):
        a = Emailinfo.objects.last()
        if not bool(a):
            lindex = "0000000001"
            mailindex = lindex
        else:
            lindex = int(a.index)
            lindex += 1
            mailindex = str(lindex).zfill(10)

        Emailinfo.objects.create(index=mailindex,title='test'+str(i),content='content'+str(i),poster='001',recipient='刘书记')

    return HttpResponse('创建成功')