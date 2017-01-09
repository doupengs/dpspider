#!/usr/bin/env python
#coding:utf-8

import re
import time
import redis
import hashlib
from Queue import Queue,Empty
from multiprocessing import freeze_support
from multiprocessing.managers import BaseManager
from .color import printText
from .download import Download
from .parser import Parser
from .insertmysql import InsertMysql

taskQueue = Queue()
resultQueue = Queue()
paramsInfo = {}

def returnTaskQueue():
    global taskQueue
    return taskQueue

def returnResultQueue():
    global resultQueue
    return resultQueue

def returnParamsInfo():
    global paramsInfo
    return paramsInfo

class QueueManager(BaseManager):
    pass

class Spider(object):
    '''
    :class: A lightweight Web Crawling and Web Scraping Distributed framework
    :author: doupeng
    '''
    def __init__(self):
        #1==== get ====
        self.listGetUrls = []
        #2==== post ====
        self.listPostUrl = ''
        self.postPages = []
        self.postPageName = None
        #3==== encoding ====
        self.encoding = ('utf8','utf8')
        #4==== printText params ====
        self.logFile = None
        self.color = True
        self.debug = 4
        #5==== Download params =====
        #5.1---- Download.__init__ params ----
        self.useProxyMaxNum = 10
        self.proxyFilePath = 'proxyList.txt'
        #5.2---- Download.download params ----
        self.method = ('GET','GET')
        self.proxyEnable = False
        self.params = None
        self.data = {}
        self.json = None
        self.headers = {}
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        self.cookies = None
        self.files = None
        self.auth = None
        self.timeout = 10
        self.allowRedirects = True
        self.verify = None
        self.stream = None
        self.cert = None
        #6==== InsertMysql params ====
        self.isInsertMysql = False
        #6.1---- InsertMysql.__init__ params ----
        self.mysqlHost = 'localhost'
        self.mysqlUser = ''
        self.mysqlPassword = ''
        self.mysqlDb = ''
        self.mysqlCharset = 'utf8'
        #6.2---- InsertMysql.insertMysql params ----
        self.mysqlTableName = ''
        self.isMysqlFLF = True
        self.isMysqlRLF = False
        #7==== redis params ====
        self.isUseRedis = False
        #7.1---- redis.Redis params ----
        self.redisHost = 'localhost'
        self.redisPort = 6379
        self.redisDb = 0
        self.redisPassword = None
        #7.2---- other params ----
        self.redisKey = ''
        self.isRedisKeyUrl = True
        self._repeatRedis = 0
        #8==== manager params ====
        self.serverHost = None
        self.serverPort = 5000
        self.serverAuthkey = None

    def md5(self,string):
        '''
        :param string: <class str>
        :function: string --> md5 value
        :return: <class str|md5 value>
        '''
        md5 = hashlib.md5()
        md5.update(string)
        return md5.hexdigest()

    def getOneResponseParse(self):
        '''
        :function: get one response from resultQueue and parse
        '''
        while True:
            try:
                response,getTask,getUrl,floor,downloadNum = self._result.get(timeout=3)
                self._resultNum += 1
                if response:
                    if floor == 1:
                        response.encoding = self.encoding[0]
                        data = Parser(response.text,response,logFile=self.logFile,color=self.color,debug=self.debug)
                        result = self.parseList(data,response)
                        printText('[INFO]downloading listUrl: %s'%getUrl,logFile=self.logFile,color=self.color,debug=self.debug)
                        for url in result:
                            if self.isUseRedis and self.isRedisKeyUrl:
                                if not self.RD.get(url) == self.mysqlTableName:
                                    self._task.put((url,2,1))
                                    self._taskNum += 1
                                    printText('[INFO]new pageUrl: %s'%url,logFile=self.logFile,color=self.color,debug=self.debug)
                                else:
                                    self._repeatRedis += 1
                                    printText("[WARING]:pageUrl %s exist in redis"%url,logFile=self.logFile,color=self.color,debug=self.debug)
                            else:
                                self._task.put((url,2,1))
                                self._taskNum += 1
                                printText('[INFO]pageUrl: %s'%url,logFile=self.logFile,color=self.color,debug=self.debug)
                    else:
                        response.encoding = self.encoding[1]
                        data = Parser(response.text,response,logFile=self.logFile,color=self.color,debug=self.debug)
                        result = self.parsePage(data,response)
                        self.insertMysql(result)
                else:
                    if downloadNum == 1:
                        if floor == 1:
                            self._task.put((getTask,1,2))
                            self._taskNum += 1
                        if floor == 2:
                            self._task.put((getTask,2,2))
                            self._taskNum += 1
                        printText('[WARING]:response is %s, Try again later. %s'%(str(response),getUrl),
                                  logFile=self.logFile,color=self.color,debug=self.debug)
                    if downloadNum == 2:
                        printText('[WARING]:request twice,but the response is still %s,Abandon %s'%(str(response),getUrl),
                                  logFile=self.logFile,color=self.color,debug=self.debug)
                if self._task.empty() and self._taskNum == self._resultNum:
                    self._manager.shutdown()
                    printText('[INFO]:all task over,master exit',logFile=self.logFile,color=self.color,debug=self.debug)
                    break
            except Empty:
                printText('[WARING]:download timeout 3s,Please wait a moment...',logFile=self.logFile,color=self.color,debug=self.debug)

    def parseList(self,data,response):
        '''
        :param data: <class Parser>
        :param response: <class Response>
        :function: parse pageUrl here
        :return: <class list|urls>
        '''
        urls = []
        return urls

    def parsePage(self,data,response):
        '''
        :param data: <class Parser>
        :param response: <class Response>
        :function: parse columns here,which you need
        :return: <class dict|jsonData>
        '''
        jsonData = {}
        return jsonData

    def insertMysql(self,jsonData):
        '''
        :param jsonData: <class dict>
        :function: print info and insert mysql
        '''
        keys = jsonData.keys()
        columns = ('(%s)'%(','.join(['%s']*len(jsonData))))%tuple(keys)
        values = tuple([jsonData[key] for key in keys])
        for key in keys:
            printText('[%s]:%s'%(key,jsonData[key]),logFile=self.logFile,color=self.color,debug=self.debug)
        self._printNum += 1
        if self.isInsertMysql:
            if self.isUseRedis:
                redisKey = jsonData[self.redisKey]
                if self.isRedisKeyUrl:
                    if self.IM.insertMysql(self.mysqlTableName,columns,values,self.isMysqlFLF,self.isMysqlRLF):
                        self.RD.set(redisKey,self.mysqlTableName)
                else:
                    if not self.RD.get(redisKey) == self.mysqlTableName:
                        if self.IM.insertMysql(self.mysqlTableName,columns,values,self.isMysqlFLF,self.isMysqlRLF):
                            self.RD.set(redisKey,self.mysqlTableName)
                    else:
                        self._repeatRedis += 1
                        printText("[WARING]:%s %s exist in redis"%(self.redisKey,redisKey),
                                  logFile=self.logFile,color=self.color,debug=self.debug)
            else:
                self.IM.insertMysql(self.mysqlTableName,columns,values,self.isMysqlFLF,self.isMysqlRLF)
        printText(' -%s- NO.%d -%s- '%('*'*15,self._printNum,'*'*15),'black','white','bold',
                  logFile=self.logFile,color=self.color,debug=self.debug)

    def run(self):
        '''
        :function: run from here
        '''
        startTime = time.time()
        #--------------------------------------
        self.headers.update({'User-Agent':self.userAgent})
        #--------------------------------------
        freeze_support()
        QueueManager.register('getTaskQueue',callable=returnTaskQueue)
        QueueManager.register('getResultQueue',callable=returnResultQueue)
        QueueManager.register('getParamsInfo',callable=returnParamsInfo)
        self._manager = QueueManager(address=(self.serverHost,self.serverPort),authkey=self.serverAuthkey)
        self._manager.start()
        self._task = self._manager.getTaskQueue()
        self._result = self._manager.getResultQueue()
        self._params = self._manager.getParamsInfo()
        paramsInfo = {
            'listPostUrl':self.listPostUrl,
            'postPageName':self.postPageName,
            'useProxyMaxNum':self.useProxyMaxNum,
            'proxyFilePath':self.proxyFilePath,
            'method':self.method,
            'proxyEnable':self.proxyEnable,
            'params':self.params,
            'json':self.json,
            'headers':self.headers,
            'cookies':self.cookies,
            'files':self.files,
            'auth':self.auth,
            'timeout':self.timeout,
            'allowRedirects':self.allowRedirects,
            'verify':self.verify,
            'stream':self.stream,
            'cert':self.cert,
        }
        self._params.update(paramsInfo)
        #--------------------------------------
        self.downloader = Download(max=self.useProxyMaxNum,proxyFilePath=self.proxyFilePath,
                                   logFile=self.logFile,color=self.color,debug=self.debug)
        #--------------------------------------
        if self.isInsertMysql:
            self.IM = InsertMysql(host=self.mysqlHost,user=self.mysqlUser,password=self.mysqlPassword,
                                  db=self.mysqlDb,charset=self.mysqlCharset,logFile=self.logFile,
                                  color=self.color,debug=self.debug)
            if self.isUseRedis:
                self.RD = redis.Redis(host=self.redisHost,port=self.redisPort,db=self.redisDb,password=self.redisPassword)
        #--------------------------------------
        self._taskNum = 0
        self._resultNum = 0
        self._printNum = 0
        #('POST','GET')
        if self.listPostUrl and self.postPages and self.postPageName:
            for postPage in self.postPages:
                self.data.update({self.postPageName:postPage})
                self._task.put((self.data,1,1))
                self._taskNum += 1
        #('GET','GET')
        elif self.listGetUrls:
            for url in self.listGetUrls:
                self._task.put((url,1,1))
                self._taskNum += 1
        #--------------------------------------
        self.getOneResponseParse()
        #--------------------------------------
        if self.isInsertMysql:
            printText('[INFO]NUM_SUCCESS: %d'%self.IM.success,logFile=self.logFile,color=self.color,debug=self.debug)
            printText('[INFO]NUM_FAILED : %d'%self.IM.fail,logFile=self.logFile,color=self.color,debug=self.debug)
            if self.isUseRedis:
                printText('[INFO]NUM_REPEAT : %d'%self._repeatRedis,logFile=self.logFile,color=self.color,debug=self.debug)
            else:
                printText('[INFO]NUM_REPEAT : %d'%self.IM.repeat,logFile=self.logFile,color=self.color,debug=self.debug)
            del self.IM
        #--------------------------------------
        endTime = time.time()
        floatTime = re.search('(\.\d{2})',str(endTime-startTime)).group(1)
        intTime = time.strftime('%H:%M:%S',time.gmtime(endTime-startTime))
        printText('[INFO]TOTAL_TIME : %s%s'%(intTime,floatTime),logFile=self.logFile,color=self.color,debug=self.debug)

if __name__ == '__main__':
    print(help(Spider))
