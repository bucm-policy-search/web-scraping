主要采用scrapy库，具体内容见[scrapy文档](https://docs.scrapy.org/en/latest/intro/tutorial.html)，调试时可使用[scrapy shell](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data)协助调试（记得也要修改Shell的User-Agent）

## 启动虚拟环境
1. 进入本仓库对应文件夹，然后`source developEnv/bin/activate`.（退出虚拟环境用`deactivate`）
2. 如果没有安装scrapy，请在虚拟环境内执行`pip install scrapy`
3. 启动对应的项目文件夹中（如developEnv/webSpider，即`scrapy.cfg`存在文件夹）`scrapy crawl policy -O input.json`开始爬虫

## 常见问题
### 被创宇云防御（云WAF类）拦下

过一两分钟就又放行了。然后注意修改User-Agent。

Scrapy Shell 启动时要加入相关参数：`scrapy shell -s USER_AGENT='custom user agent' 'http://www.example.com'`
比如 scrapy shell -s USER_AGENT='Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)' 'http://zyj.beijing.gov.cn/sy/tzgg/'

scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77' 'http://zyj.beijing.gov.cn/sy/tzgg/'

### 如何批量导入爬取的数据
在用jq 对json解码后，用官方[bulk api](ec4\u7ec7\u884c\u4e1a\u4e13\u5bb6\u5bf9\u5019\u9009\u4eba\u8fdb\u884c\u884c\u4e1a\u590d\u8bc4\uff0c\u63d0\u51fa\u521d\u6b65\u4eba\u9009\u3002</p><p><strong>\u3000\u3000\uff08\u56db\)（此处给的是Node.js版本）。**原回答废弃**原因是，对于jq转换成的`\"`，echo、printf等其他输出函数在pipe输出时会将json值中的`\"`在bulk前就转换成`"`，从而导致输入到elasticsearch中出错。且暂时无解，'\\'等常见转义字符可以取消转换，但暂未见到针对`\"`解决方式的回答。
**原回答（废弃不用）**：导入`[{},{}]`类型Json文件，参考[此elasticsearch回答](https://stackoverflow.com/questions/33340153/elasticsearch-bulk-index-json-data/33340234#33340234)使用[elastic bulk REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)

## 注意事项
1. 用scrapy库时记得要用virtualenv或conda等创建虚拟环境
2. 涉及正则部分可阅读[learn-regex-zh](https://github.com/cdoco/learn-regex-zh)，并借助诸如[regex101](https://regex101.com/)、[scrapy command line](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data)工具来辅助获取内容
3. 如何将`\uxxxx`格式代码转换为对应的汉字：安装`jq`，并执行诸如`cat in.json | jq > out.json`代码。另外，强烈推荐学一学jq，最慢10分钟能看完的[Tutorial](https://stedolan.github.io/jq/tutorial/)能解决非常多常见的JSON转换问题，JSON利器。

## 爬虫目录
### 北京市中医药管理局
截至2021-04-19该网站没有发现robots.txt文件
- 通知公告（http://zyj.beijing.gov.cn/sy/tzgg/）
- 政策法规（http://zyj.beijing.gov.cn/sy/zcfg/）
- 政策解读（http://zyj.beijing.gov.cn/zcjd/wjjd/）

2021-05-04用scrapy shell再次爬取网站时时，发现网站又进行升级，能触发scrapy shell防护（之前scrapy shell没有问题）:sob::sob:

![知道创宇云防御](https://i.imgur.com/LsIQpIL.png)

不过发现很好破解，拦截是由于我的scrapy shell没有加user-agent参数。加上user-agent一切又正常了。



