from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from mailbx.models import *
import json


def to_login(request):
    return render(request, 'login.html')


def login(request):
    if request.method == "GET":
        userid = request.COOKIES.get('userid')
        if not userid:
            return render(request, 'login.html')
        else:
            # 登陆业务块
            message = '已有用户登录邮箱，关闭浏览器重新登录'
            return render(request, 'mailbx/error.html', locals())

    elif request.method == "POST":  # 接收前端的ajax请求并获取数据
        userid = request.POST.get('userid')
        userpsw = request.POST.get('userpsw')

        # 检测账号是否存在
        try:
            user = Userinfo.objects.get(Q(id=userid))
        except Exception as e:
            jsondata = {'status': 2, 'msg': '账号不存在'}  # 状态码0：账密正确，1：账密不对，2：账号不存在，3：账号被禁用
            return JsonResponse(jsondata)

        if not user.is_active:
            jsondata = {'status': 3, 'msg': '账号被禁用'}  # 数据包含状态status和消息msg或重定向url redirct
            return JsonResponse(jsondata)

        # 登陆业务块
        if userid == user.id and userpsw == user.password and user.is_dean == 0:
            jsondata = {'status': 0}  # 账密正确登陆主页并设置cookie
            jsresp = JsonResponse(jsondata)
            jsresp.set_cookie('userid', userid)
            return jsresp
        elif userid == user.id and userpsw == user.password and user.is_dean == 1:
            jsondata = {'status': 4}  # 院长身份登陆主页并设置cookie
            jsresp = JsonResponse(jsondata)
            jsresp.set_cookie('userid', userid)
            return jsresp
        else:
            jsondata = {'status': 1, 'msg': '账号或密码不对'}
            return JsonResponse(jsondata)


# 注册页面包括功能API
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        userid = request.POST.get('id')
        nickname = request.POST.get('nickname')
        userpsw = request.POST.get('psw')
        usericon = request.POST.get('mailbxurl')

        if Userinfo.objects.filter(id=userid):
            backdata = {'status': 1, 'msg': '账号已被注册'}
            return JsonResponse(backdata)

        if Userinfo.objects.filter(nickname=nickname):
            backdata = {'status': 2, 'msg': '昵称已存在'}
            return JsonResponse(backdata)

        try:
            Userinfo.objects.create(id=userid, nickname=nickname, sex='', password=userpsw, keshi='', duty='',
                                    iconurl=usericon)
        except Exception as e:
            print('--id或昵称写入重复 %s' % (e))
            backdata = {'status': 1, 'msg': '账号已被注册'}
            return JsonResponse(backdata)

        backdata = {'status': 0, 'msg': '注册成功'}

        return JsonResponse(backdata)


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

        Emailinfo.objects.create(index=mailindex, title='test' + str(i), content='content' + str(i), poster='001',
                                 recipient='刘书记')

    return HttpResponse('创建成功')


def create_comments(request):
    for i in range(0, 5):
        a = Comments.objects.last()
        if not bool(a):
            lindex = "0000000001"
            mailindex = lindex
        else:
            lindex = int(a.index)
            lindex += 1
            mailindex = str(lindex).zfill(10)

        Comments.objects.create(index=mailindex, content='comment' + str(i), commentator_id='001',
                                email_index_id='0000000001')

    return HttpResponse('创建成功')


def test(request):
    userid = request.GET.get('userid')
    userpsw = request.GET.get('userpsw')

    userid2 = request.FILES.get('userid')
    userpsw2 = request.POST.get('userpsw')
    print(request.body, request.POST, userpsw2)
    return HttpResponse(userpsw2)
