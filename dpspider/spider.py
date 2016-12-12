#!/usr/bin/env python
#coding:utf-8

import threading
import hashlib
import redis
from dpspider.color import printText
from dpspider.download import Download
from dpspider.parser import Parser
from dpspider.insertmysql import InsertMysql

class Spider(object):
    '''
    :class: A lightweight Web Crawling and Web Scraping framework
    :author: doupeng
    '''
    def __init__(self):
        '''
        :members init:
            :self.listUrls: default=[] <class list|list urls>
            :self.pageUrls: default=[] <class list|pages urls>
            :self.encoding: default='utf-8' <class str|it's response.encoding>
            :self.threadNum: default=10 <class int|open the number of threads>
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
        self.listUrls = []
        self.pageUrls = []
        self.encoding = 'utf-8'
        self.threadNum = 10
        self.isDebug = True
        #----download params-------------
        self.useProxyMaxNum = 5
        self.proxyFilePath = 'proxyList.txt'
        self.method = 'GET'
        self.proxyEnable = False
        self.params = None
        self.data = None
        self.json = None
        self.headers = None
        self.cookies = None
        self.files = None
        self.auth = None
        self.timeout = None
        self.allowRedirects = True
        self.verify = None
        self.stream = None
        self.cert = None
        #----mysql params------------------
        self.mysqlHost = 'localhost'
        self.mysqlUser = ''
        self.mysqlPassword = ''
        self.mysqlDb = ''
        self.mysqlTableName = ''
        self.mysqlCharset = 'utf8'
        self.isMysqlRLF = False
        self.isInsertMysql = False
        #-----redis params-----------------
        self.isUseRedis = False
        self.redisMd5Key = 'MD5KEY'
        self.redisHost = 'localhost'
        self.redisPort = 6379
        self.redisDb = 0
        self.redisPassword = None
        self.__repeatRedis = 0

    def parseList(self,data,response):
        '''
        :param data: <class Parser>
        :param response: <class Response>
        :function: append url parsed from self.listUrls to self.pageUrls
        '''
        pass

    def parsePage(self,data,response):
        '''
        :param data: <class Parser>
        :param response: <class Response>
        :function: parse columns here,which you need
        :return:<class dict|jsonData>
        '''
        jsonData = {}
        return jsonData

    def getData(self,url):
        '''
        :param url: <class str>
        :function: self.downloader.download() return response,Parser(response.text,response)
        :return:(data<class Parser>,response<class Response>)|if failed None
        '''
        response = self.downloader.download(self.method,url,proxyEnable=self.proxyEnable,params=self.params,data=self.data,json=self.json,
                                          headers=self.headers,cookies=self.cookies,files=self.files,auth=self.auth,timeout=self.timeout,
                                          allowRedirects=self.allowRedirects,verify=self.verify,stream=self.stream,cert=self.cert)
        if response:
            response.encoding = self.encoding
            data = Parser(response.text,response,isDebug=self.isDebug)
            return data,response
        else:
            printText('[WARING]spider.py Spider getData: response|%s %s'%(str(response),url),'yellow',isDebug=self.isDebug)
        return None

    def runThreadingParse(self,urlListLen,urlList,func):
        '''
        :param urlListLen: <class int|the length of a list>
        :param urlList:<class list>
        :param func: function
        :function: open multi thread parse url
        '''
        nStart = 0
        nEnd = self.threadNum
        while nEnd < urlListLen + self.threadNum:
            threads = []
            for url in urlList[nStart:nEnd]:
                DR = self.getData(url)
                if DR:
                    t = threading.Thread(target=func(DR[0],DR[1]))
                    threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            nStart += self.threadNum
            nEnd += self.threadNum

    def md5(self,string):
        '''
        :param string: <class str>
        :function: string --> md5 value
        :return: <class str|md5 value>
        '''
        md5 = hashlib.md5()
        md5.update(string)
        return md5.hexdigest()

    def insertMysql(self,data,response):
        '''
        :param data: <class Parser>
        :param response: <class Response>
        :function: self.parsePage(data,response) return jsonData,then insert mysql
        '''
        jsonData = self.parsePage(data,response)
        keys = jsonData.keys()
        columns = ('(%s)'%(','.join(['%s']*len(jsonData))))%tuple(keys)
        values = tuple([jsonData[key] for key in keys])
        for key in keys:
            printText('%s:\n%s'%(key,jsonData[key]),isDebug=self.isDebug)
        if self.isInsertMysql:
            if self.isUseRedis:
                MD5KEY = jsonData[self.redisMd5Key]
                if not self.RD.get(MD5KEY) == self.mysqlTableName:
                    if self.IM.insertMysql(self.mysqlTableName,columns,values,self.isMysqlRLF):
                        self.RD.set(MD5KEY,self.mysqlTableName)
                else:
                    self.__repeatRedis += 1
                    printText("[WARING]:%s '%s' exist in redis"%(self.redisMd5Key,MD5KEY),'yellow',isDebug=self.isDebug)
            else:
                self.IM.insertMysql(self.mysqlTableName,columns,values,self.isMysqlRLF)
        printText('#'*60,'purple',isDebug=self.isDebug)

    def run(self):
        '''
        :members init:
            :self.downloader: <class Download(max=5,proxyFilePath='proxyList.txt')|can use proxy downloader>
            :self.IM:<class InsertMysql>
            :self.RD:<class Redis>
        :function: run from here
        '''

        self.downloader = Download(max=self.useProxyMaxNum,proxyFilePath=self.proxyFilePath,isDebug=self.isDebug)
        if self.isInsertMysql:
            self.IM = InsertMysql(host=self.mysqlHost,user=self.mysqlUser,password=self.mysqlPassword,
                                  db=self.mysqlDb,charset=self.mysqlCharset,isDebug=self.isDebug)
            if self.isUseRedis:
                self.RD = redis.Redis(host=self.redisHost,port=self.redisPort,db=self.redisDb,password=self.redisPassword)
        self.runThreadingParse(len(self.listUrls),self.listUrls,self.parseList)
        self.runThreadingParse(len(self.pageUrls),self.pageUrls,self.insertMysql)
        if self.isInsertMysql:
            printText('[INFO]NUM_SUCCESS: %d'%self.IM.success,'cyan',isDebug=self.isDebug)
            printText('[INFO]NUM_FAILED : %d'%self.IM.fail,'cyan',isDebug=self.isDebug)
            if self.isUseRedis:
                printText('[INFO]NUM_REPEAT : %d'%self.__repeatRedis,'cyan',isDebug=self.isDebug)
            else:
                printText('[INFO]NUM_REPEAT : %d'%self.IM.repeat,'cyan',isDebug=self.isDebug)

if __name__ == '__main__':
    print(help(Spider))
