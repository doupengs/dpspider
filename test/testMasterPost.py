#!/usr/bin/env python
#coding:utf-8

from dpspider.distspider import Spider

class MyMasterSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.listPostUrl = 'http://www1.sxcredit.gov.cn:8080/WebGovAppSgs/a/sgsxy/xzcfFind'
        self.method = ('POST','GET')
        self.postPages = range(1,11)
        self.postPageName = 'pageNo'
        self.data = {
            'pageSize':10,
        }
        self.serverHost = '127.0.0.1'
        self.serverAuthkey = 'serverAuthkey'

    def parseList(self,data,response):
        urls = []
        if data:
            loops = data.xpathAll('//table[@class="gs_list"]//tr[@style="cursor:pointer"]/@onclick')
            for item in loops:
                id = item.reOne("cfxxDetail\('','(.*?)',").str()
                state = item.reOne(",'(\d)'\)").str()
                url = 'http://www1.sxcredit.gov.cn:8080/WebGovAppSgs/a/sgsxy/cfxxDetail?id=%s&state=%s'%(id,state)
                urls.append(url)
        return urls

    def parsePage(self,data,response):
        jsonData = {}
        if data:
            NAME = data.xpathOne('//table[@class="gs_table"]//tr[1]/td/span').bytes().split('：')[1].strip()
            NUM = data.xpathOne('//table[@class="gs_table"]//tr[2]/td[2]').bytes().strip()
            TITLE = data.xpathOne('//table[@class="gs_table"]//tr[3]/td[2]').bytes().strip()
            URL = response.request.url
            jsonData = {
                '行政相对人名称': NAME,
                '行政处罚决定书文号': NUM,
                '处罚名称': TITLE,
                '链接地址':URL,
            }
        return jsonData

if __name__ == "__main__":
    MyMasterSpider().run()
