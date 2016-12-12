#!usr/bin/env python
#coding:utf-8

try:
    import MySQLdb as MYSQL
except:
    import pymysql as MYSQL
from dpspider.color import printText

class InsertMysql(object):
    '''
    :class: link mysql databases and execute sql<"INSERT INTO TABLE (COLUMNS) VALUES (...)">
    :author: doupeng
    '''
    def __init__(self,host,user,password,db,charset='utf8',isDebug=True):
        '''
        :param host: <class str|host name>
        :param user: <class str|user name>
        :param password: <class str|password>
        :param db: <class str|database name>
        :param charset: default='utf8' <class str>
        :param isDebug: default=True <class bool> or <class str|'print'>
        '''
        self.__conn = MYSQL.connect(host,user,password,db,charset=charset)
        self.__cursor = self.__conn.cursor()
        self.isDebug = isDebug
        self.success = 0
        self.fail = 0
        self.repeat = 0

    def insertMysql(self,table,columns,values,isRepeatLog=False):
        '''
        :param table: <class str|mysql table name>
        :param isRepeatLog: <class bool|create repeat.log or not>
        :param columns: <class str|some columns,columns='(column1,column1,...)',if all columns,columns=''>
        :param values: <class tuple|all columns value>
        :file:
            :fail.log: Exception and sql
            :repeat.log: Sql
                         According to [primary key]<mysql> to remove repeated data
        '''
        strValues = ""
        for i in values:
            if isinstance(i,str):
                strValues += "'%s',"%i.replace("'","\\'")
            else:
                strValues += "%s,"%i
        sql = ("INSERT INTO %s %s VALUES (%s)"%(table,columns,strValues[:-1])).replace('None','NULL')
        try:
            self.__cursor.execute(sql)
            self.__conn.commit()
            self.success += 1
            printText('[INFO]: A data insert into mysql succeeded','cyan',isDebug=self.isDebug)
            return True
        except Exception as e:
            if "for key 'PRIMARY'" not in str(e) and "1062" not in str(e):
                self.fail += 1
                printText('[Error]: A data insert into mysql failed','red',isDebug=self.isDebug)
                with open('fail.log','a') as fail:
                    fail.write('%s\n\n%s\n\n'%(str(e),sql))
            else:
                self.repeat += 1
                printText('[WARING]: The primary key exist in mysql','yellow',isDebug=self.isDebug)
                if isRepeatLog:
                    with open('repeat.log','a') as repeat:
                        repeat.write('%s\n\n'%sql)
            return False

if __name__ == '__main__':
    print(help(InsertMysql))
