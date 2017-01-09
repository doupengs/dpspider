#!/usr/bin/env python
#coding:utf-8

import re
import time
import redis
import hashlib
import threading
from Queue import Queue
from copy import copy
from .color import printText
from .download import Download
from .parser import Parser
from .insertmysql import InsertMysql

class Spider(object):
    '''
    :class: A lightweight Web Crawling and Web Scraping framework
    :author: doupeng
    '''
    def __init__(self):
        #1==== get ====
        self.listGetUrls = []
        self.pageGetUrls = []
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
        self.threadNum = 20
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

    def md5(self,string):
        '''
        :param string: <class str>
        :function: string --> md5 value
        :return: <class str|md5 value>
        '''
        md5 = hashlib.md5()
        md5.update(string)
        return md5.hexdigest()

    def runThreadingDownload(self,urlList,func,queue,method):
        '''
        :param urlList: <class list>
        :param func: function
        :param queue: <class Queue>
        :param method: request method
        :function: run multi thread download
        '''
        nStart = 0
        nEnd = self.threadNum
        urlListLen = len(urlList)
        if urlListLen > 0:
            while nEnd < urlListLen + self.threadNum:
                threads = []
                for item in urlList[nStart:nEnd]:
                    if method == 'POST' and self.postPageName:
                        self.data[self.postPageName] = item
                        t = threading.Thread(target=func,args=(method,self.listPostUrl,queue,copy(self.data)))
                    else:
                        t = threading.Thread(target=func,args=(method,item,queue))
                    threads.append(t)
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                nStart += self.threadNum
                nEnd += self.threadNum

    def downloadResponse(self,method,url,queue,postData=None):
        '''
        :param method: request method
        :param url: <class str>
        :param queue: <class Queue>
        :param postData: <class dir>
        :function: download response, then put response into queue
        '''
        response = self.downloader.download(method,url,proxyEnable=self.proxyEnable,params=self.params,data=postData,json=self.json,
                                          headers=self.headers,cookies=self.cookies,files=self.files,auth=self.auth,timeout=self.timeout,
                                          allowRedirects=self.allowRedirects,verify=self.verify,stream=self.stream,cert=self.cert)
        if response:
            if postData and self.postPageName:
                queue.put((response,postData.get(self.postPageName,'')))
            else:
                queue.put(response)
        else:
            printText('[WARING]spider.py Spider downloadResponse: response|%s %s'%(str(response),url),logFile=self.logFile,color=self.color,debug=self.debug)

    def getOneResponseParse(self,queue,func,isListResponse):
        '''
        :param queue: <class Queue>
        :param func: A function
        :param isListResponse: <class bool>
        :function: get a response from queue,and use func parse this response
        '''
        while True:
            if queue.empty() and self.runThreadingDownloadEnd:
                break
            try:
                if isListResponse and self.postPageName:
                    response,postPage = queue.get(timeout=0.1)
                    response.encoding = self.encoding[0]
                else:
                    response,postPage = queue.get(timeout=0.1),None
                    response.encoding = self.encoding[1]
                data = Parser(response.text,response,logFile=self.logFile,color=self.color,debug=self.debug)
                result = func(data,response)
                if isinstance(result,list):
                    if postPage:
                        printText('[INFO]downloading listUrl: %s  %s'%(response.request.url,'%s:%s'%(self.postPageName,postPage)),
                                  logFile=self.logFile,color=self.color,debug=self.debug)
                    else:
                        printText('[INFO]downloading listUrl: %s'%response.request.url,logFile=self.logFile,color=self.color,debug=self.debug)
                    for url in result:
                        if self.isUseRedis and self.isRedisKeyUrl:
                            if not self.RD.get(url) == self.mysqlTableName:
                                self.pageGetUrls.append(url)
                                printText('[INFO]new pageUrl:%s'%url,logFile=self.logFile,color=self.color,debug=self.debug)
                            else:
                                self._repeatRedis += 1
                                printText("[WARING]:pageUrl %s exist in redis"%url,logFile=self.logFile,color=self.color,debug=self.debug)
                        else:
                            self.pageGetUrls.append(url)
                            printText('[INFO]pageUrl: %s'%url,logFile=self.logFile,color=self.color,debug=self.debug)
                if isinstance(result,dict):
                    self.insertMysql(result)
            except Exception as e:
                if str(e):
                    printText('[Error]:spider.py Spider getOneResponseParse: %s'%e,logFile=self.logFile,color=self.color,debug=self.debug)

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
                    if self.IM.insertMysql(self.mysqlTableName,columns,values,self.isMysqlRLF):
                        self.RD.set(redisKey,self.mysqlTableName)
                else:
                    if not self.RD.get(redisKey) == self.mysqlTableName:
                        if self.IM.insertMysql(self.mysqlTableName,columns,values,self.isMysqlRLF):
                            self.RD.set(redisKey,self.mysqlTableName)
                    else:
                        self._repeatRedis += 1
                        printText("[WARING]:%s %s exist in redis"%(self.redisKey,redisKey),
                                  logFile=self.logFile,color=self.color,debug=self.debug)
            else:
                self.IM.insertMysql(self.mysqlTableName,columns,values,self.isMysqlRLF)
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
        self.queueLR = Queue()
        self.queuePR = Queue()
        self._printNum = 0
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
        self.runThreadingDownloadEnd = False
        t = threading.Thread(target=self.getOneResponseParse,args=(self.queueLR,self.parseList,True))
        t.start()
        if self.method[0] == 'POST':
            self.runThreadingDownload(self.postPages,self.downloadResponse,self.queueLR,self.method[0])
        elif self.method[0] == 'GET':
            self.runThreadingDownload(self.listGetUrls,self.downloadResponse,self.queueLR,self.method[0])
        self.runThreadingDownloadEnd = True
        t.join()
        #--------------------------------------
        self.runThreadingDownloadEnd = False
        t = threading.Thread(target=self.getOneResponseParse,args=(self.queuePR,self.parsePage,False))
        t.start()
        self.runThreadingDownload(self.pageGetUrls,self.downloadResponse,self.queuePR,self.method[1])
        self.runThreadingDownloadEnd = True
        t.join()
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
