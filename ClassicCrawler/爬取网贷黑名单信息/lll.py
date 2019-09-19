import xlsxwriter
import pymssql
from pymssql import *
# #连接数据库
server = "local"    #连接服务器地址
user = "sa"# 连接帐号
password = "."# 连接密码
conn = pymssql.connect(server,user,password,"JpErp")  #获取连接
cursor = conn.cursor()  #获取光标

#创建表格
xls2 = xlsxwriter.Workbook('../test1.xls')
sht1 = xls2.add_worksheet()
#添加字段
sht1.write(0,0,'农场')
sht1.write(0,1,'鸡舍')
sht1.write(0,2,'养殖状态')
sht1.write(0,3,'摄像头')
sht1.write(0,4,'是否在线')
sht1.write(0,5,'每日掉线时长')
sht1.write(0,6,'总掉线时长')
sht1.write(0,7,'喂食事件是否触发')
sht1.write(0,8,'喂食事件生成数据')
sht1.write(0,9,'每日喂食填报')
#给字段中加值   考虑使用循环
sht1.write(1,0,'古田钱祥云')
sht1.write(1,1,'一号舍')
sht1.write(1,2,'养殖中')
sht1.write(1,3,'舍内')
sht1.write(1,4,'是')
sht1.write(1,5,'50')
sht1.write(1,6,'50分钟')
sht1.write(1,7,'是')
sht1.write(1,8,'是')
sht1.write(1,9,'是')
sht1.write(2,3,'舍外')
sht1.write(2,4,'否')
sht1.write(2,5,'10+50')
sht1.write(2,6,'2小时20分钟')
sht1.write(2,7,'是')
sht1.write(2,8,'否')
xls2.close()


"""
C:\Python37\python.exe C:/Users/Administrator/Desktop/Test/CreateExl.py
C:/Users/Administrator/Desktop/Test/CreateExl.py:2: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated, and in 3.8 it will stop working
  import pymssql
Traceback (most recent call last):
  File "src\pymssql.pyx", line 636, in pymssql.connect
  File "src\_mssql.pyx", line 1957, in _mssql.connect
  File "src\_mssql.pyx", line 677, in _mssql.MSSQLConnection.__init__
_mssql.MSSQLDriverException: Connection to the database failed for an unknown reason.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:/Users/Administrator/Desktop/Test/CreateExl.py", line 7, in <module>
    conn = pymssql.connect(server,user,password,"JpErp")  #获取连接
  File "src\pymssql.pyx", line 645, in pymssql.connect
pymssql.InterfaceError: Connection to the database failed for an unknown reason.

Process finished with exit code 1
"""