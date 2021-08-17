爬虫默认遵守各网站`robots.txt`设置规则

## 国家中医药管理局（NATCM/SATCM）

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

## 北京市中医药管理局（BATCM）

截至 2021-04-19 [北京市中医药管理局](http://zyj.beijing.gov.cn/sy/tzgg/) 没有发现 `robots.txt` 文件

爬取内容：

- 通知公告 http://zyj.beijing.gov.cn/sy/tzgg/
- 政策法规 http://zyj.beijing.gov.cn/sy/zcfg/
- 政策解读 http://zyj.beijing.gov.cn/zcjd/wjjd/

## 天津市中医药管理局 (404 Not Found)

## 河北省中医药管理局 （HCOHP）

内容在河北省卫生健康委员会网站上

截至 2021-08-17 [河北省卫生健康委员会](http://wsjkw.hebei.gov.cn/) 官网 `robots.txt` 内容为

```
User-agent:*
Disallow:/db_backup_1491040787/  #DB crash data
Disallow:/website_backup_1491040787/
```

爬取内容：

- 综合管理 http://wsjkw.hebei.gov.cn/zhgl/index.jhtml
- 政策法规 http://wsjkw.hebei.gov.cn/zyzcfg/index.jhtml
