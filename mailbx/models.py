from django.db import models

# Create your models here.

# 用户信息表
class Userinfo(models.Model):
    id=models.CharField('工号',primary_key=True,max_length=6)
    name=models.CharField('姓名',max_length=10)
    sex=models.CharField('性别',max_length=2)
    password=models.CharField('密码',max_length=20)
    keshi=models.CharField('科室',max_length=14)
    duty=models.CharField('职务',max_length=10)
    created_time=models.DateTimeField('创建时间',auto_now_add=True)
    updated_time=models.DateTimeField('更新时间',auto_now=True)
    is_dean = models.BooleanField('是否院长', default=False)
    is_active=models.BooleanField('账号状态',default=True)
    ud_operator=models.CharField('操作人',max_length=10)

    class Meta:
        db_table='userinfo'
        verbose_name_plural='用户信息'

    def __str__(self):
        return '%s | %s | %s | %s | %s | %s | %s | %s'%(self.id,self.name,self.sex,self.keshi,self.duty,self.is_dean,self.is_active,self.ud_operator)

# email表
class Emailinfo(models.Model):
    index=models.CharField('索引',primary_key=True,max_length=10)
    title=models.CharField('标题',max_length=20)
    content=models.TextField('内容')
    poster=models.CharField('发帖人',max_length=20)
    recipient=models.CharField('收件人',max_length=20)
    is_anonymous=models.BooleanField('是否匿名',default=False)
    # 暂时用来获知是否回复信件↓
    comment_num=models.IntegerField('评论数',default=0)
    created_time=models.DateTimeField('创建时间',auto_now_add=True)
    updated_time=models.DateTimeField('更新时间',auto_now=True)
    is_active=models.BooleanField('帖子状态',default=True)
    operator=models.CharField('操作人',max_length=10)

    class Meta:
        db_table='emailinfo'
        verbose_name_plural='邮件信息表'

    def __str__(self):
        return '%s|%s|%s|%s|%s|%s|%s'%(self.title,self.poster,self.content,self.created_time,self.updated_time,self.is_active,self.operator)

# 评论表
class Comments(models.Model):
    index=models.CharField('索引',primary_key=True,max_length=10)
    email_index=models.ForeignKey(Emailinfo,null=True,blank=True,on_delete=models.SET_NULL)
    content=models.TextField('评论')
    commentator=models.CharField('评论人',max_length=20)
    floor=models.IntegerField('楼层',default=0)
    created_time=models.DateTimeField('创建时间',auto_now_add=True)
    updated_time=models.DateTimeField('更新时间',auto_now=True)
    is_active=models.BooleanField('评论状态',default=True)
    operator=models.CharField('操作人',max_length=10)

    class Meta:
        db_table='comments'
        verbose_name_plural='评论表'

    def __str__(self):
        return '%s|%s|%s|%s|%s|%s|%s'%(self.email_index,self.content,self.commentator,self.created_time,self.updated_time,self.is_active,self.operator)