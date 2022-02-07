import scrapy
import re
import sys
import requests
import logging
from webSpider.items import ElasticSearchItem
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from datetime import date
import random

##################################################################
#                           TO BE DONE                           #
##################################################################


class HCOHP(scrapy.Spider):

    # 河北省卫生健康委员会 (Health Commission of Hebei Province)
    name = "HCOHP"

    def __init__(self, mode=None):
        self.mode = mode

    def start_requests(self):
        item = ElasticSearchItem()

        urls = {
            True: [
                "http://wsjkw.hebei.gov.cn/zhgl/index.jhtml",
                "http://wsjkw.hebei.gov.cn/zyzcfg/index.jhtml",
            ],
            False: ["http://wsjkw.hebei.gov.cn/zyzcfg/index.jhtml"],
        }[hasattr(self, "mode") and self.mode == "prod"]

        for url in urls:
            # change url depending on pages
            for num in (
                range(1, 1000)
                if (hasattr(self, "mode") and self.mode == "prod")
                else range(1, 3)
            ):

                new_url = url

                if num != 1:
                    new_url = url[:-6] + f"_{num}.jhtml"

                if requests.head(
                    new_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                    },
                ).ok:
                    logging.debug(
                        "The new_url in start_request to HCOHP_contentPage: {}".format(
                            new_url
                        )
                    )
                    yield scrapy.Request(
                        url=new_url, callback=self.contentPage, meta={"item": item}
                    )
                else:
                    break

    def contentPage(self, response):
        content_urls = []
        item = response.meta["item"]
        # Check whether data exist (also check whether this page exist)
        if bool(response.css(".er-list2")):
            for quote in response.css(".er-list2").xpath("li"):
                url = response.urljoin(quote.css("a::attr(href)").get())
                if "html" not in url:
                    item["title"] = quote.xpath("a/text()").get()
                    item["article"] = quote.xpath("a/text()").get()
                    item["plaintext"] = quote.xpath("a/text()").get()
                    item["urlSource"] = url
                    item["source"] = "河北省中医药管理局"

                    today = date.today()
                    d1 = today.strftime("%Y-%m-%d")
                    item["scrapyDate"] = d1

                    tmpDate = quote.css("span::text").get()
                    item["publishingDate"] = re.search(r"\S+", tmpDate).group(0)

                    # 如果以下String不在URL中，则多半为微信公众号外链，这种情况保留网址就行
                    if "wsjkw.hebei.gov.cn" in url:
                        item["attachment"] = [
                            {"mark": quote.xpath("a/text()").get(), "link": url}
                        ]
                    else:
                        item["attachment"] = []

                    yield item

                else:
                    content_urls.append(
                        response.urljoin(quote.css("a::attr(href)").get())
                    )

            for content_url in content_urls:
                for num in range(0, 15):
                    yield scrapy.Request(
                        url=content_url, callback=self.detailPage, meta={"item": item}
                    )

    def detailPage(self, response):
        # self.logger.info('Hi, this is an item page! %s', response.url)
        item = response.meta["item"]

        item["urlSource"] = response.url

        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        item["scrapyDate"] = d1

        title_origin = response.css(".title::text").get()
        # delete "\n" and spaces in title
        title_new = title_origin.strip(" \n")
        item["title"] = re.sub(r"\s", "", title_new)

        date_origin = response.css(".fbsj2::text").get()
        # change    "时间：2020-12-10 15:40:19"    to      "2020-12-10"
        item["publishingDate"] = re.search(r"(?<=：)\S*", date_origin).group(0)

        item["source"] = "河北省卫生健康委员会 河北省中医药管理局"

        article = "".join(response.css(".con-txt").getall())
        item["article"] = remove_tags(article, which_ones=("div"))

        item["plaintext"] = re.sub(r"\s(\s)+", " ", remove_tags(article))

        attachment = []
        ul = response.css(".fjlist li")
        if ul != []:

            # 附件URL爬虫部分要移交前端，因为附件所在URL会随Timestamp实时改变

            for index, li in enumerate(ul):
                mark = li.css("a::text").get()
                attachment.append({"mark": mark, "link": response.url})

            item["attachment"] = attachment

            yield item
