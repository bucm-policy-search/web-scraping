## 如何使用

- 按照官方教程安装 [pdm](https://pdm.fming.dev/)， 使用pdm管理python包是因为python的原生包管理和Node相比实在是灾难，输出的`requirements.txt`有大堆普通开发者或使用者不想关注的细节（包），无法分清包依赖关系
- `git clone`下载仓库内容
- 在仓库根目录执行`pdm install`
- 安装过程中，可以从Docker的Elasticsearch容器中将`.crt`文件复制到本仓库中
- （可选）如果需要爬虫时自动将数据存储到后台的数据库，在`README.md`同层目录创建`.env`文件，配置如下内容

  ```
  # change the following "CHANGEME" to real params
  USERNAME=CHANGEME
  PASSWORD=CHANGEME

  HOST=localhost
  PORT=9200
  URL=https://${HOST}:${PORT}

  ES_INDEX=CHANGEME
  CERT="ca.crt"
  ```

### 后台定时爬虫

- 找到`start_crawl.py`所在位置并用 [pm2](https://pm2.keymetrics.io/) 后台管理
- 找到当前虚拟环境所在地址（绝对路径），替代下面的 /path/to/venv/bin/python

代码样例：`pm2 start start_crawl.py --interpreter=/path/to/venv/bin/python`

该样例会在每天默认时间开启全网页爬虫。你也可通过 `python start_crawl.py -h`获取更多参数相关信息

### 单次爬虫

1. 进入虚拟环境并启动虚拟环境：`source developEnv/bin/activate`（退出虚拟环境用`deactivate`）
2. 进入对应的项目文件夹中（如 venv/webSpider，即`scrapy.cfg`存在文件夹），可执行对应 spider，如`scrapy crawl BATCM -O output/result.json`。**注意：**使用默认设置会爬取某网页 2 个子页面内包含的所有子网页，而且为了防止被反爬虫限制了爬取速度，速度较慢，预计需 5 分钟

## 常见问题

### 被创宇云防御（云 WAF 类）拦下

过一两分钟可继续正常访问，注意要到文件根目录（含`scrapy.cfg`）运行`scrapy shell`；或修改 `User-Agent`，如`scrapy shell -s USER_AGENT='Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)' 'http://zyj.beijing.gov.cn/sy/tzgg/'`

### 如何手动批量导入爬取的 json 格式数据

**新回答**：在用 jq 对 json 解码后，用官方[bulk api](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)（此处给的是 Node.js 版本）。**原回答废弃**原因是，对于 jq 转换成的`\"`，echo、printf 等其他输出函数在 pipe 输出时会将 json 值中的`\"`在 bulk 前就转换成`"`，从而导致输入到 Elasticsearch 中出错。且暂时无解，'\\'等常见转义字符可以取消转换，但暂未见到针对`\"`解决方式的回答。

**原回答（废弃不用）**：导入`[{},{}]`类型 Json 文件，参考[此 elasticsearch 回答](https://stackoverflow.com/questions/33340153/elasticsearch-bulk-index-json-data/33340234#33340234)使用[elastic bulk REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)

## 网络异常，Console 出现大量报错

如出现大批量诸如 "OSError: [Error 101] Network is unreachable" 之类的错误，静等 1~2 分钟，等错误所有都跳过即可。在不用“梯子”的情况下，`fake-useragent`无法访问 `w3schools`, `heroku` 之类的数据源，且会多次重试链接。虽然无法使用随机 UA，已设置了默认的 UA，错误不用理会。

## 注意事项

1. **建议**熟悉 scrapy 库（可参照[scrapy 文档](https://docs.scrapy.org/en/latest/intro/tutorial.html)），并使用[scrapy shell](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data)协助调试（记得要修改 Shell 的 User-Agent）。
2. 用 scrapy 库时记得要用 virtualenv 或 conda 等创建虚拟环境
3. 涉及正则部分可阅读 [learn-regex-zh](https://github.com/cdoco/learn-regex-zh)，并借助诸如 [regex101](https://regex101.com/)、[scrapy command line](https://docs.scrapy.org/en/latest/intro/tutorial.html#extracting-data) 工具来辅助获取内容
4. 如何将`\uXXXX`格式代码转换为对应的汉字：安装`jq`，并执行诸如`cat in.json | jq > out.json`代码。另外，强烈推荐学一学 jq， 该[Tutorial](https://stedolan.github.io/jq/tutorial/)10 分钟。jq 能解决非常多常见的 JSON 转换问题，实属 JSON 利器
5. 本仓库 python 的`linter`和`formatter`分别使用了`flake8`和`black`

## 爬虫目录

详见[crawling-catalog.md](./crawling-catalog.md)
