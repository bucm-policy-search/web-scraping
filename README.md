主要采用scrapy库，具体内容见[scrapy文档](https://docs.scrapy.org/en/latest/intro/tutorial.html)

## 注意事项
1. 用scrapy库时记得要用virtualenv或conda等创建虚拟环境
2. 涉及正则部分可阅读[learn-regex-zh](https://github.com/cdoco/learn-regex-zh)，并借助诸如[regex101](https://regex101.com/)、[scrapy command line](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data)工具来辅助获取内容

## 爬虫目录
### 北京市中医药管理局
截至2021-04-19该网站没有发现robots.txt文件
- 通知公告（http://zyj.beijing.gov.cn/sy/tzgg/）
- 政策法规（http://zyj.beijing.gov.cn/sy/zcfg/）
- 政策解读（http://zyj.beijing.gov.cn/zcjd/wjjd/）