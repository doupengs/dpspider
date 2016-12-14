# dpspider 目录

* [框架简介](#框架简介)
* [下载安装](#下载安装)
 * [依赖库](#依赖库)
 * [安装方法](#安装方法)
* [spider.py](#spiderpy)
 * [spider简介](#spider简介)
 * [初始化的成员](#初始化的成员)
 * [需要重载的方法](#需要重载的方法)
 * [运行效果图展示](#运行效果图展示)
* [insertmysql.py](#insertmysqlpy)
 * [insertmysql简介](#insertmysql简介)
* [parser.py](#parserpy)
 * [parser简介](#parser简介)
* [download.py](#downloadpy)
 * [download简介](#download简介)
* [color.py](#colorpy)
 * [color简介](#color简介)
* [反馈与建议](#反馈与建议)

# 框架简介

**dpspider-1.0** ： 一个轻量级Web[爬虫](http://baike.baidu.com/link?url=0HQZpaVPnDxHZnv_cnQBHL5SGLuLOMGa3FstKxUzluN5J39uVRRVya9Ca9Txkh4e9hffRCJG00e6_1k0KY_hzejB3gdtB_v6xqcESvNBTkC)框架

* 1.支持是否使用代理下载
* 2.支持自定义多线程数量
* 3.支持Mysql数据库自动写入过程
* 4.支持redis数据库去重

# 下载安装

#### 依赖库

* **requests >= 2.11** `pip install requests` **安装即可**
* **lxml >= 3.6** `pip install lxml` **安装**
 * 如果`lxml`安装失败，`windows`系统点击[这里](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)下载合适的版本
* **MySQL-python >= 1.2.3** `pip install MySQL-python` **安装**
 * 如果`MySQL-python`安装失败，`windows`系统点击[这里](http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python)下载合适的版本
* **redis>= 2.10** `pip install redis` **安装即可**

#### 安装方法

```markdown
1.python setup.py install
2.pip install dpspider-x.x.x.tar.gz ( win | linux | macOS )
3.dpspider-x.x.x.win-amd64.exe ( windows可执行文件，双击安装) 
```

* `xxx.tar.gz` 历史所有版本
 * [dpspider-1.0.0.tar.gz](http://pan.baidu.com/s/1eSr7Jyy)
* `xxx.exe` 历史所有版本
 * [dpspider-1.0.0.win-amd64.exe](http://pan.baidu.com/s/1kUSvjOr)

# spider.py

#### spider简介

```markdown
框架的主体，配置文件要继承的类
```
#### 初始化的成员

* **self.listUrls** : 最初的要爬取的列表页的所有链接
* **self.pageUrls** : 存储通过列表页解析来的所有详情页的链接
* **self.encoding** : 网页的编码，默认为UTF-8
* **self.threadNum** : 开启的线程数量，默认开启10个线程
* **self.decode** : 将打印语句解码成unicode，默认为 UTF-8,例如数据需要UTF-8，而输出终端需要gbk，将输出语句解码，解决打印乱码问题
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
* **self.RD** redis数据库的参数设置:
 * **self.isUseRedis** : 是否使用redis数据库进行去重, 默认为 False
 * **self.redisMd5Key** : 如果使用redis去重，最好在 mysql 中设置一个字段来存储 md5值, 默认为 "MD5KEY", 同时将 md5值 作为redis的一个key存储，value值为mysql的表名
 * **self.redisHost** : 数据库的主机名，默认为本机 localhost
 * **self.redisPort** : 数据库的端口号，默认为6379
 * **self.redisDb** : redis数据库，默认为0
 * **self.redisPassword** : 数据库的密码，默认为 None

#### 需要重载的方法

* **parseList(**self,data,response**)**
```markdown
通过data(是一个Parser类，可以看parser.py来了解这个类下的方法)，response，解析的所有详情页的url添加到self.pageUrls中.
self.pageUrls.append(url)
```

* **parsePage(**self,data,response**)**
```markdown
通过data(是一个Parser类，可以看parser.py来了解这个类下的方法)，response，解析的所有你想要的字段,并返回一个字典
{
colunm1:value1,
colunm2:value2,
...
}
```

#### 运行效果图展示

* 点击查看 [test.py](https://github.com/doupengs/dpspider/blob/master/test.py) `实例源码`

![](https://github.com/doupengs/dpspider/blob/master/image/1.jpg)<br>
```markdown
1.彩色打印，调试阶段，不进行数据入库和去重
```

![](https://github.com/doupengs/dpspider/blob/master/image/2.png)<br>
```markdown
2.redis数据库中存在这个 key 的[WARING]
```

![](https://github.com/doupengs/dpspider/blob/master/image/3.png)<br>
```markdown
3.mysql数据库违反主键唯一约束条件的[WARING]
```

![](https://github.com/doupengs/dpspider/blob/master/image/4.png)<br>
```markdown
4.mysql数据库插入成功的[INFO]
```

![](https://github.com/doupengs/dpspider/blob/master/image/5.png)<br>
```markdown
5.Parser类中 xpath 的[Error]和解析为空的[WARING]
```

![](https://github.com/doupengs/dpspider/blob/master/image/6.png)<br>
```markdown
6.Download类下载失败的[Error],从而response为None的[WARING]
```

![](https://github.com/doupengs/dpspider/blob/master/image/7.png)<br>
```markdown
7.使用代理和更换代理的[INFO]
```

# insertmysql.py

#### insertmysql简介

```markdown
数据写入模块
如果数据插入失败会生成 fail.log
可以选择是否生成违反主键唯一约束条件的插入语句，即 repeat.log
```

# parser.py

#### parser简介

```markdown
选择 xpath 和 re 相结合的解析方法，方法很强大
```
点击了解[xpath](http://www.w3school.com.cn/xpath/)

# download.py

#### download简介

```markdown
可以选择是否使用代理下载
代理不能使用会自动更新下一个代理，还可以设置每个代理最大连续使用次数
```

# color.py

#### color简介

```markdown
可选是否带有颜色打印，或者什么都不打印
```

# 反馈与建议

* 希望反馈您的宝贵意见、建议和使用中的BUG.
* GITHUP地址：[窦朋 | doupeng](https://github.com/doupengs)
* 微信公众号：[人生苦短遂学python](https://mp.weixin.qq.com/mp/homepage?__biz=MzI5MzI5NTQ4Mg==&hid=1&sn=fde1700cb5532eb84d227b1f6ded6838&uin=Njg4NTExNDQw&key=9ed31d4918c154c8f98e46aaf51029e25d006894bd336605c9ea269077414f400da2fd9110bf7810e535c7ca20c6c5b603eab7f647d52d77496e30ce9f13d357022d8408093b3456b3ce82c9a9069ceb&devicetype=Windows+10&version=62030053&lang=zh_CN&winzoom=1)
* 邮箱：<doupeng1993@sina.com>
