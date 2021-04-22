主要采用scrapy库，具体内容见[scrapy文档](https://docs.scrapy.org/en/latest/intro/tutorial.html)

## 注意事项
1. 用scrapy库时记得要用virtualenv或conda等创建虚拟环境
2. 涉及正则部分可阅读[learn-regex-zh](https://github.com/cdoco/learn-regex-zh)，并借助诸如[regex101](https://regex101.com/)、[scrapy command line](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data)工具来辅助获取内容
3. 如何将`\uxxxx`格式代码转换为对应的汉字：安装`jq`，并执行诸如`cat in.json | jq > out.json`代码。另外，强烈推荐学一学jq，最慢10分钟能看完的[Tutorial](https://stedolan.github.io/jq/tutorial/)能解决非常多常见的Json转换问题，Json利器。
4. 导入`[{},{}]`类型Json文件，参考[此elasticsearch回答](https://stackoverflow.com/questions/33340153/elasticsearch-bulk-index-json-data/33340234#33340234)使用[elastic bulk REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)

## 爬虫目录
### 北京市中医药管理局
截至2021-04-19该网站没有发现robots.txt文件
- 通知公告（http://zyj.beijing.gov.cn/sy/tzgg/）
- 政策法规（http://zyj.beijing.gov.cn/sy/zcfg/）
- 政策解读（http://zyj.beijing.gov.cn/zcjd/wjjd/）