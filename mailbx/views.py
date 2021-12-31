import json
from django.core import serializers
from django.shortcuts import render, redirect
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
    userid = request.COOKIES.get('userid')
    user = Userinfo.objects.get(id=userid)
    return user


# 主页
def mainpage(request):
    if request.COOKIES.get('userid'):
        userid = request.COOKIES.get('userid')

        user = Userinfo.objects.get(id=userid)

        # paginator=Paginator(emails,10)
        # page_num=request.GET.get('page',1)
        # c_page=paginator.page(int(page_num))

        return render(request, 'mailbx/main.html', locals())
    else:
        return redirect('/login/')


# 院长主页
def receive(request):
    if request.COOKIES.get('userid'):
        deanid = request.COOKIES.get('userid')

        dean = Userinfo.objects.get(id=deanid)

        # paginator=Paginator(emails,10)
        # page_num=request.GET.get('page',1)
        # c_page=paginator.page(int(page_num))

        return render(request, 'mailbx/receive.html', locals())
    else:
        return redirect('/login/')


# 注销功能，cookie的设置都交给后端
def logout(request):
    resp = HttpResponse('1')
    resp.delete_cookie('userid')
    return resp


# ————————main非页面功能函数API——————————————
# 返回邮件json数据
def main_back_emails(request):
    userid = request.COOKIES.get('userid')

    emails = Emailinfo.objects.filter(Q(poster=userid)).order_by('-created_time')

    jsondata = serializers.serialize('json', emails)
    # 用HttpResponse返回序列化好的数据，前端接收到用JSON.parse能转换成json格式

    return HttpResponse(jsondata)


# 返回指定邮件的评论，和院长主页共用一个api
def main_back_comments(request):
    email_id = request.GET.get('emailid')
    commentator_id = request.GET.get('commentatorId')

    # 新回复点击完更改flag为0的功能
    email = Emailinfo.objects.get(Q(index=email_id))
    if email.other_new_comment == 1:
        email.other_new_comment = 0
        email.save()

    commentator = Userinfo.objects.filter(id=commentator_id)
    commentatorjson = serializers.serialize('json', commentator)

    comments = Comments.objects.filter(Q(email_index=email_id))
    commentsjson = serializers.serialize('json', comments)

    data = {'comments': commentsjson, 'commentator': commentatorjson}

    return JsonResponse(data)


# 给院长写信件功能函数
def main_write_email(request):
    receiver = request.POST.get('receiver')
    title = request.POST.get('title')
    content = request.POST.get('content')
    poster_id = request.COOKIES.get('userid')
    receiver_id = ''

    if receiver == '刘炳芹':
        receiver_id = '111'
    elif receiver == '赵彬':
        receiver_id = '112'

    a = Emailinfo.objects.last()
    if not bool(a):
        lindex = "0000000001"
        emailindex = lindex
    else:
        lindex = int(a.index)
        lindex += 1
        emailindex = str(lindex).zfill(10)

    Emailinfo.objects.create(index=emailindex, title=title, content=content, poster=poster_id, recipient=receiver_id)

    return HttpResponse(0)


# 院长主页和用户主页评论功能
def main_write_comment(request):
    content = request.POST.get('content')
    commentator_id = request.COOKIES.get('userid')
    email_index = request.POST.get('email_id')

    user = Userinfo.objects.get(Q(id=commentator_id))

    a = Comments.objects.last()
    if not bool(a):
        lindex = "0000000001"
        cmtindex = lindex
    else:
        lindex = int(a.index)
        lindex += 1
        cmtindex = str(lindex).zfill(10)

    Comments.objects.create(index=cmtindex, content=content, commentator=user.nickname, commentator_id=commentator_id,
                            email_index_id=email_index)

    # 将邮件的新回复flag改为1，判断是否是两位院长，普通user改poster_new_comment，院长改other_new_comment
    email = Emailinfo.objects.get(Q(index=email_index))

    if user.name == '刘炳芹' or user.name == '赵彬':
        if email.other_new_comment != 1:
            email.other_new_comment = 1
            email.save()

        # 院长回复完将email_flag改为3已处理
        if email.email_flag != 3:
            email.email_flag = 3
            email.save()
    else:
        if email.poster_new_comment != 1:
            email.poster_new_comment = 1
            email.save()

        # 用户回复完将email_flag改为2未处理
        if email.email_flag != 2:
            email.email_flag = 2
            email.save()

    return HttpResponse(0)


# ————————recevie非页面功能函数API————————————
# 院长主页返回邮件数据
def recevie_back_emails(request):
    deanid = request.COOKIES.get('userid')

    emails = Emailinfo.objects.filter(Q(recipient=deanid)).order_by('-created_time')
    emailsdata = serializers.serialize('json', emails)

    # 将各个状态的邮件数量统计出来发给前端
    new_emails = Emailinfo.objects.filter(Q(email_flag=1)).count()
    new_reply = Emailinfo.objects.filter(Q(poster_new_comment=1)).count()
    # ↓防止未处理和新回复有重叠的部分，限制未处理为是未处理并且不是新回复的邮件为未处理的真实数量↓
    untreated_emails = Emailinfo.objects.filter(Q(email_flag=2) & Q(poster_new_comment=0)).count()
    did_emails = Emailinfo.objects.filter(Q(email_flag=3)).count()
    emailstatus = {'new_emails': new_emails, 'new_reply': new_reply, 'untreated_emails': untreated_emails,
                   'did_emails': did_emails}

    jsondata = {'emailstatus': emailstatus, 'emailsdata': emailsdata}

    return JsonResponse(jsondata)


def recevie_back_comments(request):
    email_id = request.GET.get('emailid')
    commentator_id = request.GET.get('commentatorId')

    # 院长主页上的新回复点击完更改flag为0的功能
    email = Emailinfo.objects.get(Q(index=email_id))
    if email.poster_new_comment == 1:
        email.poster_new_comment = 0
        email.save()
    # 新邮件点击完更改flag为2未处理的功能
    if email.email_flag == 1:
        email.email_flag = 2
        email.save()

    commentator = Userinfo.objects.filter(id=commentator_id)
    commentatorjson = serializers.serialize('json', commentator)

    comments = Comments.objects.filter(Q(email_index=email_id))
    commentsjson = serializers.serialize('json', comments)

    data = {'comments': commentsjson, 'commentator': commentatorjson}

    return JsonResponse(data)
