#!/usr/bin/env python
#coding:utf-8

from dpspider.spider import Spider

class Mypider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.listGetUrls = ['http://www.tmtpost.com/new/%d'%page for page in range(1,3)]
        # self.threadNum = 40
        # self.isInsertMysql = True
        # self.mysqlHost = ''
        # self.mysqlUser = ''
        # self.mysqlPassword = ''
        # self.mysqlDb = ''
        # self.mysqlTableName = ''
        # self.isUseRedis = True
        # self.proxyEnable = True

    def parseList(self,data,response):
        urls = []
        if data:
            loops = data.xpathAll('//h3/a/@href')
            for item in loops:
                url = 'http://www.tmtpost.com%s'%item.str()
                urls.append(url)
        return urls

    def parsePage(self,data,response):
        jsonData = {}
        if data:
            TITLE = data.xpathOne('//h1').bytes().strip()
            URL = response.request.url
            CTIME = data.xpathOne('//span[contains(@class,"time")]').bytes().strip()
            SUMMERY = data.xpathOne('//p[@class="post-abstract"]/text()[2]').bytes().strip()
            jsonData = {
                'TITLE': TITLE,
                'URL': URL,
                'CTIME': CTIME,
                'SUMMERY': SUMMERY,
            }
        return jsonData

if __name__ == "__main__":
    dps = Mypider()
    dps.run()