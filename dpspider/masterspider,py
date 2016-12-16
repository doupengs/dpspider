#!/usr/bin/env python
#coding:utf-8

import queue
from multiprocessing.managers import BaseManager
from dpspider.spider import *

taskQueue = queue.Queue()
resultQueue = queue.Queue()

def returnTaskQueue():
    global taskQueue
    return taskQueue

def returnResultQueue():
    global resultQueue
    return resultQueue

class QueueManager(BaseManager):
    pass

class MasterSpider(Spider):
    def __init__(self):
        '''
        :MasterSpider new members init:
            self.serverHost = None
            self.serverPort = 5000
            self.serverAuthkey = None
            self.getResultTimeout = 5
        :dpspider.spider.Spider members init:
            :self.listUrls: default=[] <class list|list urls>
            :self.pageUrls: default=[] <class list|pages urls>
            :self.encoding: default='utf8' <class str|it's response.encoding>
            :self.threadNum: default=10 <class int|open the number of threads>
            :self.decode: default='utf8' <class str>
            :self.isDebug: default=True <class bool> or <class str|'print'>
            :self.downloader params as follows:
                :self.useProxyMaxNum = 5
                :self.proxyFilePath = 'proxyList.txt'
                :self.method = 'GET'
                :self.proxyEnable = False
                :self.params = None
                :self.data = None
                :self.json = None
                :self.headers = None
                :self.cookies = None
                :self.files = None
                :self.auth = None
                :self.timeout = None
                :self.allowRedirects = True
                :self.verify = None
                :self.stream = None
                :self.cert = None
            :self.IM params as follows:
                :self.mysqlHost = 'localhost'
                :self.mysqlUser = ''
                :self.mysqlPassword = ''
                :self.mysqlDb = ''
                :self.mysqlTableName = ''
                :self.mysqlCharset = 'utf8'
                :self.isMysqlRLF = False
                :self.isInsertMysql = False
            :self.RD params as follows:
                :self.isUseRedis = False
                :self.redisMd5Key = 'MD5KEY'
                :self.redisHost = 'localhost'
                :self.redisPort = 6379
                :self.redisDb = 0
                :self.redisPassword = None
        '''
        Spider.__init__(self)
        self.serverHost = None
        self.serverPort = 5000
        self.serverAuthkey = None
        self.getResultTimeout = 3

    def getResult(self):
        '''
        :function: *new function* get result from resultQueue and then insertMysql
        '''
        printText('[INFO]:Try get results...','cyan',decode=self.decode,isDebug=self.isDebug)
        while True:
            try:
                response = self.__result.get(timeout=self.getResultTimeout)
                if response:
                    response.encoding = self.encoding
                    self.insertMysql(Parser(response.text),response)
            except queue.Empty:
                if self.__task.empty():
                    printText('[INFO]: task and result queue are both empty','cyan',decode=self.decode,isDebug=self.isDebug)
                    break
                else:
                    printText('[WARING]: result queue is empty','yellow',decode=self.decode,isDebug=self.isDebug)
        self.__manager.shutdown()
        printText('[INFO]: master exit','cyan',decode=self.decode,isDebug=self.isDebug)

    def appendUrls(self,data,response):
        '''
        :param data: <class Parser>
        :param response: <class Response>
        :function: *reload function* append url parsed from self.listUrls to taskQueue
        '''
        urls = self.parseList(data,response)
        for url in urls:
            printText('[INFO] put task-pageUrl: %s'%url,'cyan',decode=self.decode,isDebug=self.isDebug)
            self.__task.put(url)

    def run(self):
        '''
        :dpspider.spider.Spider members init:
            :self.downloader: <class Download(max=5,proxyFilePath='proxyList.txt')|can use proxy downloader>
            :self.IM:<class InsertMysql>
            :self.RD:<class Redis>
        :function: *reload function* run from here
        '''
        self.downloader = Download(max=self.useProxyMaxNum,proxyFilePath=self.proxyFilePath,isDebug=self.isDebug)
        #--------------------------------------
        if self.isInsertMysql:
            self.IM = InsertMysql(host=self.mysqlHost,user=self.mysqlUser,password=self.mysqlPassword,
                                  db=self.mysqlDb,charset=self.mysqlCharset,isDebug=self.isDebug)
            if self.isUseRedis:
                self.RD = redis.Redis(host=self.redisHost,port=self.redisPort,db=self.redisDb,password=self.redisPassword)
        #--------------------------------------
        QueueManager.register('getTaskQueue', callable=returnTaskQueue)
        QueueManager.register('getResultQueue', callable=returnResultQueue)
        self.__manager = QueueManager(address=(self.serverHost,self.serverPort), authkey=self.serverAuthkey)
        self.__manager.start()
        self.__task = self.__manager.getTaskQueue()
        self.__result = self.__manager.getResultQueue()
        #--------------------------------------
        self.runThreadingParse(len(self.listUrls),self.listUrls,self.appendUrls)
        self.getResult()
        #--------------------------------------
        if self.isInsertMysql:
            printText('[INFO]NUM_SUCCESS: %d'%self.IM.success,'cyan',decode=self.decode,isDebug=self.isDebug)
            printText('[INFO]NUM_FAILED : %d'%self.IM.fail,'cyan',decode=self.decode,isDebug=self.isDebug)
            if self.isUseRedis:
                printText('[INFO]NUM_REPEAT : %d'%self._repeatRedis,'cyan',decode=self.decode,isDebug=self.isDebug)
            else:
                printText('[INFO]NUM_REPEAT : %d'%self.IM.repeat,'cyan',decode=self.decode,isDebug=self.isDebug)

if __name__ == '__main__':
    print(help(MasterSpider))
