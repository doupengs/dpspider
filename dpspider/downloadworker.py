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
        '''
        self.serverHost = None
        self.serverPort = 5000
        self.serverAuthkey = None
        self.decode = 'utf8'
        self.isDebug = True

    def run(self):
        '''
        :function: run from here
        '''
        QueueManager.register('getParamsInfo')
        QueueManager.register('getTaskQueue')
        QueueManager.register('getResultQueue')
        printText('[INFO]: Try to connect to server %s'%self.serverHost,'cyan',decode=self.decode,isDebug=self.isDebug)
        manager = QueueManager(address=(self.serverHost,self.serverPort),authkey=self.serverAuthkey)
        manager.connect()
        printText('[INFO]: Connect success','green',decode=self.decode,isDebug=self.isDebug)
        params = manager.getParamsInfo()
        task = manager.getTaskQueue()
        result = manager.getResultQueue()
        self.decode = params.get('decode','utf8')
        self.isDebug = params.get('isDebug',True)
        self.useProxyMaxNum = params.get('useProxyMaxNum',5)
        self.proxyFilePath = params.get('proxyFilePath','proxyList.txt')
        self.method = params.get('method','GET')
        self.proxyEnable = params.get('proxyEnable',False)
        self.params = params.get('params',None)
        self.data = params.get('data',None)
        self.json = params.get('json',None)
        self.headers = params.get('headers',None)
        self.cookies = params.get('cookies',None)
        self.files = params.get('files',None)
        self.auth = params.get('auth',None)
        self.timeout = params.get('timeout',None)
        self.allowRedirects = params.get('allowRedirects',True)
        self.verify = params.get('verify',None)
        self.stream = params.get('stream',None)
        self.cert = params.get('cert',None)
        self.downloader = Download(max=self.useProxyMaxNum,proxyFilePath=self.proxyFilePath,isDebug=self.isDebug)
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
