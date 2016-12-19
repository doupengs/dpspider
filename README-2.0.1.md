# dpspider-2.0.1 目录新增内容

* [masterspider.py](#masterspiderpy)
 * [masterspider简介](#masterspider简介)
* [downloadworker.py](#downloadworkerpy)
 * [downloadworker简介](#downloadworker简介)

#	masterspider.py

#### masterspider简介

```markdown
继承于 Spider类，可以将下载任务交给其他服务器
masterspider 负责发布任务，解析 downloadworker 下载的 response 和 入库操作
```

* 点击查看 [testMaster.py](https://github.com/doupengs/dpspider/blob/master/test/testMaster.py) `实例源码` 

# downloadworker.py

#### downloadworker简介

```markdown
负责为 masterspider 下载 response 的工作者
只需匹配上 masterspider 的 ip 和 秘钥，其他参数由 masterspider 传递
```

* 点击查看 [testWorker.py](https://github.com/doupengs/dpspider/blob/master/test/testWorker.py) `实例源码` 
