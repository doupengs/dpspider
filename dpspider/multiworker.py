#!/usr/bin/env python
#coding:utf-8

from multiprocessing import Process
from multiprocessing import freeze_support
from multiprocessing.managers import BaseManager
from .color import printText
from .download import Download

class QueueManager(BaseManager):
    pass

class DownloadWorker(object):
    def __init__(self,serverHost=None,serverAuthkey=None,serverPort=5000,logFile=None,color=True,debug=4):
        '''
        :param serverHost: default=None <class str>
        :param serverAuthkey: default=None <class str>
        :param serverPort: default=5000 <class int>
        :param logFile: default=None <class str>
        :param color: default=True <class bool>
        :param debug: default=4 <class int|0 NONE,1 [Error],2 [Error][WARING],3 [Error][WARING][INFO],4 ALL>
        '''
        self.logFile = logFile
        self.color = color
        self.debug = debug
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.serverAuthkey = serverAuthkey

    def run(self,pName):
        '''
        :param pName: process name
        :function: run from here
        '''
        try:
            freeze_support()
            QueueManager.register('getParamsInfo')
            QueueManager.register('getTaskQueue')
            QueueManager.register('getResultQueue')
            printText('[INFO]%s:Try to connect to %s'%(pName,self.serverHost),logFile=self.logFile,color=self.color,debug=self.debug)
            manager = QueueManager(address=(self.serverHost,self.serverPort),authkey=self.serverAuthkey)
            manager.connect()
            printText('[INFO]%s:Connect success'%pName,logFile=self.logFile,color=self.color,debug=self.debug)
            paramsInfo = manager.getParamsInfo()
            task = manager.getTaskQueue()
            result = manager.getResultQueue()
            while True:
                if paramsInfo:
                    self.listPostUrl = paramsInfo.get('listPostUrl','')
                    self.postPageName = paramsInfo.get('postPageName',None)
                    self.useProxyMaxNum = paramsInfo.get('useProxyMaxNum',5)
                    self.proxyFilePath = paramsInfo.get('proxyFilePath','proxyList.txt')
                    self.method = paramsInfo.get('method',('GET','GET'))
                    self.proxyEnable = paramsInfo.get('proxyEnable',False)
                    self.params = paramsInfo.get('paramsInfo',None)
                    self.json = paramsInfo.get('json',None)
                    self.headers = paramsInfo.get('headers',None)
                    self.cookies = paramsInfo.get('cookies',None)
                    self.files = paramsInfo.get('files',None)
                    self.auth = paramsInfo.get('auth',None)
                    self.timeout = paramsInfo.get('timeout',10)
                    self.allowRedirects = paramsInfo.get('allowRedirects',True)
                    self.verify = paramsInfo.get('verify',None)
                    self.stream = paramsInfo.get('stream',None)
                    self.cert = paramsInfo.get('cert',None)
                    break
            self.downloader = Download(max=self.useProxyMaxNum,proxyFilePath=self.proxyFilePath,logFile=self.logFile,color=self.color,debug=self.debug)
            while True:
                try:
                    getTask,floor,downloadNum = task.get()
                    if floor == 1:
                        method = self.method[0]
                        if self.listPostUrl and self.postPageName and isinstance(getTask,dict):
                            url = self.listPostUrl
                            data = getTask
                        else:
                            url = getTask
                            data = None
                    elif floor == 2:
                        method = self.method[1]
                        url = getTask
                        data = None
                    getUrl = url if not data else '%s  %s:%s'%(url,self.postPageName,data[self.postPageName])
                    printText('[INFO]%s:getUrl:%s  taskNum:%d'%(pName,getUrl,task.qsize()),logFile=self.logFile,color=self.color,debug=self.debug)
                    response = self.downloader.download(method=method,url=url,proxyEnable=self.proxyEnable,params=self.params,data=data,json=self.json,
                                                            headers=self.headers,cookies=self.cookies,files=self.files,auth=self.auth,timeout=self.timeout,
                                                            allowRedirects=self.allowRedirects,verify=self.verify,stream=self.stream,cert=self.cert)
                    result.put((response,getTask,getUrl,floor,downloadNum))
                    if response:
                        printText('[INFO]%s:download success'%pName,logFile=self.logFile,color=self.color,debug=self.debug)
                    else:
                        printText('[WARING]%s:download failed,response is %s'%(pName,str(response)),logFile=self.logFile,color=self.color,debug=self.debug)
                except:
                    printText('[INFO]%s:all task over,master exit'%pName,logFile=self.logFile,color=self.color,debug=self.debug)
                    break
        except:
            printText('[Error]%s:Connect break'%pName,logFile=self.logFile,color=self.color,debug=self.debug)

def multiWorker(processNum=4,serverHost='127.0.0.1',serverAuthkey='',serverPort=5000,logFile=None,color=True,debug=4):
    '''
    :param processNum: default=4 <class int>
    :param serverHost: default='127.0.0.1' <class str>
    :param serverAuthkey: default='' <class bytes>
    :param serverPort: default=5000 <class int>
    :param logFile: default=None <class str>
    :param color: default=True <class bool>
    :param debug: default=4 <class int|0 NONE,1 [Error],2 [Error][WARING],3 [Error][WARING][INFO],4 ALL>
    :function: multiprocessing download
    '''
    while True:
        pools = []
        for num in range(processNum):
            pools.append(Process(target=DownloadWorker(serverHost,serverAuthkey,serverPort,logFile,color,debug).run,args=('Worker%d'%num,)))
        for p in pools:
            p.start()
        for p in pools:
            p.join()

if __name__ == '__main__':
    print(help(DownloadWorker))
    print(help(multiWorker))