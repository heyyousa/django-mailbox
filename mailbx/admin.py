from django.contrib import admin
from .models import *
# Register your models here.

class UserinfoManager(admin.ModelAdmin):
    list_display = ['id','nickname','password','is_active']

admin.site.register(Userinfo,UserinfoManager)


class EmailinfoManager(admin.ModelAdmin):
    list_display = ['title','content','poster','recipient','is_active']

admin.site.register(Emailinfo,EmailinfoManager)

class CommentsManager(admin.ModelAdmin):
    list_display = ['content','commentator','is_active','email_index']

admin.site.register(Comments,CommentsManager)