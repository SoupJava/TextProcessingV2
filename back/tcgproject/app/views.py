from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.http import FileResponse ,JsonResponse
import time
import uuid
import os
import shutil 
import pymysql
import random
import hashlib
from xml.etree import ElementTree
from datetime import datetime
from app import docx_mapping
from app.docxutils import SampleWord 
from app.docxutils import docx_test
from app.docxutils import do_docx
from app.docxutils import FileConversion
from app.docxutils import comparsion
from app.docxutils import FileBat
from app.models import User
from app.models import DocxVersion
from apscheduler.schedulers.background import BackgroundScheduler # 使用它可以使你的定时任务在后台运行
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.shortcuts import redirect

wx_login={}
def delete_files(directory):
    file_list = os.listdir(directory)
    for file in file_list:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    @register_job(scheduler, "interval", seconds=86400,replace_existing=True)
    def remove_file_job():
        delete_files("C:/tcg/MySoftWare/textprocess/Project/doc") 
        delete_files("C:/tcg/MySoftWare/textprocess/Project/docx")
        delete_files("C:/tcg/MySoftWare/textprocess/Project/excel")
        delete_files("C:/tcg/MySoftWare/textprocess/Project/jpg")
        delete_files("C:/tcg/MySoftWare/textprocess/Project/pdf")
        delete_files("C:/tcg/MySoftWare/textprocess/Project/ppt")
        delete_files("C:/tcg/MySoftWare/textprocess/Project/TEMP")
        delete_files("C:/tcg/MySoftWare/textprocess/Project/zip")
        print(time.strftime('%Y-%m-%d %H:%M:%S')+" 进行了文件清除")
    # register_events(scheduler)
    @register_job(scheduler, "interval", seconds=15,replace_existing=True)
    def remove_yzid_job():
        now = datetime.now()
        timestamp=now.timestamp()
        for i in list(wx_login.keys()):
            if timestamp-wx_login.get(i)[1]>60:
                del wx_login[i]
                continue
        print(time.strftime('%Y-%m-%d %H:%M:%S')+" 进行了验证码过期清除")
    register_events(scheduler)
    # 启动定时器
    scheduler.start()
except Exception as e:
    print('定时任务异常：%s' % str(e))

config = {  
    'host': 'localhost',  
    'user': 'root',  
    'password': 'excalibur',  
    'db': 'articalprocessing',  
    'charset': 'utf8mb4',  
    'cursorclass': pymysql.cursors.DictCursor  
}  
def hello(request):
    if request.method == 'GET':
        g = request.GET.get('g')
    # return HttpResponse("Hello world !{} ".format(g))
        return redirect('http://www.tcgweb.cn:80')
    else:
        return HttpResponse("The request succeeded, but the interface was deprecated, please visit http://www.tcgweb.cn !")
def replace(request):
    if request.method == 'POST':
            word=SampleWord.replaceWords(request.POST['word'],request.POST['sex'],request.POST['identity'],request.POST['Generation'])
            return HttpResponse(word)
