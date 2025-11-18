from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=12, primary_key=True,default="", verbose_name="用户账号", null=False)
    password = models.CharField(max_length=255, default="", verbose_name="密码", null=False)
    user_name=models.CharField(max_length=255,default="",verbose_name="用户名", null=False)
    user_tel=models.CharField(max_length=255,default="",verbose_name="电话号码", null=True)
    user_mail=models.CharField(max_length=255,default="",verbose_name="邮箱", null=True)
    user_avatar_url=models.CharField(max_length=255,default="",verbose_name="用户头像地址", null=True)
    class Meta:
        db_table = "user"

class DocxVersion(models.Model):  
    DocxName = models.CharField(max_length=255, primary_key=True, verbose_name='用户ID_文档名', null=False)  
    UserId = models.CharField(max_length=255, verbose_name='用户ID', null=False)  
    CreateTime = models.CharField(max_length=255,verbose_name='创建时间', null=False)  
    TableName = models.CharField(max_length=255, verbose_name='存储文件信息的数据表名', null=False)  
    Address = models.CharField(max_length=255, verbose_name='该版本论文所在的目录', null=False)  
    neglect = models.FloatField(verbose_name='忽视率', null=False)  
    Iteration = models.FloatField(verbose_name='小版本增加率', null=False)  
    version = models.FloatField(verbose_name='大版本增加率', null=False)  
    remind = models.IntegerField(verbose_name='论文是否正确率', null=False)
    bigversion = models.IntegerField(verbose_name='大版本号', null=False)  
    smallversion = models.IntegerField(verbose_name='小版本号', null=False)  
    class Meta:  
        db_table = 'docxversion'
    
class Docx(models.Model):  
    DocxName = models.CharField(max_length=255, verbose_name='论文名称', null=False)  
    FileName = models.CharField(max_length=255, primary_key=True, verbose_name='论文版本名称', null=False)  
    UserId = models.CharField(max_length=255, verbose_name='用户ID', null=False)  
    UploadTime = models.CharField(max_length=255, verbose_name='上传时间', null=False) 
    Address = models.CharField(max_length=255, verbose_name='存储地址', null=False)  
    class Meta:  
        db_table = 'docx'  # 明确指定数据库中的表名  