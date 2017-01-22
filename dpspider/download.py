#!/usr/bin/env python
#coding:utf-8

import requests
from .color import printText

class Download(object):
    '''
    :class: use requests.request method,return response or None
    :author: doupeng
    '''
    def __init__(self,max=10,proxyFilePath="proxyList.txt",logFile=None,color=True,debug=4):
        '''
        :param max: default=10 <class int|maximum use of each proxy>
        :param proxyFilePath: default="proxyList.txt" <class str|proxy file path>
        :param logFile: default=None <class str>
        :param color: default=True <class bool>
        :param debug: default=4 <class int|0 NONE,1 [Error],2 [Error][WARING],3 [Error][WARING][INFO],4 ALL>
        :file: the format of each line in the proxyFile must be as follows
            1. http[s],http[s]://ip(\d+\.\d+\.\d+\.\d+):port(\d+)
            2. http[s],http[s]://ip(\d+\.\d+\.\d+\.\d+):port(\d+)
            3. ......
            4. ......
        '''
        self.logFile = logFile
        self.color = color
        self.debug = debug
        self._max = max
        self._index = 0
        self._count = 0
        self._enableProxiesList = []
        try:
            with open(proxyFilePath,"r") as f:
                self._proxiesList = f.readlines()
            proxy = self._proxiesList[self._index].strip().split(",",1)
            self._proxies = {proxy[0]:proxy[1]}
        except Exception as e:
            printText("[Error]download.py Download __init__:%s"%e,logFile=self.logFile,color=self.color,debug=self.debug)

    def download(self,method,url,proxyEnable=False,params=None,data=None,json=None,
                 headers=None,cookies=None,files=None,auth=None,timeout=10,
                 allowRedirects=True,verify=None,stream=None,cert=None):
        '''
        :param method: <class str|'GET','POST','PUT','DELETE','HEAD','OPTIONS'>
        :param url: <class str>
        :param proxyEnable: default=False <class bool|use proxy or not>
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`
        :param json: (optional) json data to send in the body of the :class:`Request`
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`
        :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`
        :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``)
                      for multipart encoding upload.``file-tuple`` can be a 2-tuple ``('filename', fileobj)``,
                      3-tuple ``('filename', fileobj, 'content_type')``or a 4-tuple ``('filename', fileobj,
                      'content_type', custom_headers)``, where ``'content-type'`` is a string defining the
                      content type of the given file and ``custom_headers`` a dict-like object containing
                      additional headers to add for the file
        :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth
        :param timeout: (optional) How long to wait for the server to send data
                        before giving up, as a float, or a :ref:`(connect timeout, read
                        timeout) <timeouts>` tuple <float or tuple>
        :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed <class bool>
        :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy
        :param verify: (optional) whether the SSL cert will be verified. A CA_BUNDLE path can also be provided. Defaults to ``True``
        :param stream: (optional) if ``False``, the response content will be immediately downloaded
        :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair
        :return: <class Response> if failed <None>
        '''
        response = None
        #----not use proxy--------------
        if proxyEnable == False:
            try:
                response = requests.request(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,
                                            files=files,auth=auth,timeout=timeout,allow_redirects=allowRedirects,
                                            verify=verify,stream=stream,cert=cert)
            except Exception as e:
                 printText("[Error]download.py Download download: %s"%e,logFile=self.logFile,color=self.color,debug=self.debug)
            return response
        #----use proxy------------------
        elif proxyEnable:
            try:
                if self._count < self._max:
                    p = 'http' if 'http' in self._proxies else 'https'
                    printText("[INFO]use proxy:%s"%self._proxies.get(p,'').replace(p+'://',''),logFile=self.logFile,color=self.color,debug=self.debug)
                    response = requests.request(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,
                                                files=files,auth=auth,timeout=timeout,allow_redirects=allowRedirects,
                                                proxies=self._proxies,verify=verify,stream=stream,cert=cert)
                    self._count += 1
                else:
                    if self._index < len(self._proxiesList):
                        self._enableProxiesList.append(self._proxies)
                    raise Exception
            except:
                response = self._reTryDownload(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,
                                                files=files,auth=auth,timeout=timeout,allowRedirects=allowRedirects,
                                                verify=verify,stream=stream,cert=cert)
            return response

    def _reTryDownload(self,method,url,params=None,data=None,json=None,headers=None,cookies=None,files=None,
                        auth=None,timeout=10,allowRedirects=True,verify=None,stream=None,cert=None):
        '''
        :function: change proxy
        '''
        self._index += 1
        if self._index < len(self._proxiesList):
            proxy = self._proxiesList[self._index].strip().split(",",1)
            self._proxies = {proxy[0]:proxy[1]}
            self._count = 0
        else:
            self._proxies = self._enableProxiesList[0]
            self._enableProxiesList.append(self._enableProxiesList.pop(0))
            self._count = 0
        try:
            p = 'http' if 'http' in self._proxies else 'https'
            printText("[INFO]change proxy:%s"%self._proxies.get(p,'').replace(p+'://',''),logFile=self.logFile,color=self.color,debug=self.debug)
            response = requests.request(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,
                                        files=files,auth=auth,timeout=timeout,allow_redirects=allowRedirects,
                                        proxies=self._proxies,verify=verify,stream=stream,cert=cert)
            self._count += 1
            return response
        except:
            return self._reTryDownload(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,
                                        files=files,auth=auth,timeout=timeout,allowRedirects=allowRedirects,
                                        verify=verify,stream=stream,cert=cert)

if __name__ == '__main__':
    print(help(Download))