def correctDocx(request):
    if request.method == 'POST':
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\docx\\"+str(uuid.uuid1())+".docx"
            with open(path,'wb+') as f:
                for i in request.FILES.get('file',None).chunks():
                    f.write(i)
            correct_code=docx_test.text_process(path)
            if correct_code==100:
                response = FileResponse(open(path, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Correct.docx'  
                return response
            else:
                return "error"
def correctFile(request):
    if request.method == 'POST':
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\docx\\"+str(uuid.uuid1())+".docx"
            with open(path,'wb+') as f:
                    for i in request.FILES.get('file',None).chunks():
                        f.write(i)
            correct_code=do_docx.do_docx(path)
            if correct_code==100:
                response = FileResponse(open(path, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Result.docx'  
                return response
            else:
                return "error"
def FileToPdf(request):
        file=request.FILES.get('file',None)
        filename=str(file)
        filetype=filename.split('.')[-1]
        if filetype=='docx':
            docxName=str(uuid.uuid1())
            print(docxName)
            print(type(file))
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\docx\\"+docxName+".docx"
            path2="C:\\tcg\\MySoftWare\\textprocess\\Project\\pdf\\"+docxName+".pdf"
            with open(path,'wb+') as f:
                for i in file.chunks():
                    f.write(i)
            # print(123)
            correct_code=FileConversion.docxTopdf(path,path2)
            # print(456)
            if correct_code==100:
                response = FileResponse(open(path2, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Result.pdf'  
                return response
            else:
                return "error"
        if filetype=='ppt':
            pptName=str(uuid.uuid1())
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\ppt\\"+pptName+".ppt"
            path2="C:\\tcg\\MySoftWare\\textprocess\\Project\\pdf\\"+pptName+".pdf"
            with open(path,'wb+') as f:
                for i in request.FILES.get('file',None).chunks():
                    f.write(i)
            correct_code=FileConversion.pptTopdf(path,path2)
            if correct_code==100:
                response = FileResponse(open(path2, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Result.pdf'  
                return response
            else:
                return "error"
        if filetype=='xlsx':
            xlsxName=str(uuid.uuid1())
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\excel\\"+xlsxName+".xlsx"
            path2="C:\\tcg\\MySoftWare\\textprocess\\Project\\pdf\\"+xlsxName+".pdf"
            with open(path,'wb+') as f:
                for i in request.FILES.get('file',None).chunks():
                    f.write(i)
            correct_code=FileConversion.excelTopdf(path,path2)
            if correct_code==100:
                response = FileResponse(open(path2, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Result.pdf'  
                return response
            else:
                return "error"
        if filetype=='jpg':
            jpgName=str(uuid.uuid1())
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\jpg\\"+jpgName+".jpg"
            path2="C:\\tcg\\MySoftWare\\textprocess\\Project\\pdf\\"+jpgName+".pdf"
            with open(path,'wb+') as f:
                for i in request.FILES.get('file',None).chunks():
                    f.write(i)
            correct_code=FileConversion.jpgTopdf(path,path2)
            if correct_code==100:
                response = FileResponse(open(path2, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Result.pdf'  
                return response
            else:
                return "error"
        if filetype=='zip':
            zipName=str(uuid.uuid1())
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\TEMP\\"+zipName+".zip"
            path2="C:\\tcg\\MySoftWare\\textprocess\\Project\\zip\\"+zipName+".zip"
            with open(path,'wb+') as f:
                for i in request.FILES.get('file',None).chunks():
                    f.write(i)
            correct_code=FileConversion.zipTopdf(path,path2)
            if correct_code==100:
                response = FileResponse(open(path2, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Result.zip'  
                return response
            else:
                return "error"
def FileToDocx(request):
        file=request.FILES.get('file',None)
        filename=str(file)
        filetype=filename.split('.')[-1]
        if filetype=='pdf':
            pdfName=str(uuid.uuid1())
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\pdf\\"+pdfName+".pdf"
            path2="C:\\tcg\\MySoftWare\\textprocess\\Project\\docx\\"+pdfName+".docx"
            with open(path,'wb+') as f:
                for i in request.FILES.get('file',None).chunks():
                    f.write(i)
            correct_code=FileConversion.pdfTodocx(path,path2)
            if correct_code==100:
                response = FileResponse(open(path2, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Result.docx'  
                return response
            else:
                return "error"
        if filetype=='doc':
            docName=str(uuid.uuid1())
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\doc\\"+docName+".doc"
            path2="C:\\tcg\\MySoftWare\\textprocess\\Project\\docx\\"+docName+".docx"
            with open(path,'wb+') as f:
                for i in request.FILES.get('file',None).chunks():
                    f.write(i)
            correct_code=FileConversion.docTodocx(path,path2)
            if correct_code==100:
                response = FileResponse(open(path2, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Result.docx'  
                return response
            else:
                return "error"
        if filetype=='zip':
            zipName=str(uuid.uuid1())
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\TEMP\\"+zipName+".zip"
            path2="C:\\tcg\\MySoftWare\\textprocess\\Project\\zip\\"+zipName+".zip"
            with open(path,'wb+') as f:
                for i in request.FILES.get('file',None).chunks():
                    f.write(i)
            correct_code=FileConversion.zipTodocx(path,path2)
            if correct_code==100:
                response = FileResponse(open(path2, 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'Result.zip'  
                return response
            else:
                return "error"
def Filebat(request):
        if request.method =='POST':
            docxName=str(uuid.uuid1())
            xlsxName=str(uuid.uuid1())
            fruitZipName=str(uuid.uuid1())
            path1="C:\\tcg\\MySoftWare\\textprocess\\Project\\docx\\"+docxName+".docx"
            path2="C:\\tcg\\MySoftWare\\textprocess\\Project\\excel\\"+xlsxName+".xlsx"
            path3="C:\\tcg\\MySoftWare\\textprocess\\Project\\TEMP\\"+fruitZipName+"\\"
            fruit="C:\\tcg\\MySoftWare\\textprocess\\Project\\zip\\"+fruitZipName
            print(request.FILES.get('DocxFile'))
            with open(path1,'wb+') as f:
                    for i in request.FILES.get('DocxFile',None).chunks():
                        f.write(i)
            with open(path2,'wb+') as f:
                    for i in request.FILES.get('ExcelFile',None).chunks():
                        f.write(i)
            correct_code=FileBat.do_bat(path1,path2,path3,fruitZipName,request.POST['control'])
            if correct_code==100:
                    response = FileResponse(open(fruit+".zip", 'rb'), as_attachment=True)  
                    response['Content-Disposition'] = 'fruit.zip'  
                    return response
            else:
                    return "error"
def register(request):
    if request.method =='POST':
        print(request.POST)
        try:
            user = User.objects.get(user_id=request.POST['userId'])
            return HttpResponse(-1)
        except Exception as e:
            if request.POST['yzid'] in list(wx_login.keys()):
                user_openid=wx_login[request.POST['yzid']][0]
                user = User.objects.filter(user_avatar_url=user_openid)
                if(len(user)>0):
                    return HttpResponse(-1)
                else:
                    newuser=User(user_id=request.POST['userId'],password=request.POST['password'],user_name=request.POST['username'],user_avatar_url=user_openid)
                    newuser.save()
                    return HttpResponse(0)
            else:
                return HttpResponse(-1)
def login(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            user = User.objects.get(user_id=request.POST['userId'])
            if(request.POST['password']==user.password):
                request.session['user']=user.user_id
                return HttpResponse(0)
            else:
                return HttpResponse(-1)
        except Exception as e:
            return HttpResponse(-1)
def login_id(request):
    if request.method =='POST':
        print(request.POST)
        if request.POST['yzid'] in list(wx_login.keys()):
            user_openid=wx_login[request.POST['yzid']][0]
            user = User.objects.get(user_avatar_url=user_openid)
            request.session['user']=user.user_id
            del wx_login[request.POST['yzid']]
            return HttpResponse(0)
        else:
            return HttpResponse(-1)
def logout(request):
    if request.method == 'POST':
        del request.session['user']
        if request.session.get('DV',None)!=None:
            del request.session['DV']
    return HttpResponse(0)
def test(request):
    if request.method == 'POST':
        print(request.session.get('user', None))
        if request.session.get('user',None)==None:
            return HttpResponse(-1)
        else:
            return HttpResponse(request.session.get('user', None))
def getmessage(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        if userid ==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            user=User.objects.get(user_id=userid)
            data={
                'name':user.user_name,
                'phone':user.user_tel,
                'email':user.user_mail,
                'password':user.password
            }
            return JsonResponse({'code': 0, 'data':data, 'message': '提交成功'})
def updatemessage(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        if userid ==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            try:
                user = User.objects.get(user_id=request.session.get('user',None))
                user.password=request.POST['password']
                user.user_name=request.POST['username']
                user.user_tel=request.POST['userTel']
                user.user_mail=request.POST['userMail']
                user.save()
                return JsonResponse({'code': 1, 'message': '成功'})
            except Exception as e:
                return JsonResponse({'code': 0, 'message': 'userId不存在'})
def SelectAllFile(request):
    if request.method =='POST':
        userid = request.session.get('user',None)
        if userid ==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            docxVersion=DocxVersion.objects.filter(UserId=userid)
            data=list(docxVersion.values())
            return JsonResponse({'code': 1,'data':data ,'message': '成功'})
def SelectFile(request):
    if request.method =='POST':
        userid = request.session.get('user',None)
        if userid ==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            DocxName=userid+"_"+request.POST['ThesisName']
            docxVersion=DocxVersion.objects.filter(DocxName=DocxName)
            data=list(docxVersion.values())
            return JsonResponse({'code': 1,'data':data ,'message': '成功'})
def SetFileSession(request):
    if request.method == 'POST':
        request.session['DV']=request.POST['ThesisName']
        print(request.session.get('DV', None))
        if request.session.get('DV',None)==None:
            return HttpResponse(-1)
        else:
            return HttpResponse(request.session.get('DV', None))
def GetFileSession(request):
    if request.method == 'POST':
        print(request.session.get('DV', None))
        if request.session.get('DV',None)==None:
            return HttpResponse(-1)
        else:
            return HttpResponse(request.session.get('DV', None))
def AddFile(request):
    if request.method == 'POST':
        print(request.session.get('user', None))
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            now = datetime.now()
            daytime = now.strftime('%Y-%M-%D')
            hourtime = now.strftime('%H:%M:%S')
            Createtime = daytime +"-"+hourtime
            TableName = str(uuid.uuid4().hex)
            address = "C:/tcg/MySoftWare/textprocess/Project/user/"
            user_id=request.session.get('user', None)
            address = os.path.join(address, user_id, TableName)
            docx_name = f"{user_id}_{request.POST['ThesisName']}"  
            neglect = 0.98  
            iteration = 0.80  
            version = 0.50  
            remind = 0  
            bigversion = 0  
            smallversion = 0  
            dv = DocxVersion(  
                DocxName=docx_name,  
                UserId=user_id,  
                CreateTime=Createtime,  
                TableName=TableName,  
                Address=address,  
                neglect=neglect,  
                Iteration=iteration,  
                version=version,  
                remind=remind,  
                bigversion=bigversion,  
                smallversion=smallversion  
            )  
            # 保存到数据库  
            dv.save()
            if not os.path.exists(address):  
                os.makedirs(address)  
            connection = pymysql.connect(**config)
            try:  
                with connection.cursor() as cursor:  
                    # 创建一个新表  
                    create_table_query = f"""  
                    CREATE TABLE IF NOT EXISTS {TableName} (
                                `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',
                                `DocxName` varchar(255) NOT NULL COMMENT '论文名称',
                                `FileName` varchar(255) NOT NULL COMMENT '论文版本名称',
                                `UserId` varchar(255) NOT NULL COMMENT '用户ID',
                                `UploadTime` varchar(255) NOT NULL COMMENT '上传时间',
                                `Address` varchar(255) NOT NULL COMMENT '存储地址',
                                PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                    """  
                    cursor.execute(create_table_query)  
                connection.commit() 
            finally:  
                connection.close()
            return JsonResponse({'code': 0, 'message': '创建成功'})
def DelFile(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            DocxName=userid+"_"+request.POST['ThesisName']
            docxVersion=DocxVersion.objects.get(DocxName=DocxName)
            tablename=docxVersion.TableName
            filePath = "C:/tcg/MySoftWare/textprocess/Project/user/"+userid+'/'+docxVersion.TableName
            print(filePath)
            if os.path.exists(filePath):   
                shutil.rmtree(filePath)  
            connection = pymysql.connect(**config)
            try:  
                with connection.cursor() as cursor:   
                    create_table_query = f"""  
                    DROP TABLE IF EXISTS `{tablename}`;
                    """  
                    cursor.execute(create_table_query)   
                connection.commit() 
            finally: 
                connection.close()
            docxVersion.delete()
            return JsonResponse({'code': 0, 'message': '成功'})
def mydocx(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            print(userid+"_"+request.POST['ThesisName'])
            docxversion=DocxVersion.objects.filter(DocxName=userid+"_"+request.POST['ThesisName'])
            result=docx_mapping.commit(docx_mapping.SelectByUser(docxversion[0].TableName,userid))
            return JsonResponse({'code': 0, 'data':result,'message': '成功'})
def docxupload (request):
    if request.method =='POST':
        userid = request.session.get('user',None)
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            result=[]
            DocxName=userid+"_"+request.POST['ThesisName']
            docxVersion=DocxVersion.objects.filter(DocxName=DocxName)
            bigversion=docxVersion[0].bigversion
            smallversion=docxVersion[0].smallversion
            now = datetime.now()
            daytime = now.strftime('%Y-%M-%D')
            hourtime = now.strftime('%H:%M:%S')
            uploadTime = daytime +"-"+hourtime
            newFileName=str(uuid.uuid4().hex)
            filePath="C:/tcg/MySoftWare/textprocess/Project/user/"
            user_id=request.session.get('user', None)
            filePath = filePath+user_id+'/'+docxVersion[0].TableName
            if not os.path.exists(filePath):  
                os.makedirs(filePath)  
            filePath=filePath+"/"+newFileName+".docx"
            print(filePath)
            with open(filePath,'wb+') as f:
                for i in request.FILES.get('file',None).chunks():
                    f.write(i)
            print(docx_mapping.commit(docx_mapping.CountTable(docxVersion[0].TableName))[0]['count(*)'])
            if(docx_mapping.commit(docx_mapping.CountTable(docxVersion[0].TableName))[0]['count(*)']<1):
                bigversion=1
                smallversion=1
            else:
                path2=str(docx_mapping.commit(docx_mapping.SelectNewFile(docxVersion[0].TableName))[0]['Address'])
                similar=comparsion.do_com(filePath,path2)
                result.append(bigversion)
                result.append(smallversion)
                if(similar<=1 and similar>docxVersion[0].neglect):
                    smallversion=smallversion+1
                    result.append("toosmall")
                elif(similar<=docxVersion[0].neglect and similar>docxVersion[0].Iteration):
                    smallversion=smallversion+1
                    result.append("normal")
                elif(similar<=docxVersion[0].Iteration and similar>docxVersion[0].version):
                    bigversion=bigversion+1
                    smallversion=1
                    result.append("normal")
                else:
                    bigversion=bigversion+1;
                    smallversion=1;
                    result.append("toobig")
            filename="第"+str(bigversion)+"."+str(smallversion)+"版"
            result.append(filename)
            filePathTemp="C:/tcg/MySoftWare/textprocess/Project/user/"+user_id+'/'+docxVersion[0].TableName+'/'+filename+'.docx'
            if os.path.isfile(filePath):  
                os.rename(filePath, filePathTemp)  
            docx_mapping.commit(docx_mapping.AddDocx(docxVersion[0].TableName,docxVersion[0].DocxName,filename,user_id,uploadTime,filePathTemp))
            DocxVersion.objects.filter(DocxName=DocxName).update(bigversion=bigversion,smallversion=smallversion)
            return JsonResponse({'code': 0, 'data':result,'message': '成功'})
def UpdateParameter(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            DocxName=userid+"_"+request.POST['ThesisName']
            docxversion=DocxVersion.objects.get(DocxName=DocxName)
            docxversion.remind=0
            docxversion.neglect=request.POST['neglect']
            docxversion.Iteration=request.POST['Iteration']
            docxversion.version=request.POST['version']
            docxversion.save()
            return JsonResponse({'code': 0,'message': '成功'})
def docxdownload(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            DocxName=userid+"_"+request.POST['ThesisName']
            name=request.POST['name']
            docxversion=DocxVersion.objects.get(DocxName=DocxName)
            address=docx_mapping.commit(docx_mapping.SelectByOne(docxversion.TableName,request.POST['name']))[0]["Address"]
            response = FileResponse(open(address, 'rb'), as_attachment=True)  
            response['Content-Disposition'] = f'{name}.docx'  
            return response
def DeleteDocx(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            DocxName=userid+"_"+request.POST['ThesisName']
            docxversion=DocxVersion.objects.get(DocxName=DocxName)
            address=docx_mapping.commit(docx_mapping.SelectByOne(docxversion.TableName,request.POST['name']))[0]["Address"]
            docx_mapping.commit(docx_mapping.DelDocx(docxversion.TableName,request.POST['name']))
            if os.path.exists(address):  
                os.remove(address)  
            return JsonResponse({'code': 0,'message': '成功'})
def Selectdocx(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            DocxName=userid+"_"+request.POST['ThesisName']
            docxversion=DocxVersion.objects.get(DocxName=DocxName)
            result=docx_mapping.commit(docx_mapping.SelectByOne(docxversion.TableName,request.POST['name']))
            # print(result)
            return JsonResponse({'code': 0,'data':result,'message': '成功'})
def ComReports(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            path="C:\\tcg\\MySoftWare\\textprocess\\Project\\docx\\"+str(uuid.uuid1())+".docx"
            with open(path,'wb+') as f:
                    for i in request.FILES.get('file',None).chunks():
                        f.write(i)
            DocxName=userid+"_"+request.POST['ThesisName']
            docxversion=DocxVersion.objects.get(DocxName=DocxName)
            Address=docxversion.Address
            fruitExcelName=str(uuid.uuid1())
            correct_code=FileBat.get_Similarity(path,Address,fruitExcelName)
            if correct_code==100:
                response = FileResponse(open("C:\\tcg\\MySoftWare\\textprocess\\Project\\excel\\"+fruitExcelName+".xlsx", 'rb'), as_attachment=True)  
                response['Content-Disposition'] = 'fruit.xlsx'  
                return response
            else:
                return JsonResponse({'code': -1, 'message': '失败'})
def GetText(request):
    if request.method == 'POST':
        userid = request.session.get('user',None)
        ThesisName = request.session.get('DV',None)
        if request.session.get('user',None)==None:
            return JsonResponse({'code': -1, 'message': 'Session过期'})
        else:
            DocxName=userid+"_"+ThesisName
            docxversion=DocxVersion.objects.get(DocxName=DocxName)
            address=docx_mapping.commit(docx_mapping.SelectByOne(docxversion.TableName,request.POST['versionName']))[0]["Address"]
            # print(address)
            text=comparsion.gettext(address)
            return JsonResponse({'code': 0,'data':text ,'message': '成功'})
        



class ParseXmlMsg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

        if self.MsgType == 'text':
            self.Content = xmlData.find('Content').text.encode('utf-8')
        elif self.MsgType == 'image':
            self.PicUrl = xmlData.find('PicUrl').text
            self.MediaId = xmlData.find('MediaId').text


class TextMsg(object):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
        return XmlForm.format(**self.__dict)

def TencentView(request):
    if request.method == 'GET':# 解析参数
        data = request.GET
        if len(data) == 0:
            return HttpResponse(content="hello, this is WeChat view")
        signature = data.get(key='signature', default='')
        timestamp = data.get(key='timestamp', default='')
        nonce = data.get(key='nonce', default='')
        echostr = data.get(key='echostr', default='')
    # 请按照公众平台官网\基本配置中信息填写
        token = 'JavaSoup123'	
        list_para = [token, timestamp, nonce]
        list_para.sort()
        list_str = ''.join(list_para).encode('utf-8')
	
        sha1 = hashlib.sha1()
        sha1.update(list_str)
        hashcode = sha1.hexdigest()
        print("/GET func: hashcode: {0}, signature: {1}".format(hashcode, signature))	
        if hashcode == signature:
            return HttpResponse(content=echostr)
        else:
            return HttpResponse(content='验证失败')	
    elif request.method == 'POST':
        # 解析发送过来的body
        webData = request.body
        xmlData = ElementTree.fromstring(webData)
        recMsg = ParseXmlMsg(xmlData)
        # print(request.POST['openid'])
        if recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            if(str(recMsg.Content)=="b'123'"):
                yzid = ""
                for i in range(6):
                    ch = chr(random.randrange(ord('0'), ord('9') + 1))
                    yzid += ch
                if yzid not in wx_login.keys():
                    print(yzid)
                    now = datetime.now()
                    timestamp = now.timestamp()
                    msg=list()
                    msg.append(recMsg.FromUserName)
                    msg.append(timestamp)
                    wx_login[yzid]=msg
                    print(wx_login)
                    content="感谢使用 IFP论文小助手 !\n您的验证码为："+f"<a href='weixin://bizmsgmenu?msgmenuid=1&msgmenucontent={yzid}'>"+f"{yzid}"+"</a>"
                # content=recMsg.Content
            else:
                content = "感谢关注 IFP论文小助手 微信公众号!\n这里将不定期推送有关办公和计算机知识!\n如果您要登录，请输入‘123’来获取登录验证码。\n点击登录：<a href='http://www.tcgweb.cn/#/login'>IFP论文小助手</a>"
            # print(recMsg.FromUserName)
            # print(str(recMsg.Content))
            replyMsg = TextMsg(toUser, fromUser, content)
            return HttpResponse(content=replyMsg.send())