#!/usr/bin/env python
#coding:utf-8

import re
from lxml import etree
from dpspider.color import printText

class Parser(object):
    '''
    :class: this is a html parser
    :author: doupeng
    '''
    def __init__(self,data=None,response=None,url=None,isDebug=True):
        '''
        :param data: default=None <class str|unicode response.text>
        :param response: default=None <class Response>
        :param url: default=None <class str>
        :param isDebug: default=True <class bool> or <class str|'print'>
        '''
        try:
            self.isDebug = isDebug
            self.data = data
            self.response = response
            self.url = response.request.url if response and not url else url
            self.__html = etree.HTML(self.data) if data else None
        except Exception as e:
            printText('[Error]parser.py Parser __init__: %s'%e,'red',isDebug=self.isDebug)

    def xpathOne(self,xpath):
        '''
        :param xpath: <class str|xpath expression>
        :function: xpath match one
        :return: <class Parser>
        '''
        try:
            labels = self.__html.xpath(xpath)
        except:
            printText("[Error]parser.py Parser xpathOne: %s %s"%(xpath,self.url),"red",isDebug=self.isDebug)
            return Parser("")
        if len(labels) > 0:
            label = labels[0]
            return Parser(etree.tostring(label,encoding="unicode",method="html")) if isinstance(label,etree._Element) else Parser(label)
        else:
            printText("[WARING]parser.py Parser xpathOne parse None: %s %s"%(xpath,self.url),"yellow",isDebug=self.isDebug)
            return Parser("")

    def xpathAll(self,xpath):
        '''
        :param xpath: <class str|xpath expression>
        :function: xpath match all
        :return: [<class Parser>,<class Parser>...]
        '''
        try:
            labels = self.__html.xpath(xpath)
        except:
            printText("[Error]parser.py Parser xpathAll: %s %s"%(xpath,self.url),"red",isDebug=self.isDebug)
            return []
        if len(labels)>0:
            return [Parser(etree.tostring(label,encoding="unicode",method="html")) if isinstance(label,etree._Element) else Parser(label) for label in labels]
        else:
            printText("[WARING]parser.py Parser xpathAll parse None: %s %s"%(xpath,self.url),"yellow",isDebug=self.isDebug)
            return []

    def reOne(self,pattern):
        '''
        :param pattern: <class str|regular expression>
        :function: regular match one
        :return: <class Parser>
        '''
        try:
            labels = re.findall(pattern,self.data)
        except:
            printText("[Error]parser.py Parser reOne: %s %s"%(pattern,self.url),"red",isDebug=self.isDebug)
            return Parser("")
        if len(labels) > 0:
            return Parser(labels[0])
        else:
            printText("[WARING]parser.py Parser reOne parse None: %s %s"%(pattern,self.url),"yellow",isDebug=self.isDebug)
            return Parser("")

    def reAll(self,pattern):
        '''
        :param pattern: <class str|regular expression>
        :function: regular match all
        :return: [<class Parser>,<class Parser>...]
        '''
        try:
            labels = re.findall(pattern,self.data)
        except:
            printText("[Error]parser.py Parser reAll: %s %s"%(pattern,self.url),"red",isDebug=self.isDebug)
            return []
        if len(labels)>0:
            return [Parser(label) for label in labels]
        else:
            printText("[WARING]parser.py Parser reAll parse None: %s %s"%(pattern,self.url),"yellow",isDebug=self.isDebug)
            return []

    def reSub(self,pattern,goalStr,count=0):
        """
        :param pattern: <class str|regular expression>
        :param count: default=0 <class int|replace number>
        :function: re.sub(pattern,goalStr)
        :return: <class Parser>
        """
        try:
            data = re.compile(pattern).sub(goalStr,self.data,count)
        except Exception as e:
            printText("[Error]parser.py Parser reSub: %s"%e,"red",isDebug=self.isDebug)
            return self
        return Parser(data)

    def str(self):
        '''
        :function: <class Parser> return <class str>
        :return: <class str> if Error <u''>
        '''
        if self.__html is not None:
            return etree.tostring(self.__html,encoding="unicode",method='text')
        else:
            return u''

    def bytes(self,encoding='utf8'):
        '''
        :param encoding: default='utf8' <class str>
        :function: <class Parser> return <class bytes>
        :return: <class bytes> if Error <b''>
        '''
        if self.__html is not None:
            return etree.tostring(self.__html,encoding=encoding,method='text')
        else:
            return u''.encode('utf8')

    def int(self):
        '''
        :function: <class Parser> return <class int>
        :return: <class int> if Error <0>
        '''
        try:
            integer = int(self.data)
        except:
            printText("[Error]parser.py Parser int: self.data must be int","red",isDebug=self.isDebug)
            return 0
        return integer

    def float(self):
        '''
        :function: <class Parser> return <class float>
        :return: <class float> if Error <0.0>
        '''
        try:
            f = float(self.data)
        except:
            printText("[Error]parser.py Parser float:self.data must be float","red",isDebug=self.isDebug)
            return 0.0
        return f

if __name__ == '__main__':
    print(help(Parser))
