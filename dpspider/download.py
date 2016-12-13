#!/usr/bin/env python
#coding:utf-8

import requests
from dpspider.color import printText

class Download(object):
    '''
    :class: use requests.request method,return response or None
    :author: doupeng
    '''
    def __init__(self,max=5,proxyFilePath="proxyList.txt",decode='utf8',isDebug=True):
        '''
        :param max: default=5 <class int|maximum use of each proxy>
        :param proxyFilePath: default="proxyList.txt" <class str|proxy file path>
        :param decode: default='utf-8' <class str>
        :param isDebug: default=True <class bool> or <class str|'print'>
        :file: the format of each line in the proxyFile must be as follows
            1. http[s],http[s]://ip(\d+\.\d+\.\d+\.\d+):port(\d+)
            2. http[s],http[s]://ip(\d+\.\d+\.\d+\.\d+):port(\d+)
            3. ......
            4. ......
        '''
        try:
            self.decode = decode
            self.isDebug = isDebug
            self.__max = max
            self.__index = 0
            self.__count = 0
            self.__enableProxiesList = []
            with open(proxyFilePath,"r") as f:
                self.__proxiesList = f.readlines()
            proxy = self.__proxiesList[self.__index].strip().split(",",1)
            self.__proxies = {proxy[0]:proxy[1]}
        except Exception as e:
            printText('[Error]download.py Download __init__: %s'%e,'red',decode=self.decode,isDebug=self.isDebug)

    def download(self,method,url,proxyEnable=False,params=None,data=None,json=None,
                 headers=None,cookies=None,files=None,auth=None,timeout=None,
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
                 printText("[Error]download.py Download download: %s"%e,"red",decode=self.decode,isDebug=self.isDebug)
            return response
        #----use proxy------------------
        elif proxyEnable:
            try:
                if self.__count < self.__max:
                    p = 'http' if 'http' in self.__proxies else 'https'
                    printText("[INFO]use proxy: %s"%self.__proxies.get(p,'').replace(p+'://',''),"green",decode=self.decode,isDebug=self.isDebug)
                    response = requests.request(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,
                                                files=files,auth=auth,timeout=timeout,allow_redirects=allowRedirects,
                                                proxies=self.__proxies,verify=verify,stream=stream,cert=cert)
                    self.__count += 1
                else:
                    if self.__index < len(self.__proxiesList):
                        self.__enableProxiesList.append(self.__proxies)
                    raise Exception
            except:
                response = self.__reTryDownload(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,
                                                files=files,auth=auth,timeout=timeout,allowRedirects=allowRedirects,
                                                verify=verify,stream=stream,cert=cert)
            return response

    def __reTryDownload(self,method,url,params=None,data=None,json=None,headers=None,cookies=None,files=None,
                        auth=None,timeout=None,allowRedirects=True,verify=None,stream=None,cert=None):
        '''
        :function: change proxy
        '''
        self.__index += 1
        if self.__index < len(self.__proxiesList):
            proxy = self.__proxiesList[self.__index].strip().split(",",1)
            self.__proxies = {proxy[0]:proxy[1]}
            self.__count = 0
        else:
            self.__proxies = self.__enableProxiesList[0]
            self.__enableProxiesList.append(self.__enableProxiesList.pop(0))
            self.__count = 0
        try:
            p = 'http' if 'http' in self.__proxies else 'https'
            printText("[INFO]change proxy: %s"%self.__proxies.get(p,'').replace(p+'://',''),"cyan",decode=self.decode,isDebug=self.isDebug)
            response = requests.request(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,
                                        files=files,auth=auth,timeout=timeout,allow_redirects=allowRedirects,
                                        proxies=self.__proxies,verify=verify,stream=stream,cert=cert)
            self.__count += 1
            return response
        except:
            return self.__reTryDownload(method,url,params=params,data=data,json=json,headers=headers,cookies=cookies,
                                        files=files,auth=auth,timeout=timeout,allowRedirects=allowRedirects,
                                        verify=verify,stream=stream,cert=cert)

if __name__ == '__main__':
    print(help(Download))
