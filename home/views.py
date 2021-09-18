from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from mailbx.models import *


def login(request):
    if request.method=="GET":
        return render(request, 'home.html', locals())

    elif request.method == "POST":
        userid=request.POST.get('userid')
        userpsw=request.POST.get('userpsw')

        if not userid or userpsw:
            return

        user=Userinfo.objects.get(id=userid)

        if not user.is_active:
            return HttpResponse('账号被禁用')

        if userid==user.id and userpsw==user.password:
            responds=redirect('/mailbx/mainpage')
            responds.set_cookie('userid',user.id)
            responds.set_cookie('userpsw',user.password)
            return responds
        else:
            return HttpResponse('账号密码不对')

