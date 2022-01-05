from mailbx import views
from django.urls import path

urlpatterns = [
    path('main/', views.mainpage),  # 返回员工主页
    path('logout/', views.logout),  # 注销
    path('receive/', views.receive),  # 院长收件箱页面
    # ------main页面非页面功能函数API---------
    path('mbe/', views.main_back_emails),  # 返回邮件json数据
    path('mbc/', views.main_back_comments),  # 返回评论json数据
    path('mwe/', views.main_write_email),  # 给院长写邮件
    path('aui/', views.alteruserinfo),  # 用户修改个人信息
    # ------receive页面非页面功能函数API--------
    path('rbe/', views.recevie_back_emails),  # 院长页面返回邮件json数据
    path('rbc/', views.recevie_back_comments),  # 院长页面返回评论和评论人json数据
    # ------全局使用的非功能函数API-----------
    path('mwc/', views.main_write_comment),  # 院长和用户写评论
    path('getallicons/', views.getallicons),  # 获取全部头像
    # ------管理员功能函数-----------------
    path('uni/',views.update_new_icons),  # 添加新头像url到数据库
]
