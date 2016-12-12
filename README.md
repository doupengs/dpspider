# dpspider-1.0 目录

* [框架简介](#框架简介)
* [spider.py](#spiderpy)
 * [模块简介](#模块简介)
 * [初始化的成员](#初始化的成员)
 * [重写的方法](#重写的方法)
* [insertmysql.py](#insertmysqlpy)
 * [1](#1)
 * [2](#2)
* [parser.py](#parserpy)
 * [3](#3)
 * [4](#4)
* [download.py](#downloadpy)
 * [5](#5)
 * [6](#6)
* [color.py](#colorpy)
 * [7](#7)
 * [8](#8)
* [反馈与建议](#反馈与建议)

# 框架简介

**dpspider-1.0** ： 一个轻量级Web[爬虫](http://baike.baidu.com/link?url=0HQZpaVPnDxHZnv_cnQBHL5SGLuLOMGa3FstKxUzluN5J39uVRRVya9Ca9Txkh4e9hffRCJG00e6_1k0KY_hzejB3gdtB_v6xqcESvNBTkC)框架

* 1.支持是否使用代理下载
* 2.支持自定义多线程数量
* 3.支持Mysql数据库自动写入过程
* 4.支持redis数据库去重 

# spider.py

#### 模块简介

```markdown
框架的主体，配置文件要继承的类
```
#### 初始化的成员

```markdown
* **self.listUrls** : 最初的要爬取的列表页的所有链接
* **self.pageUrls** : 存储通过列表页解析来的所有详情页的链接
* **self.encoding** : 网页的编码，默认为UTF-8
* **self.threadNum** : 设置开启的线程数量，默认开启10个线程
* **self.isDebug** : 设置是否要打印日志信息，不支持打印彩色的终端可以设置为 print 就是正常的打印，默认为 True 就是彩色打印，False就是关闭所有打印信息，一般程序后台运行时可用
* **self.downloader** 下载器的参数设置:
 * **self.useProxyMaxNum** : 每个代理的连续使用的最大次数，当连续使用次数达到这个数字时，强制更换代理，防止代理被封，默认为5次
 * **self.proxyFilePath** :  代理文件的路径，默认为当前路径下的 proxyList.txt 文件
 * **self.method** : 请求方法，默认为 GET 方法
 * **self.proxyEnable** : 是否使用代理，默认为 False
 * **下面这些是请求时可能用到可选参数，相对常会用到的: data, headers, cookies, timeout**
 * **self.params** = None
 * **self.data** = None
 * **self.json** = None
 * **self.headers** = None
 * **self.cookies** = None
 * **self.files** = None
 * **self.auth** = None
 * **self.timeout** = None
 * **self.allowRedirects** = True
 * **self.verify** = None
 * **self.stream** = None
 * **self.cert** = None
* **self.IM** mysql数据库的参数设置 :
 * **self.mysqlHost** : 数据库的主机名，默认为本机 localhost
 * **self.mysqlUser** : 数据库的用户名
 * **self.mysqlPassword** : 数据库的密码
 * **self.mysqlDb** : 数据库的库名
 * **self.mysqlTableName** : 数据库库下的表名
 * **self.mysqlCharset** : 默认编码为 UTF-8
 * **self.isMysqlRLF** : 违反mysql主键唯一约束条件,没有插入数据库的sql语句，相当于去重，默认不生成repeat.log文件
 * **self.isInsertMysql** : 是否连接数据库，测试抓取正常时启用，默认不连接数据库
* **self.RD** redis书籍库的参数设置:
 * **self.isUseRedis** : 是否使用redis数据库进行去重, 默认为 False
 * **self.redisMd5Key** : 如果使用redis去重，最好在 mysql 中设置一个字段来存储 md5值, 默认为 "MD5KEY", 同时将 md5值 作为redis的一个key存储，value值为mysql的表名
 * **self.redisHost** : 数据库的主机名，默认为本机 localhost
 * **self.redisPort** : 数据库的端口号，默认为6379
 * **self.redisDb** : redis数据库，默认为0
 * **self.redisPassword** : 数据库的密码，默认为 None
 ```
 
#### 重写的方法
 
# insertmysql.py

#### 1

#### 2

# parser.py

#### 3

#### 4

# download.py

#### 5

#### 6

# color.py

#### 7

#### 8

# 反馈与建议

* GITHUP地址：[窦朋 | doupeng](https://github.com/doupengs)
* 微信公众号：[人生苦短遂学python](https://mp.weixin.qq.com/mp/homepage?__biz=MzI5MzI5NTQ4Mg==&hid=1&sn=fde1700cb5532eb84d227b1f6ded6838&uin=Njg4NTExNDQw&key=9ed31d4918c154c8f98e46aaf51029e25d006894bd336605c9ea269077414f400da2fd9110bf7810e535c7ca20c6c5b603eab7f647d52d77496e30ce9f13d357022d8408093b3456b3ce82c9a9069ceb&devicetype=Windows+10&version=62030053&lang=zh_CN&winzoom=1)
* 邮箱：<doupeng1993@sina.com>
