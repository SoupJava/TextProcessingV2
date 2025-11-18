"""
URL configuration for tcgproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path("", views.hello, name="hello"),
    path("work/HumbleSubstitution", views.replace, name="谦敬词替换"),
    path("work/correctDocx", views.correctDocx, name="生成纠错报告"),
    path("work/correctFile", views.correctFile, name="文本纠错"),
    path("work/FileToPdf", views.FileToPdf, name="文件转pdf"),
    path("work/FileToDocx", views.FileToDocx, name="文件转docx"),
    path("work/FileBat", views.Filebat, name="模板生成"),
    path("work/GetText",views.GetText,name="获取文本来做比对"),

    path("user/register",views.register,name="注册账号"),
    path("user/login",views.login,name="登录账号"),
    path("user/yzid",views.login_id,name="公众号验证码登录"),
    path("user/logout",views.logout,name="退出登录"),
    path("user/test",views.test,name="测试会话是否还在"),
    path("user/getmessage",views.getmessage,name="获取用户基础信息"),
    path("user/updatemessage",views.updatemessage,name="获取用户基础信息"),

    path("docx/SelectAllFile",views.SelectAllFile,name="查找所有项目"),
    path("docx/SelectFile",views.SelectFile,name="查找指定项目"),
    path("docx/SetFileSession",views.SetFileSession,name="set文件的session"),
    path("docx/GetFileSession",views.GetFileSession,name="get文件的session"),
    path("docx/AddFile",views.AddFile,name="添加项目"),
    path("docx/DelFile",views.DelFile,name="删除项目"),
    path("docx/UpdateParameter",views.UpdateParameter,name="修改项目识别参数"),
    path("docx/mydocx",views.mydocx,name="获取该项目下的所有文件"),
    path("docx/docxupload",views.docxupload,name="上传文件"),
    path("docx/docxdownload",views.docxdownload,name="下载文件"),
    path("docx/DeleteDocx",views.DeleteDocx,name="删除文件"),
    path("docx/Selectdocx",views.Selectdocx,name="查找指定文件"),
    path("docx/ComReports",views.ComReports,name="生成相似度报告"),

    path('wechat/', views.TencentView,name="微信公众号接入"),
]
