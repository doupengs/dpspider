#!/usr/bin/env python
#coding:utf-8

from multiprocessing.managers import BaseManager
from dpspider.download import Download
from dpspider.color import printText

class QueueManager(BaseManager):
    pass

class DownloadWorker(object):
    def __init__(self):
        '''
        :members init:
            :self.serverHost = None
            :self.serverPort = 5000
            :self.authkey = None
            :self.decode = 'utf8'
            :self.isDebug = True
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
        '''
        self.serverHost = None
        self.serverPort = 5000
        self.serverAuthkey = None
        self.decode = 'utf8'
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

        self.downloader = Download()

    def run(self):
        self.downloader = Download(max=self.useProxyMaxNum,proxyFilePath=self.proxyFilePath,isDebug=self.isDebug)
        QueueManager.register('getTaskQueue')
        QueueManager.register('getResultQueue')
        printText('[INFO]: Try to connect to server %s'%self.serverHost,'cyan',decode=self.decode,isDebug=self.isDebug)
        manager = QueueManager(address=(self.serverHost,self.serverPort),authkey=self.serverAuthkey)
        manager.connect()
        printText('[INFO]: Connect success','green',decode=self.decode,isDebug=self.isDebug)
        task = manager.getTaskQueue()
        result = manager.getResultQueue()
        while True:
            try:
                printText('[INFO] Now taskQueue num: %d'%task.qsize(),'cyan',decode=self.decode,isDebug=self.isDebug)
                url = task.get()
                printText('[INFO] Get task url: %s'%url,'cyan',decode=self.decode,isDebug=self.isDebug)
                response = self.downloader.download(self.method,url,proxyEnable=self.proxyEnable,params=self.params,data=self.data,json=self.json,
                                          headers=self.headers,cookies=self.cookies,files=self.files,auth=self.auth,timeout=self.timeout,
                                          allowRedirects=self.allowRedirects,verify=self.verify,stream=self.stream,cert=self.cert)
                result.put(response)
                printText('[INFO]: Task run over and put into resultQueue success','green',decode=self.decode,isDebug=self.isDebug)
            except:
                break

if __name__ == '__main__':
    print(help(DownloadWorker))
