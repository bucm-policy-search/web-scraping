from urllib.parse import urljoin
import scrapy
from webSpider.items import ElasticSearchItem
import re
from datetime import date
from w3lib.html import remove_tags


class SATCM(scrapy.Spider):
    name = "SATCM"
    # 陕西省中医药管理局
    allowed_domains = ["atcm.shaanxi.gov.cn"]

    def __init__(self, mode=None):
        self.mode = mode

    def start_requests(self):
        urls = {
            True: [
                "http://atcm.shaanxi.gov.cn/bsfw/xzzq/",
                "http://atcm.shaanxi.gov.cn/sy/dtyw/index.html",
                "http://atcm.shaanxi.gov.cn/zfxxgk/zcjd/",
                "http://atcm.shaanxi.gov.cn/zfxxgk/zfxxgknb/",
                "http://atcm.shaanxi.gov.cn/zfxxgk/zfxxgkzn/",
                "http://atcm.shaanxi.gov.cn/zfxxgk/zfxxgkzd/",
            ],
            False: ["http://atcm.shaanxi.gov.cn/bsfw/xzzq/"],
        }[hasattr(self, "mode") and self.mode == "prod"]
        if len(urls) == 1:
            yield scrapy.Request(url=urls[0], callback=self.parse)  # 下载专区
        else:
            for i in range(6):
                if i == 0:
                    # 下载专区
                    yield scrapy.Request(url=urls[i], callback=self.parse)
                elif i == 1:
                    # 动态要闻
                    yield scrapy.Request(url=urls[i], callback=self.parse)
                    for i in range(1, 60):
                        url = "http://atcm.shaanxi.gov.cn/sy/dtyw/index_{}.html".format(
                            i)
                        yield scrapy.Request(url=url, callback=self.parse)
                elif i == 2:
                    # 政策解读
                    yield scrapy.Request(url=urls[i], callback=self.parse)
                    for i in range(1, 4):
                        url = "http://atcm.shaanxi.gov.cn/sy/dtyw/index_{}.html".format(
                            i)
                        yield scrapy.Request(url=url, callback=self.parse)
                elif i == 3:
                    # 政府信息公开年报
                    yield scrapy.Request(url=urls[i], callback=self.parse)
                elif i == 4:
                    yield scrapy.Request(
                        url=urls[i], callback=self.content_pattern2
                    )  # 政府信息公开指南(无二级链接)
                elif i == 5:
                    yield scrapy.Request(
                        url=urls[i], callback=self.content_pattern2
                    )  # 政府信息公开制度(无二级链接)

    def parse(self, response):
        if response.status == 404:
            return
        if response.url == "http://atcm.shaanxi.gov.cn/bsfw/xzzq/":
            url_list = response.xpath("//li[@class='clearfix']")
            for i in url_list:
                url = response.urljoin(i.xpath("./a/@href").extract_first())
                if url is not None:
                    yield scrapy.Request(url=url, callback=self.content_pattern1)
        else:  # i=1,2,3
            url_list = response.xpath("//a[@class='f-otw']")
            for i in url_list:
                url_origin = response.urljoin(
                    i.xpath("./@href").extract_first())
                if url_list is not None:
                    yield scrapy.Request(url=url_origin, callback=self.content_pattern1)

    # 解析网页,i=0,1,2,3
    def content_pattern1(self, response):
        item = ElasticSearchItem()

        publishingDate = response.xpath(
            "//span[@class='con']/text()").extract_first()

        item["publishingDate"] = publishingDate
        article = response.xpath(
            "//div[@class='detail-con content']").extract()
        item["article"] = remove_tags(article, which_ones=("div"))
        plaintext = re.sub(r"\s(\s)+", " ", remove_tags(str(article)))
        item["plaintext"] = plaintext

        title = response.xpath("//h1/text()").extract_first()
        item["title"] = title

        item["urlSource"] = response.url
        item["source"] = "陕西省中医药管理局"

        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        item["scrapyDate"] = d1

        attachment = []
        a_list = re.findall(r"<a.*?do.\w{0,1}.*?a>", response.text)
        for i in a_list:
            link = response.url[:44] + re.findall(r"P.*?do.\w{0,1}", i)[0]
            mark = re.findall(r">.*?<", i)[0]
            if len(mark) <= 2:
                continue
            attachment.append({"mark": mark[1:-1], "link": link})
        item["attachment"] = attachment
        yield item

    def content_pattern2(self, response):
        item = ElasticSearchItem()
        item["source"] = "陕西省中医药管理局"
        title = response.xpath("//h1[@class='tit']/text()").extract_first()
        item["title"] = title
        item["urlSource"] = response.url
        article = response.css(".con-box").get()
        item["article"] = remove_tags(article, which_ones=("div"))
        plaintext = re.sub(r"\s(\s)+", " ", remove_tags(article))
        item["plaintext"] = plaintext
        item["publishingDate"] = ""
        yield item
