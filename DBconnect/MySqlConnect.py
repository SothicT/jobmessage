import pymysql
import os.path
from MyLog import MyLog as mylog
class MysqlConnect(object):
    def __init__(self):
        self.log = mylog()
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            db='jobmessage',
            charset='utf8')
    def InsertToMySqlDB(self,sql,data):
        try:
            with self.connect.cursor as cursor:
                cursor.execute(sql,data)
                cursor.commit()
        finally:
            cursor.close()
            self.connect.close()
        self.log.info(u'数据插入成功！')

    # def QueryToMySqlDB(self, sql):
    #     try:
    #     except:
    #     finally:
    #         pass
    #     self.log.info(u'数据查询成功！')

