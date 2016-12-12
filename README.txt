# dpspider
A lightweight Web Crawling and Web Scraping framework
一个轻量级Web爬行抓取框架

Help on class Spider in module __main__:

class Spider(__builtin__.object)
 |  :class: A lightweight Web Crawling and Web Scraping framework
 |          一个轻量级Web爬行抓取框架
 |  :author: doupeng
 |
 |  Methods defined here:
 |
 |  __init__(self)
 |      :members init:
 |          :self.listUrls: default=[] <class list|list urls>
 |                          这里是最初的要爬取得列表页的链接
 |          :self.pageUrls: default=[] <class list|pages urls>
 |                          这里是存储通过列表页解析来的所有详情页的链接
 |          :self.encoding: default='utf-8' <class str|it is response.encoding>
 |                          这里设置网页的编码，默认为UTF-8
 |          :self.threadNum: default=10 <class int|open the number of threads>
 |                           这里是设置开启的线程数量，默认为开启10个线程
 |          :self.isDebug: default=True <class bool> or <class str|'print'>
 |                         这里是设置是否要打印输出一些日志信息，不支持打印彩色的终端可以设置为print就是正常的输出了
 |                         默认为True就是彩色输出，False就是关闭所有输出信息，一般程序后台运行时可用
 |          :self.downloader params as follows:
 |           关于下载器的一些参数设置
 |              :self.useProxyMaxNum = 5
 |               每个代理的连续最大使用次数，当连续使用达到这个数字是，强制更换，防止IP被封，默认为5
 |              :self.proxyFilePath = 'proxyList.txt'
 |               代理文件的路径，默认为当前路径下的proxyList.txt文件
 |              :self.method = 'GET'
 |               请求方法，默认为GET方法
 |              :self.proxyEnable = False
 |               是否使用代理，默认为不适用
 |              ------------------------------------------------------
 |              这些是请求时可能用到的一些参数，一般为可选参数，相对常会用到的:data,headers,cookies,timeout
 |              :self.params = None
 |              :self.data = None
 |              :self.json = None
 |              :self.headers = None
 |              :self.cookies = None
 |              :self.files = None
 |              :self.auth = None
 |              :self.timeout = None
 |              :self.allowRedirects = True
 |              :self.verify = None
 |              :self.stream = None
 |              :self.cert = None
 |              -----------------------------------------------------
 |          :self.IM params as follows:
 |           这里是关于mysql数据库的一些设置参数
 |              :self.mysqlHost = 'localhost'
 |               mysql数据库的IP地址，默认为本机的localhost
 |              :self.mysqlUser = ''
 |               mysql数据库的用户名
 |              :self.mysqlPassword = ''
 |               mysql数据库的密码
 |              :self.mysqlDb = ''
 |               mysql数据库的库名
 |              :self.mysqlTableName = ''
 |               mysql数据库的库下的表名
 |              :self.mysqlCharset = 'utf8'
 |               默认编码为UTF-8
 |              :self.isMysqlRLF = False
 |               这个是违反mysql主键唯一的约束条件时没有插入数据库的sql语句的日志，相当于去重，默认不生成repeat.log文件
 |              :self.isInsertMysql = False
 |               这是在配置网址xpath或者re正则的时候先关闭连接数据库，测试抓取正常是启用，默认不连接数据库
 |          :self.RD params as follows:
 |           这里是关于redis数据库的一些设置参数
 |              :self.isUseRedis = False
 |               是否使用redis数据库进行去重
 |              :self.redisMd5Key = 'MD5KEY'
 |               如果使用redis去重，做好在mysql中设置一个字段来存储md5值,默认为MD5KEY
 |               同时将md5值作为redis的一个key存储，value值为mysql的表名
 |              :self.redisHost = 'localhost'
 |               redis数据库的IP地址，默认为localhost
 |              :self.redisPort = 6379
 |               redis数据库的端口号，默认为6379
 |              :self.redisDb = 0
 |               redis数据库，默认为0
 |              :self.redisPassword = None
 |               redis数据库的密码，默认为空
 |
 |  parseList(self, data, response)
 |      :param data: <class Parser>
 |      :param response: <class Response>
 |       初始的列表页的URL请求返回的response和实例化的Parser类data,data所拥有的方法具体help(Parser),或看test.py
 |      :function: append url parsed from self.listUrls to self.pageUrls
 |                 通过这个函数将解析出来的详情页链接添加到self.pageUrls中
 |
 |  parsePage(self, data, response)
 |      :param data: <class Parser>
 |      :param response: <class Response>
 |       详情页的URL请求返回的response和实例化的Parser类data,data所拥有的方法具体help(Parser),或看test.py
 |      :function: parse columns here,which you need
 |                 将你想要的信息字段在这里解析
 |      :return:<class dict|jsonData>
 |               次方法需要返回一个字典
 |               jsonData = {
 |                   'COLUMN1': COLUMN1,
 |                   'COLUMN2': COLUMN2,
 |                   'COLUMN3': COLUMN3,
 |                    ......
 |                   self.redisMd5Key:self.md5(URL)
 |               }
