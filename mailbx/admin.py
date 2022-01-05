from django.contrib import admin
from .models import *



# Register your models here.

# 用户信息表管理类
class UserinfoManager(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'password', 'is_active']
    search_fields = ['id','nickname']

admin.site.register(Userinfo, UserinfoManager)


# 邮件表管理类
class EmailinfoManager(admin.ModelAdmin):
    list_display = ['title', 'content', 'poster', 'recipient', 'is_active','index']
    search_fields = ['index']

admin.site.register(Emailinfo, EmailinfoManager)


# 评论表管理类
class CommentsManager(admin.ModelAdmin):
    list_display = ['content', 'commentator', 'is_active', 'email_index_id']


admin.site.register(Comments, CommentsManager)


# 头像表管理类
class UsericonsManager(admin.ModelAdmin):
    list_display = ['index', 'is_active']

admin.site.register(Usericons, UsericonsManager)
