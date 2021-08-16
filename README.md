## 创建目的

促进中医药信息化发展。由于缺少政策搜索引擎，在查找中医药相关政策有时非常麻烦。故想创建一个方便中医药院校广大师生、中医药从政人员以及中医药爱好者使用的搜索引擎。

## 项目优点

爬虫时可默认将爬虫数据导入到 Elasticsearch 中。如果检测没有连接到 Elasticsearch 或配置不正确，则不会将数据导入到 ES 中。你也可通过加`-O`参数将爬取内容导出为指定目录的`json`文件。

## 如何执行此仓库

- 用`conda`或`virtualenv`创建虚拟环境。
- `git clone`下载仓库内容
- 运行`pip install -r requirements.txt`安装所有依赖包
- （可选）如果需要爬虫时自动将数据存储到后台的数据库，在`README.md`同层目录创建`.env`文件，输入类似如下内容

  ```
  USERNAME=ELASTICSEARCH_CHANGEME
  PASSWORD=PASSWORD_CHANGEME
  HOST=localhost
  PORT=9200
  URL=${HOST}:${PORT}
  ES_INDEX=INDEX_CHANGEME
  ```

### 后台定时爬虫

- 找到`start_crawl.py`所在位置并用 [pm2](https://pm2.keymetrics.io/) 后台管理
- 找到当前虚拟环境所在地址，替代下面的 /path/to/venv/bin/python

代码样例：`pm2 start start_crawl.py --interpreter=/path/to/venv/bin/python`

该样例会在每天默认时间开启全网页爬虫。你也可通过 `python start_crawl.py -h`获取更多参数相关信息

### 单次爬虫

1. 进入虚拟环境并启动虚拟环境：`source developEnv/bin/activate`（退出虚拟环境用`deactivate`）
2. 进入对应的项目文件夹中（如 venv/webSpider，即`scrapy.cfg`存在文件夹），可执行对应 spider，如`scrapy crawl BATCM -O output/result.json`。**注意：**使用默认设置会爬取某网页 3 个子页面内包含的所有子网页，而且为了防止被反爬虫限制了爬取速度，速度较慢，预计需 5 分钟

## 常见问题

### 被创宇云防御（云 WAF 类）拦下

过一两分钟可继续正常访问，注意修改 `User-Agent` . Scrapy Shell 启动时要加入相关参数，如`scrapy shell -s USER_AGENT='Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)' 'http://zyj.beijing.gov.cn/sy/tzgg/'`

### 如何手动批量导入爬取的 json 格式数据

**新回答**：在用 jq 对 json 解码后，用官方[bulk api](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)（此处给的是 Node.js 版本）。**原回答废弃**原因是，对于 jq 转换成的`\"`，echo、printf 等其他输出函数在 pipe 输出时会将 json 值中的`\"`在 bulk 前就转换成`"`，从而导致输入到 Elasticsearch 中出错。且暂时无解，'\\'等常见转义字符可以取消转换，但暂未见到针对`\"`解决方式的回答。

**原回答（废弃不用）**：导入`[{},{}]`类型 Json 文件，参考[此 elasticsearch 回答](https://stackoverflow.com/questions/33340153/elasticsearch-bulk-index-json-data/33340234#33340234)使用[elastic bulk REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)

## 网络异常，Console 出现大量报错

如出现大批量诸如 "OSError: [Errno 101] Network is unreachable" 之类的错误

那是因为在不连接梯子的情况下，`fake-useragent`无法访问 `w3schools`, `heroku` 之类的数据源。用默认值忽视就行。

## 注意事项

1. **建议**熟悉 scrapy 库（可参照[scrapy 文档](https://docs.scrapy.org/en/latest/intro/tutorial.html)），并使用[scrapy shell](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data)协助调试（记得要修改 Shell 的 User-Agent）。
2. 用 scrapy 库时记得要用 virtualenv 或 conda 等创建虚拟环境
3. 涉及正则部分可阅读 [learn-regex-zh](https://github.com/cdoco/learn-regex-zh)，并借助诸如 [regex101](https://regex101.com/)、[scrapy command line](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data) 工具来辅助获取内容
4. 如何将`\uxxxx`格式代码转换为对应的汉字：安装`jq`，并执行诸如`cat in.json | jq > out.json`代码。另外，强烈推荐学一学 jq， 该[Tutorial](https://stedolan.github.io/jq/tutorial/)10 分钟。jq 能解决非常多常见的 JSON 转换问题，实属 JSON 利器
5. 本仓库 python 的`linter`和`formatter`分别使用了`flake8`和`black`

## 爬虫目录

### 国家中医药管理局（NATCM/SATCM）

截至 2021-06-11 [国家中医药管理局](http://www.natcm.gov.cn/) 官网 `robots.txt` 内容为

```
User-agent: *

Disallow: /d/
Disallow: /e/class/
Disallow: /e/config/
Disallow: /e/data/
Disallow: /e/enews/
Disallow: /e/update/
```

爬取内容：

- 通知公告 http://www.natcm.gov.cn/a/tzgg/
- 工作动态 http://www.natcm.gov.cn/a/gzdt/
- 新闻发布 http://www.natcm.gov.cn/a/bgs_xwfb/
- 政策文件 http://www.satcm.gov.cn/a/zcwj/
- 政策解读 http://www.satcm.gov.cn/a/zcjd/
- 法律法规 http://www.satcm.gov.cn/a/fjs_flfg/

对于在不同分类的相同文件，只保留一份

### 北京市中医药管理局（BATCM）

截至 2021-04-19 [北京市中医药管理局](http://zyj.beijing.gov.cn/sy/tzgg/) 没有发现 `robots.txt` 文件

爬取内容：

- 通知公告 http://zyj.beijing.gov.cn/sy/tzgg/
- 政策法规 http://zyj.beijing.gov.cn/sy/zcfg/
- 政策解读 http://zyj.beijing.gov.cn/zcjd/wjjd/
