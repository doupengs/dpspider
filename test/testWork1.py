#!/usr/bin/env python
#coding:utf-8

from dpspider.downloadworker import DownloadWorker

class MyWorkSpider(DownloadWorker):
    def __init__(self):
        DownloadWorker.__init__(self)
        self.serverHost = '127.0.0.1'
        self.serverAuthkey = b'test'

if __name__ == '__main__':
    while True:
        try:
            dp = MyWorkSpider()
            dp.run()
        except:
            pass
