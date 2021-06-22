## 创建目的

促进中医药信息化发展。由于缺少政策搜索引擎，在查找中医药相关政策有时非常麻烦。故想创建一个方便中医药院校广大师生、中医药从政人员以及中医药爱好者使用的搜索引擎。

## 如何执行此仓库

建议用`conda`或`virtualenv`创建虚拟环境。运行`pip install -r requirements.txt`安装所有依赖包

### 后台定点爬虫

用pm2，代码如`pm2 start echo.py --interpreter=/path/to/venv/bin/python`

### 单次爬虫

1. 进入本仓库对应文件夹，然后`source developEnv/bin/activate`.（退出虚拟环境用`deactivate`）
2. 【建议但非必须】熟悉 scrapy 库（可参照[scrapy 文档](https://docs.scrapy.org/en/latest/intro/tutorial.html)），并使用[scrapy shell](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data)协助调试（记得要修改 Shell 的 User-Agent）。如`scrapy shell -s USER_AGENT='Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)' `'http://zyj.beijing.gov.cn/sy/tzgg/'
3. 进入对应的项目文件夹中（如 developEnv/webSpider，即`scrapy.cfg`存在文件夹）`scrapy crawl policy -O result.json`开始爬虫。**注意：**默认设置会爬取三个网页的所有子网页，所以会很慢，5 分钟左右，谨慎执行。

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
4. 本仓库python的`linter`和`formatter`分别使用了`flake8`和`black`

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
