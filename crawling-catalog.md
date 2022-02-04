## 概括

示意：:pencil2: 表示尚未完成，:heavy_check_mark: 表示已完成， :x: 表示开发人员没有找到对应机构官方网站。

只爬取以`.gov.cn`为后缀的域名网站

以下是中国大陆境内中医药管理局机构的详细名单及对应网站爬取情况（排名不分先后）

:heavy_check_mark: [国家中医药管理局](#国家中医药管理局)

:heavy_check_mark: [北京市中医药管理局](#北京市中医药管理局)

:pencil2: [天津市中医药管理局](#天津市中医药管理局)

:pencil2: [上海市中医药管理局](#上海市中医药管理局)

:pencil2: [重庆市中医药管理局](#重庆市中医药管理局)

:heavy_check_mark: [河北省中医药管理局](#河北省中医药管理局)

:heavy_check_mark: [山西省中医药管理局](#山西省中医药管理局)

:pencil2: [辽宁省中医药管理局](#辽宁省中医药管理局)

:pencil2: [吉林省中医药管理局](#吉林省中医药管理局)

:pencil2: [黑龙江省中医药管理局](#黑龙江省中医药管理局)

:pencil2: [江苏省中医药管理局](#江苏省中医药管理局)

:pencil2: [浙江省中医药管理局](#浙江省中医药管理局)

:pencil2: [安徽省中医药管理局](#安徽省中医药管理局)

:pencil2: [福建省中医药管理局](#福建省中医药管理局)

:pencil2: [江西省中医药管理局](#江西省中医药管理局)

:pencil2: [山东省中医药管理局](#山东省中医药管理局)

:pencil2: [河南省中医药管理局](#河南省中医药管理局)

:pencil2: [湖北省中医药管理局](#湖北省中医药管理局)

:pencil2: [湖南省中医药管理局](#湖南省中医药管理局)

:pencil2: [广东省中医药管理局](#广东省中医药管理局)

:pencil2: [海南省中医药管理局](#海南省中医药管理局)

:pencil2: 四川省中医药管理局

:pencil2: 贵州省中医药管理局

:x: 云南省中医药管理局

:heavy_check_mark: [陕西省中医药管理局](:陕西省中医药管理局)

:pencil2: 广西壮族自治区中医药管理局

:x: 内蒙古自治区中医药管理局

:x: 西藏自治区中医药管理局

:x: 宁夏回族自治区中医药管理局

:x: 新疆维吾尔自治区中医药管理局

## 详细内容

爬虫默认遵守各网站`robots.txt`设置规则

### 国家中医药管理局
<!-- http://natcm.gov.cn 和 http://satcm.gov.cn 都指向同一个网站-->

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

### 北京市中医药管理局

截至 2021-04-19 [北京市中医药管理局](http://zyj.beijing.gov.cn/) 没有发现 `robots.txt` 文件

爬取内容：

- 通知公告 http://zyj.beijing.gov.cn/sy/tzgg/
- 政策法规 http://zyj.beijing.gov.cn/sy/zcfg/
- 政策解读 http://zyj.beijing.gov.cn/zcjd/wjjd/

### 上海市中医药管理局

内容在上海市卫生健康委员会网站上

截至 2022-02-02, 未在[上海市卫生健康委员会](http://wsjkw.sh.gov.cn/) 官网找到 `robots.txt` 

**（特殊！）需要试图获取搜索结果**

### 黑龙江省中医药管理局

内容在黑龙江省卫生健康委员会网站上

截至 2022-02-02, 未在[黑龙江省卫生健康委员会](http://wsjkw.hlj.gov.cn/) 官网找到 `robots.txt` 

**（特殊！）需要试图获取搜索结果**

### 天津市中医药管理局

截至 2022-02-03, 未在[天津市卫生健康委员会](http://wsjk.tj.gov.cn/) 官网找到 `robots.txt`

**（特殊！）需要试图获取搜索结果**

### 河北省中医药管理局

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

### 陕西省中医药管理局

截至 2021-08-17 [陕西省卫生健康委员会](http://atcm.shaanxi.gov.cn/) 没有发现 `robots.txt` 文件

爬取内容：

#### 模板一

- 动态要闻 http://atcm.shaanxi.gov.cn/sy/dtyw/

#### 模板二

- 下载专区 http://atcm.shaanxi.gov.cn/bsfw
- 政府信息公开指南 http://atcm.shaanxi.gov.cn/zfxxgk/zfxxgkzn/
- 政府信息公开实施细则 http://atcm.shaanxi.gov.cn/zfxxgk/zfxxgkzd/
- 政策解读 http://atcm.shaanxi.gov.cn/zfxxgk/zcjd/

#### 模板三

- 政府信息年度公开 http://atcm.shaanxi.gov.cn/zfxxgk/zfxxgknb/

### 山西省中医药管理局

内容在山西省卫生健康委员会网站上

截至 2021-08-17 [山西省卫生健康委员会](http://wjw.shanxi.gov.cn/) 没有发现 `robots.txt` 文件

- 综合管理 http://wjw.shanxi.gov.cn/zyygljl01/index.hrh

### 吉林省中医药管理局

截至2022-02-02 [吉林省中医药管理局](http://jltcm.jl.gov.cn/) 没有发现 `robots.txt` 文件

- 公开文件 http://jltcm.jl.gov.cn/tzgg/xgdt/
- 公示公告 http://jltcm.jl.gov.cn/tzgg/gsgg/
- 政策解读 http://jltcm.jl.gov.cn/zwgk/zcjd/

### 江苏省中医药管理局

截至2022-02-02 [江苏省中医药管理局](http://wjw.jiangsu.gov.cn/col/col57216/index.html) 没有发现 `robots.txt` 文件

- 政策法规 http://wjw.jiangsu.gov.cn/col/col57222/index.html
- 部门文件 http://wjw.jiangsu.gov.cn/col/col57223/index.html
- 财政信息 http://wjw.jiangsu.gov.cn/col/col57224/index.html
- 公示公告 http://wjw.jiangsu.gov.cn/col/col57225/index.html

### 浙江省中医药管理局

与浙江省卫健委信息合并

截至2022-02-02 [浙江省中医药管理局](https://wsjkw.zj.gov.cn/) 没有发现 `robots.txt` 文件

**（特殊！）需要试图获取搜索结果**

### 辽宁省中医药管理局

截至2022-02-04 [辽宁省卫生健康委](http://wsjk.ln.gov.cn/) 没有发现 `robots.txt` 文件

- 中医管理 http://wsjk.ln.gov.cn/wst_xxgk/wst_ywpd/wst_zygl/

### 重庆市中医药管理局

截至2022-02-04 [重庆市中医药管理局](http://wsjkw.cq.gov.cn/) 没有发现 `robots.txt` 文件

**（特殊！）需要试图获取搜索结果**

### 安徽省中医药管理局

截至2022-02-04 [安徽省中医药管理局](http://wjw.ah.gov.cn/zyyglj/index.html) 没有发现 `robots.txt` 文件

- 机构职责 http://wjw.ah.gov.cn/ztzl/zyygljzt/jgzz/index.html
- 文件通知 http://wjw.ah.gov.cn/ztzl/zyygljzt/zyyztsy/wjtz/index.html
- 政策法规 http://wjw.ah.gov.cn/ztzl/zyygljzt/zyyztsy/zcfg/index.html

### 福建省中医药管理局

截至2022-02-04 [福建省中医药管理局](http://wjw.fujian.gov.cn/) 没有发现 `robots.txt` 文件

**（特殊！）需要试图获取搜索结果**

### 江西省中医药管理局

截至2022-02-04 [江西省中医药管理局](http://hc.jiangxi.gov.cn/col/col38208/index.html) 没有发现 `robots.txt` 文件

- 工作动态 http://hc.jiangxi.gov.cn/col/col38209/index.html
- 通知公告 http://hc.jiangxi.gov.cn/col/col38210/index.html
- 政策法规 http://hc.jiangxi.gov.cn/col/col38211/index.html
- 医政医管 http://hc.jiangxi.gov.cn/col/col38212/index.html
- 科技教育 http://hc.jiangxi.gov.cn/col/col38213/index.html
- 产业促进 http://hc.jiangxi.gov.cn/col/col38214/index.html
- 表格下载 http://hc.jiangxi.gov.cn/col/col47102/index.html

### 山东省中医药管理局

截至2022-02-04 [山东省中医药管理局](http://wsjkw.shandong.gov.cn/) 没有发现 `robots.txt` 文件

**（特殊！）需要试图获取搜索结果**

### 河南省中医药管理局

截至2022-02-04 [河南省中医药管理局](https://www.tcm.gov.cn/) 没有发现 `robots.txt` 文件

- 中医动态 https://www.tcm.gov.cn/xxfb/zydt/
- 中医管理 https://www.tcm.gov.cn/zfxxgk/fdzdgknr/zygl/
- 公告公示 https://www.tcm.gov.cn/zfxxgk/fdzdgknr/tzgg/

### 湖北省中医药管理局

截至2022-02-04 [湖北省中医药管理局](http://wjw.hubei.gov.cn/) 没有发现 `robots.txt` 文件

**（特殊！）需要试图获取搜索结果**

### 湖南省中医药管理局

截至2022-02-04 [湖南省中医药管理局](http://tcm.hunan.gov.cn/) 没有发现 `robots.txt` 文件

- 中医药要闻 http://tcm.hunan.gov.cn/tcm/xxgk/xwzx/zyyw/index.html
- 行业动态 http://tcm.hunan.gov.cn/tcm/xxgk/xwzx/hydt/index.html
- 时政要闻 http://tcm.hunan.gov.cn/tcm/xxgk/xwzx/szyw/index.html
- 通知公告 http://tcm.hunan.gov.cn/tcm/xxgk/tzgg/index.html
- 财政信息 http://tcm.hunan.gov.cn/tcm/xxgk/czxx/index.html

### 广东省中医药管理局

截至2022-02-04 [广东省中医药管理局](http://szyyj.gd.gov.cn/) 没有发现 `robots.txt` 文件

- 工作动态 http://szyyj.gd.gov.cn/zwyw/gzdt/
- 新闻发布会 http://szyyj.gd.gov.cn/zwyw/xwfbh/
- 政策文件 http://szyyj.gd.gov.cn/zwyw/bmwj/
- 建议提案 http://szyyj.gd.gov.cn/zwgk/jyta/
- 政策解读 http://szyyj.gd.gov.cn/hdjl/zcjd/
- 统计信息 http://szyyj.gd.gov.cn/zwgk/tjxx/
- 公告公示 http://szyyj.gd.gov.cn/zwgk/gsgg/
- 重点领域信息公开 http://szyyj.gd.gov.cn/zwgk/zdly/
- 政务五公开
  - 决策公开 http://szyyj.gd.gov.cn/zwgk/wgk/jcgk/
  - 执行公开 http://szyyj.gd.gov.cn/zwgk/wgk/zxgk/
  - 管理公开 http://szyyj.gd.gov.cn/zwgk/wgk/glgk/
  - 服务公开 http://szyyj.gd.gov.cn/zwgk/wgk/fwgk/
  - 结果公开 http://szyyj.gd.gov.cn/zwgk/wgk/jggk/
- 工作报表 http://szyyj.gd.gov.cn/zwgk/xxgknb/
- 数据发布 http://szyyj.gd.gov.cn/zwgk/sjfb/

### 海南省中医药管理局

截至2022-02-04 [海南省中医药管理局](http://wst.hainan.gov.cn/swjw/index.html) 没有发现 `robots.txt` 文件

**（特殊！）需要试图获取搜索结果**
