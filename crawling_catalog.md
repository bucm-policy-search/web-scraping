## 目录

示意：&#9744; 表示尚未完成，&#9745; 表示已完成， &#9746; 表示对应机构网站不存在。

只爬取以`.gov.cn`为后缀的域名网站

以下是中国大陆境内中医药管理局机构的详细名单及对应网站爬取情况（排名不分先后）

&#9745; [国家中医药管理局](http://www.natcm.gov.cn/)

&#9745; [北京市中医药管理局](http://zyj.beijing.gov.cn/)

&#9746; 天津市中医药管理局

&#9744; [上海市中医药管理局（上海市卫生健康委员会）](https://wsjkw.sh.gov.cn/)

&#9746; 重庆市中医药管理局

&#9745; 河北省中医药管理局

&#9744; 山西省中医药管理局

&#9746; 辽宁省中医药管理局

&#9744; 吉林省中医药管理局

&#9746; 黑龙江省中医药管理局

&#9744; 江苏省中医药管理局

&#9744; 浙江省中医药管理局

&#9744; 安徽省中医药管理局

&#9744; 福建省中医药管理局

&#9744; 江西省中医药管理局

&#9746; 山东省中医药管理局

&#9744; 河南省中医药管理局

&#9746; 湖北省中医药管理局

&#9744; 湖南省中医药管理局

&#9744; 广东省中医药局

&#9746; 海南省中医药管理局

&#9744; 四川省中医药管理局

&#9744; 贵州省中医药管理局

&#9746; 云南省中医药管理局

&#9744; 陕西省中医药管理局

&#9744; 广西壮族自治区中医药管理局

&#9746; 内蒙古自治区中医药管理局

&#9746; 西藏自治区中医药管理局

&#9746; 宁夏回族自治区中医药管理局

&#9746; 新疆维吾尔自治区中医药管理局

## 详细内容

爬虫默认遵守各网站`robots.txt`设置规则

### 国家中医药管理局（NATCM/SATCM）

截至 2021-06-11 [国家中医药管理局](http://www.natcm.gov.cn/) 官网 `robots.txt` 内容为

```txt
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

### 北京市中医药管理局（BATCM）

截至 2021-04-19 [北京市中医药管理局](http://zyj.beijing.gov.cn/) 没有发现 `robots.txt` 文件

爬取内容：

- 通知公告 http://zyj.beijing.gov.cn/sy/tzgg/
- 政策法规 http://zyj.beijing.gov.cn/sy/zcfg/
- 政策解读 http://zyj.beijing.gov.cn/zcjd/wjjd/

### 天津市中医药管理局 (404 Not Found)

### 河北省中医药管理局 （HCOHP）

内容在河北省卫生健康委员会网站上

截至 2021-08-17 [河北省卫生健康委员会](http://wsjkw.hebei.gov.cn/) 官网 `robots.txt` 内容为

```txt
User-agent:*
Disallow:/db_backup_1491040787/  #DB crash data
Disallow:/website_backup_1491040787/
```

爬取内容：

- 综合管理 http://wsjkw.hebei.gov.cn/zhgl/index.jhtml
- 政策法规 http://wsjkw.hebei.gov.cn/zyzcfg/index.jhtml

### 陕西中医药管理局（SATCM）

截至 2021-08-17 [陕西省卫生健康委员会](http://atcm.shaanxi.gov.cn/) 没有发现 `robots.txt` 文件

爬取内容：

#### 模板一

- 动态要闻 http://atcm.shaanxi.gov.cn/sy/dtyw/

#### 模板二

- 下载专区 https://atcm.shaanxi.gov.cn/bsfw
- 政府信息公开指南 http://atcm.shaanxi.gov.cn/zfxxgk/zfxxgkzn/
- 政府信息公开实施细则 http://atcm.shaanxi.gov.cn/zfxxgk/zfxxgkzd/
- 政策解读 http://atcm.shaanxi.gov.cn/zfxxgk/zcjd/

#### 模板三

- 政府信息年度公开 http://atcm.shaanxi.gov.cn/zfxxgk/zfxxgknb/

### 山西省中医药管理局 （HCOSP）

内容在山西省卫生健康委员会网站上

截至 2021-08-17 [山西省卫生健康委员会](http://wjw.shanxi.gov.cn/) 没有发现 `robots.txt` 文件

- 综合管理 http://wjw.shanxi.gov.cn/zyygljl01/index.hrh
