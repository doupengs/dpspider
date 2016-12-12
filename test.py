#!/usr/bin/env python
#coding:utf-8

from dpspider.spider import Spider

class Mypider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.listUrls = ['http://www.tmtpost.com/new/%d'%page for page in range(1,2)]
        self.mysqlUser = 'root'
        self.mysqlPassword = 'isoftadmin'
        self.mysqlDb = 'mysql'
        self.mysqlTableName = 'doupeng_test'
        # self.isInsertMysql = True
        # self.isUseRedis = True
        # self.proxyEnable = True

    def parseList(self,data,response):
        if data:
            loops = data.xpathAll('//h3/a/@href')
            for item in loops:
                url = 'http://www.tmtpost.com%s'%item.str()
                self.pageUrls.append(url)
                print(url)

    def parsePage(self,data,response):
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
                self.redisMd5Key: self.md5(URL)
            }
            return jsonData

if __name__ == "__main__":
    dps = Mypider()
    dps.run()
