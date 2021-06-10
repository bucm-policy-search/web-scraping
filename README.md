## 如何执行此仓库

1. 进入本仓库对应文件夹，然后`source developEnv/bin/activate`.（退出虚拟环境用`deactivate`）
2. 如果没有安装 scrapy，请在虚拟环境内执行`pip install scrapy`
3. 【建议但非必须】熟悉 scrapy 库（可参照[scrapy 文档](https://docs.scrapy.org/en/latest/intro/tutorial.html)），并使用[scrapy shell](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data)协助调试（记得要修改 Shell 的 User-Agent）。如`scrapy shell -s USER_AGENT='Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)' `'http://zyj.beijing.gov.cn/sy/tzgg/'
4. 进入对应的项目文件夹中（如 developEnv/webSpider，即`scrapy.cfg`存在文件夹）`scrapy crawl policy -O result.json`开始爬虫。**注意：**默认设置会爬取三个网页的所有子网页，所以会很慢，5 分钟左右，谨慎执行。

## 常见问题

### 被创宇云防御（云 WAF 类）拦下

过一两分钟就又放行了。然后注意修改 User-Agent. Scrapy Shell 启动时要加入相关参数：`scrapy shell -s USER_AGENT='custom user agent' 'http://www.example.com'`

### 如何批量导入爬取的数据

**新回答**：在用 jq 对 json 解码后，用官方[bulk api](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)（此处给的是 Node.js 版本）。**原回答废弃**原因是，对于 jq 转换成的`\"`，echo、printf 等其他输出函数在 pipe 输出时会将 json 值中的`\"`在 bulk 前就转换成`"`，从而导致输入到 elasticsearch 中出错。且暂时无解，'\\'等常见转义字符可以取消转换，但暂未见到针对`\"`解决方式的回答。

**原回答（废弃不用）**：导入`[{},{}]`类型 Json 文件，参考[此 elasticsearch 回答](https://stackoverflow.com/questions/33340153/elasticsearch-bulk-index-json-data/33340234#33340234)使用[elastic bulk REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)

## 注意事项

1. 用 scrapy 库时记得要用 virtualenv 或 conda 等创建虚拟环境
2. 涉及正则部分可阅读[learn-regex-zh](https://github.com/cdoco/learn-regex-zh)，并借助诸如[regex101](https://regex101.com/)、[scrapy command line](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data)工具来辅助获取内容
3. 如何将`\uxxxx`格式代码转换为对应的汉字：安装`jq`，并执行诸如`cat in.json | jq > out.json`代码。另外，强烈推荐学一学 jq，最慢 10 分钟能看完的[Tutorial](https://stedolan.github.io/jq/tutorial/)能解决非常多常见的 JSON 转换问题，JSON 利器。

## 爬虫目录

### 北京市中医药管理局

截至 2021-04-19 该网站没有发现 robots.txt 文件

- 通知公告（ http://zyj.beijing.gov.cn/sy/tzgg/ ）
- 政策法规（ http://zyj.beijing.gov.cn/sy/zcfg/ ）
- 政策解读（ http://zyj.beijing.gov.cn/zcjd/wjjd/ ）

2021-05-04 用 scrapy shell 再次爬取网站时时，发现网站又进行升级，能触发 scrapy shell 防护（之前 scrapy shell 没有问题）:sob::sob:

![知道创宇云防御](https://i.imgur.com/LsIQpIL.png)

不过好在非常容易破解，详见常见问题