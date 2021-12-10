from mailbx import views
from django.urls import path

urlpatterns = [
    path('main/',views.mainpage),  # 返回员工主页
    path('logout/',views.logout),  # 注销
    path('wemail/',views.wemail),  #
    path('receive/',views.receive),  # 院长收件箱页面
    path('mbe/',views.main_back_emails),  # 返回邮件json数据
    path('mbc/',views.main_back_comments),  # 返回评论json数据
]