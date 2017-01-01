#!usr/bin/env python
#coding:utf-8

try:
    import MySQLdb as MYSQL
except:
    import pymysql as MYSQL
from datetime import datetime
from .color import printText

class InsertMysql(object):
    '''
    :class: link mysql databases and execute sql<"INSERT INTO TABLE (COLUMNS) VALUES (...)">
    :author: doupeng
    '''
    def __init__(self,host,user,password,db,charset='utf8',logFile=None,color=True,debug=4):
        '''
        :param host: <class str|host name>
        :param user: <class str|user name>
        :param password: <class str|password>
        :param db: <class str|database name>
        :param charset: default='utf8' <class str>
        :param logFile: default=None <class str>
        :param color: default=True <class bool>
        :param debug: default=4 <class int|0 NONE,1 [Error],2 [Error][WARING],3 [Error][WARING][INFO],4 ALL>
        '''
        self.logFile = logFile
        self.color = color
        self.debug = debug
        self.success = 0
        self.fail = 0
        self.repeat = 0
        self._conn = MYSQL.connect(host,user,password,db,charset=charset)
        self._cursor = self._conn.cursor()

    def __del__(self):
        self._cursor.close()
        self._conn.close()
        printText('[INFO]:mysql connect close',logFile=self.logFile,color=self.color,debug=self.debug)

    def insertMysql(self,table,columns,values,isMysqlRLF=False):
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
            self._cursor.execute(sql)
            self._conn.commit()
            self.success += 1
            printText('[INFO]:Insert into mysql succeeded',logFile=self.logFile,color=self.color,debug=self.debug)
            return True
        except Exception as e:
            time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            if "for key 'PRIMARY'" not in str(e) and "1062" not in str(e):
                self.fail += 1
                printText('[Error]:Insert into mysql failed',logFile=self.logFile,color=self.color,debug=self.debug)
                with open('insertMysqlFail.log','a') as fail:
                    fail.write('%s %s\n%s\n'%(time,e,sql))
            else:
                self.repeat += 1
                printText('[WARING]:The primary key exist in mysql',logFile=self.logFile,color=self.color,debug=self.debug)
                if isMysqlRLF:
                    with open('insertMysqlRepeat.log','a') as repeat:
                        repeat.write('%s %s\n%s\n'%(time,e,sql))
            return False

if __name__ == '__main__':
    print(help(InsertMysql))