import os
import shutil
import pythoncom
from win32com import client as wc
import zipfile
def docxTopdf(path,path2):
    pythoncom.CoInitialize()
    word = wc.Dispatch("Word.Application")  # 打开word应用程序
    # for file in files:
    doc = word.Documents.Open(path)  # 打开word文件
    doc.SaveAs(path2, 17)  # 另存为后缀为".pdf"的文件，其中参数17表示为pdf    
    doc.Close()  # 关闭原来word文件
    word.Quit()
    return 100
def pptTopdf(path,path2):
    pythoncom.CoInitialize()
    pptt = wc.Dispatch("PowerPoint.Application")
    ppt = pptt.Presentations.Open(path)
    ppt.SaveAs(path2, 32)
    ppt.Close()
    pptt.Quit()
    # from ppt2pdf import convert
    # path2 = path2.Replace('/', '\\');
    # convert(path,path2)
    return 100
def jpgTopdf(path,path2):
    pythoncom.CoInitialize()
    from PIL import Image
    img=Image.open(path)
    img.save(path2,"PDF",resolution=100.0,save_all=True)
    return 100
def excelTopdf(path,path2):
    print(path)
    print(path2)
    pythoncom.CoInitialize()
    excel=wc.Dispatch("Excel.Application")
    xls=excel.Workbooks.Open(path)
    xls.SaveAs(path2,57)
    xls.Close()
    excel.Quit()
    return 100
def pdfTodocx(path,path2):
    pythoncom.CoInitialize()
    from pdf2docx import Converter
    #pdf转word
    a = Converter(path)  #pdf的路径
    a.convert(path2)
    a.close() #一定要有，释放内存用的
    return 100
def docTodocx(path,path2):
    pythoncom.CoInitialize()
    word = wc.Dispatch("Word.Application")
    doc = word.Documents.Open(path)
    doc.SaveAs(path2, 12)  # 12表示docx格式
    doc.Close()
    word.Quit()
    return 100
def zipTopdf(path,path2):
    zipfilename=path
    if zipfile.is_zipfile(zipfilename):
        zfile=support_gbk(zipfile.ZipFile(zipfilename))
        dirpath=path[:-4]
        dirpath2=path2[:-4]
        os.mkdir(dirpath2)
        for file in zfile.namelist():
            zfile.extract(file,dirpath)
        files=os.listdir(dirpath)
        print(files)
        for file in files:
            result=os.path.splitext(file)
            filetype=result[1]
            filename=result[0]
            filepath=dirpath+"/"+file
            print(filepath)
            filepath2=dirpath2+"/"+filename+".pdf"
            print(filetype)
            if filetype=='.docx':
                docxTopdf(filepath,filepath2)
            elif filetype=='.ppt':
                pptTopdf(filepath,filepath2)
            elif filetype=='.xlsx':
                excelTopdf(filepath,filepath2)
            elif filetype=='.jpg':
                jpgTopdf(filepath,filepath2)
        zipDir(dirpath2,path2)#压缩文件夹
        shutil.rmtree(dirpath)
        shutil.rmtree(dirpath2)
        return 100
def zipTodocx(path,path2):
    zipfilename=path
    if zipfile.is_zipfile(zipfilename):
        zfile=support_gbk(zipfile.ZipFile(zipfilename))
        dirpath=path[:-4]
        dirpath2=path2[:-4]
        os.mkdir(dirpath2)
        for file in zfile.namelist():
            zfile.extract(file,dirpath)
        files=os.listdir(dirpath)
        for file in files:
            result=os.path.splitext(file)
            filetype=result[1]
            filename=result[0]
            filepath=dirpath+"/"+file
            filepath2=dirpath2+"/"+filename+".docx"
            if filetype=='.doc':
                docTodocx(filepath,filepath2)
            elif filetype=='.pdf':
                pdfTodocx(filepath,filepath2)
        zipDir(dirpath2,path2)#压缩文件夹
        shutil.rmtree(dirpath)
        shutil.rmtree(dirpath2)
        return 100
def zipDir(dirpath,outFullName):
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        fpath = path.replace(dirpath,'')
        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()
#中文编码补丁
def support_gbk(zip_file: zipfile.ZipFile):
    name_to_info = zip_file.NameToInfo
    # copy map first
    for name, info in name_to_info.copy().items():
        real_name = name.encode('cp437').decode('gbk')
        if real_name != name:
            info.filename = real_name
            del name_to_info[name]
            name_to_info[real_name] = info
    return zip_file

if __name__ =="__main__":
    correct_code=docxTopdf('E://Project//docx//dc7700a2-242b-11ef-a408-cc6b1e8cd122.docx','E://Project//pdf//dc7700a2-242b-11ef-a408-cc6b1e8cd122.pdf')
    # jpgTopdf(r"C:\Users\13977\Desktop\本科生创意组+赵新元+汤城冠+论文修改辅助平台.doc",r"C:\Users\13977\Desktop\本科生创意组+赵新元+汤城冠+论文修改辅助平台.docx")