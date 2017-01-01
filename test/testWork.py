#!/usr/bin/env python
#coding:utf-8

from dpspider.multiworker import multiWorker

if __name__ == '__main__':
    multiWorker(10,serverAuthkey='hello')
    #multiWorker(serverAuthkey='hello',logFile='1.log')
