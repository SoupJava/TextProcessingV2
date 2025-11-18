import pymysql
def SelectByUser(TableName,userId):
    return f"""
    select * from `{TableName}` where UserId='{userId}'
    """
def SelectByOne(TableName,FileName):
    return f"""
    select * from {TableName} where FileName='{FileName}'
    """
def SelectNewFile(FileName):
    return f"""
    select * from {FileName} where id = (SELECT max(id) FROM {FileName})
    """
def CountTable(FileName):
    return f"""
    select count(*) from {FileName}
    """
def AddDocx(TableName,DocxName,FileName,UserId,UploadTime,Address):
    return f"""
    insert into {TableName} (`DocxName`,`FileName`,`UserId`,`UploadTime`,`Address`) values ('{DocxName}','{FileName}','{UserId}','{UploadTime}','{Address}');
    """
def DelDocx(TableName,FileName):
    return f"""
    delete from {TableName} where FileName='{FileName}'
    """
def UpdateAddress(TableName,Address,FileName):
    return f"""
    update {TableName} set Address={Address} where FileName='{FileName}'
    """



def commit(sql):
    config = {  
    'host': 'localhost',  
    'user': 'root',  
    'password': 'excalibur',  
    'db': 'articalprocessing',  
    'charset': 'utf8mb4',  
    'cursorclass': pymysql.cursors.DictCursor,
    }
    print(sql)
    connection = pymysql.connect(**config)  
    result='init'
    try:  
        with connection.cursor() as cursor:  
            cursor.execute(sql)  
            result = cursor.fetchall()
            connection.commit()
    finally:  
        connection.close()
        return result