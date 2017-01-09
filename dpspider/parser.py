#!/usr/bin/env python
#coding:utf-8

import re
from lxml import etree
from .color import printText

class Parser(object):
    '''
    :class: this is a html parser
    :author: doupeng
    '''
    def __init__(self,data=None,response=None,url=None,logFile=None,color=True,debug=4):
        '''
        :param data: default=None <class str|unicode response.text>
        :param response: default=None <class Response>
        :param url: default=None <class str>
        :param logFile: default=None <class str>
        :param color: default=True <class bool>
        :param debug: default=4 <class int|0 NONE,1 [Error],2 [Error][WARING],3 [Error][WARING][INFO],4 ALL>
        '''
        self.logFile = logFile
        self.color = color
        self.debug = debug
        self.data = data
        self.response = response
        try:
            self.url = response.request.url if response and not url else url
            self._html = etree.HTML(self.data) if data else None
        except Exception as e:
            printText("[Error]parser.py Parser __init__:%s"%e,logFile=self.logFile,color=self.color,debug=self.debug)

    def xpathOne(self,xpath):
        '''
        :param xpath: <class str|xpath expression>
        :function: xpath match one
        :return: <class Parser>
        '''
        try:
            labels = self._html.xpath(xpath)
        except Exception as e:
            printText("[Error]parser.py Parser xpathOne:%s %s %s"%(e,xpath,self.url),logFile=self.logFile,color=self.color,debug=self.debug)
            return Parser(data='',url=self.url,logFile=self.logFile,color=self.color,debug=self.debug)
        if len(labels) > 0:
            label = labels[0]
            return Parser(data=etree.tostring(label,encoding="unicode",method="html"),url=self.url,logFile=self.logFile,color=self.color,
            debug=self.debug) if isinstance(label,etree._Element) else Parser(data=label,url=self.url,logFile=self.logFile,color=self.color,debug=self.debug)
        else:
            printText("[WARING]parser.py Parser xpathOne parse None:%s %s"%(xpath,self.url),logFile=self.logFile,color=self.color,debug=self.debug)
            return Parser(data='',url=self.url,logFile=self.logFile,color=self.color,debug=self.debug)

    def xpathAll(self,xpath):
        '''
        :param xpath: <class str|xpath expression>
        :function: xpath match all
        :return: [<class Parser>,<class Parser>...]
        '''
        try:
            labels = self._html.xpath(xpath)
        except Exception as e:
            printText("[Error]parser.py Parser xpathAll:%s %s %s"%(e,xpath,self.url),logFile=self.logFile,color=self.color,debug=self.debug)
            return []
        if len(labels)>0:
            return [Parser(data=etree.tostring(label,encoding="unicode",method="html"),url=self.url,logFile=self.logFile,color=self.color,
            debug=self.debug) if isinstance(label,etree._Element) else Parser(data=label,url=self.url,logFile=self.logFile,color=self.color,
            debug=self.debug) for label in labels]
        else:
            printText("[WARING]parser.py Parser xpathAll parse None:%s %s"%(xpath,self.url),logFile=self.logFile,color=self.color,debug=self.debug)
            return []

    def reOne(self,pattern):
        '''
        :param pattern: <class str|regular expression>
        :function: regular match one
        :return: <class Parser>
        '''
        try:
            labels = re.findall(pattern,self.data)
        except Exception as e:
            printText("[Error]parser.py Parser reOne:%s %s %s"%(e,pattern,self.url),logFile=self.logFile,color=self.color,debug=self.debug)
            return Parser(data='',url=self.url,logFile=self.logFile,color=self.color,debug=self.debug)
        if len(labels) > 0:
            return Parser(data=labels[0],url=self.url,logFile=self.logFile,color=self.color,debug=self.debug)
        else:
            printText("[WARING]parser.py Parser reOne parse None:%s %s"%(pattern,self.url),logFile=self.logFile,color=self.color,debug=self.debug)
            return Parser(data='',url=self.url,logFile=self.logFile,color=self.color,debug=self.debug)

    def reAll(self,pattern):
        '''
        :param pattern: <class str|regular expression>
        :function: regular match all
        :return: [<class Parser>,<class Parser>...]
        '''
        try:
            labels = re.findall(pattern,self.data)
        except  Exception as e:
            printText("[Error]parser.py Parser reAll:%s %s %s"%(e,pattern,self.url),logFile=self.logFile,color=self.color,debug=self.debug)
            return []
        if len(labels)>0:
            return [Parser(data=label,url=self.url,logFile=self.logFile,color=self.color,debug=self.debug) for label in labels]
        else:
            printText("[WARING]parser.py Parser reAll parse None:%s %s"%(pattern,self.url),logFile=self.logFile,color=self.color,debug=self.debug)
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
            printText("[Error]parser.py Parser reSub:%s"%e,logFile=self.logFile,color=self.color,debug=self.debug)
            return self
        return Parser(data=data,url=self.url,logFile=self.logFile,color=self.color,debug=self.debug)

    def str(self):
        '''
        :function: <class Parser> return <class str>
        :return: <class str> if Error <u''>
        '''
        if self._html is not None:
            return etree.tostring(self._html,encoding="unicode",method='text')
        else:
            return u''

    def bytes(self,encoding='utf8'):
        '''
        :param encoding: default='utf8' <class str>
        :function: <class Parser> return <class bytes>
        :return: <class bytes> if Error <b''>
        '''
        if self._html is not None:
            return etree.tostring(self._html,encoding=encoding,method='text')
        else:
            return u''.encode('utf8')

    def int(self):
        '''
        :function: <class Parser> return <class int>
        :return: <class int> if Error <0>
        '''
        try:
            integer = int(self.data)
        except Exception as e:
            printText("[Error]parser.py Parser int:%s"%e,logFile=self.logFile,color=self.color,debug=self.debug)
            return 0
        return integer

    def float(self):
        '''
        :function: <class Parser> return <class float>
        :return: <class float> if Error <0.0>
        '''
        try:
            f = float(self.data)
        except Exception as e:
            printText("[Error]parser.py Parser float:%s"%e,logFile=self.logFile,color=self.color,debug=self.debug)
            return 0.0
        return f

if __name__ == '__main__':
    print(help(Parser))
