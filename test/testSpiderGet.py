#!/usr/bin/env python
#coding:utf-8

from dpspider.spider import Spider

class Mypider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.listGetUrls = ['http://www.tmtpost.com/new/%d'%page for page in range(1,11)]

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
            CTIME = data.xpathOne('//span[contains(@class,"time")]').datetime()
            CONTENT = data.xpathOne('//article/div[@class="inner"]').bytes().strip()
            jsonData = {
                'TITLE': TITLE,
                'URL': URL,
                'CTIME': CTIME,
                'CONTENT': CONTENT,
            }
        return jsonData

if __name__ == "__main__":
    Mypider().run()
