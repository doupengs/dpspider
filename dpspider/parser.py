#!/usr/bin/env python
#coding:utf-8

import re
import datetime
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
    
    def datetime(self,timeStrFormat="%Y-%m-%d %H:%M:%S",returnStrType=True):
        '''
        :param timeStrFormat: <class str|time format>
        :param returnStrType: <class bool>
        :return: True -> return string time
                 False -> return datetime.datetime
                 current time if search failed
        '''
        S = re.search(u"(\d+)\s*秒前",self.data)
        M = re.search(u"(\d+)\s*分钟前",self.data)
        H = re.search(u"(\d+)\s*小时前",self.data)
        D = re.search(u"(\d+)\s*天前",self.data)
        W = re.search(u"(\d+)\s*周前",self.data)
        JT = re.search(u'今天\s*(\d+:\d+:?\d*)',self.data)
        ZT = re.search(u'昨天\s*(\d+:\d+:?\d*)',self.data)
        QT = re.search(u'前天\s*(\d+:\d+:?\d*)',self.data)
        SZ = re.search(u'((\d+)[-/年](\d+)[-/月](\d+)日?\s*(\d*):?(\d*):?(\d*))',self.data)
        if S or M or H or D or W:
            seconds = int(S.group(1)) if S else 0
            minutes = int(M.group(1)) if M else 0
            hours   = int(H.group(1)) if H else 0
            days    = int(D.group(1)) if D else 0
            weeks   = int(W.group(1)) if W else 0
            dtf = datetime.datetime.now() - datetime.timedelta(days,seconds,0,0,minutes,hours,weeks)
            strDt = dtf.strftime(timeStrFormat)
            dt = datetime.datetime.strptime(strDt,timeStrFormat)
        elif JT or ZT or QT:
            strTime = JT.group(1) if JT else ZT.group(1) if ZT else QT.group(1)
            startDay = 1 if JT else 2 if ZT else 3
            days = datetime.date.today() - datetime.date(1900,1,startDay)
            try:
                dt = datetime.datetime.strptime(strTime,"%H:%M:%S") + days
            except:
                dt = datetime.datetime.strptime(strTime,"%H:%M") + days
            strDt = dt.strftime(timeStrFormat)
        elif SZ:
            year = SZ.group(2)
            mouth = SZ.group(3)
            day = SZ.group(4)
            hour = SZ.group(5) if SZ.group(5) else u'00'
            minute = SZ.group(6) if SZ.group(6) else u'00'
            second = SZ.group(7) if SZ.group(7) else u'00'
            if len(year) == 4:
                dt = datetime.datetime.strptime('%s%s%s%s%s%s'%(year,mouth,day,hour,minute,second),'%Y%m%d%H%M%S')
            elif len(year)  == 2:
                dt = datetime.datetime.strptime('%s%s%s%s%s%s'%(year,mouth,day,hour,minute,second),'%y%m%d%H%M%S')
            strDt = dt.strftime(timeStrFormat)
        else:
            dtf = datetime.datetime.now()
            strDt = dtf.strftime(timeStrFormat)
            dt = datetime.datetime.strptime(strDt,timeStrFormat)
            printText('[Error]parser.py Parser datetime:search time format failed, return current time',
                      logFile=self.logFile,color=self.color,debug=self.debug)
        if returnStrType:
            return strDt
        else:
            return dt

if __name__ == '__main__':
    print(help(Parser))
