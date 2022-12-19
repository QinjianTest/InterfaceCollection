def create_database():#创建数据库
    try:
        conn, cursor = init_database()
        cursor.execute('create database if NOT EXISTS data_collection_platform default character set utf8 COLLATE utf8_general_ci')
        conn.close()
        return True
    except:
        print('Error:创建数据库失败')
        return None

def create_table():#创建表详细表data,统计表report
    try:
        conn, cursor = init_database()
        cursor.execute('use data_collection_platform')
        cursor.execute('create table if NOT EXISTS data(System varchar(255),CaseName varchar(255), RequestName varchar(255), Result int(5), Time float(5,2), Date datetime,PRIMARY KEY (System,Date,RequestName))') #联合主键
        cursor.execute('create table if NOT EXISTS report(System varchar(255),CaseCount int(6), RequestCount int(6), Seccess int(6) default 0, Fail int(6) default 0,Rate int(5) default 1,Time float(5,2),Date date)')
        cursor.execute('SET SQL_SAFE_UPDATES = 0') #设置可以无条件update，用于计算成功率Rate
        conn.close()
        return True
    except:
        print('Error:创建表失败')
        return None

def init_database(): #连接数据库
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',db='mysql', charset='gbk')
        cursor = conn.cursor()
        return conn,cursor
    except:
        print('Error:数据库连接失败')
        return None

def insert_database(sql,*args):#插入数据
    conn, cursor = init_database()
    cursor.execute('use data_collection_platform')
    try:
        cursor.execute(sql,args)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except:
        print("Error:数据插入失败")
        return None

def update_report(sql): #更新report统计表
    try:
        conn, cursor = init_database()
        cursor.execute('use data_collection_platform')
        cursor.execute('truncate table report')
        cursor.execute(sql)
        cursor.execute('update report set Rate =  Seccess/(Seccess+Fail)*100') #成功或者失败数有可能为NULL，需要重新计算
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except:
        print("Error:更新统计表失败")
        return None

def select_data(sql, *args):#查询数据
    try:
        conn, cursor = init_database()
        cursor.execute('use data_collection_platform')
        cursor.execute(sql, args)
        datas =  cursor.fetchall()
        cursor.close()
        conn.close()
        return datas
    except:
        print("Error:数据查找错误")
        return None
