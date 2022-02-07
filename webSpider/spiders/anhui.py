import scrapy
from webSpider.items import ElasticSearchItem
import re
from datetime import date
from w3lib.html import remove_tags
from gerapy_auto_extractor import extract_list
from gerapy_auto_extractor.helpers import content, jsonify
import os
import json


class AHTCM(scrapy.Spider):
    name = "AHTCM"
    # 安徽省中医药管理局
    allowed_domains = ["wjw.ah.gov.cn"]

    def __init__(self, mode=None):
        self.mode = mode

    def start_requests(self):
        urls = {
            True: [
                "http://wjw.ah.gov.cn/ztzl/zyygljzt/jgzz/index.html",
                "http://wjw.ah.gov.cn/content/column/6792061?pageIndex=1",
                "http://wjw.ah.gov.cn/content/column/6792051?pageIndex=2",
            ],
            False: ["http://wjw.ah.gov.cn/ztzl/zyygljzt/jgzz/index.html"],
        }[hasattr(self, "mode") and self.mode == "prod"]
        for url in urls:
            if url[-4:] == "html":
                yield scrapy.Request(url=url, callback=self.details_2)
            else:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response.body.decode("utf-8")
        with open("test.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        html = content("test.html")
        os.remove("test.html")
        url_list = json.loads(jsonify(extract_list(html)))
        for i in url_list:
            url = i["url"]
            yield scrapy.Request(url=url, callback=self.details)

    def details(self, response):
        item = ElasticSearchItem()
        response.body.decode("utf-8")

        publishingDate = re.findall(
            "(\d{4}-\d{1,2}-\d{1,2})", response.xpath("//div[@class='newsinfoleft fl']/text()").extract_first())
        article = response.xpath(
            "//div[@class='j-fontContent newscontnet minh300']//text()").extract()
        plaintext = re.sub(r"\s(\s)+", " ", remove_tags(str(article)))
        title = response.xpath("//h1/text()").extract_first()
        scrapy_date = date.today().strftime("%Y-%m-%d")
        attachment = ""

        item["publishingDate"] = publishingDate
        item["article"] = remove_tags(article, which_ones=("div"))
        item["plaintext"] = plaintext
        item["title"] = title
        item["urlSource"] = response.url
        item["source"] = "安徽省中医药管理局"
        item["scrapyDate"] = scrapy_date
        item["attachment"] = attachment

        yield item

    def details_2(self, response):
        item = ElasticSearchItem()
        response.body.decode("utf-8")

        publishingDate = ""
        article = response.xpath(
            "//div[@class='ptlmcontent']//text()").extract()
        plaintext = re.sub(r"\s(\s)+", " ", remove_tags(str(article)))
        title = response.xpath("//h2/text()").extract_first()
        scrapy_date = date.today().strftime("%Y-%m-%d")
        attachment = ""

        item["publishingDate"] = publishingDate
        item["article"] = remove_tags(article, which_ones=("div"))
        item["plaintext"] = plaintext
        item["title"] = title
        item["urlSource"] = response.url
        item["source"] = "安徽省中医药管理局"
        item["scrapyDate"] = scrapy_date
        item["attachment"] = attachment

        yield item
