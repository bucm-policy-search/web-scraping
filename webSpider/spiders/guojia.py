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


class NATCM(scrapy.Spider):

    # 国家中医药管理局 (National Administration of Traditional Chinese Medicine)
    name = "NATCM"

    page_urls = []

    def __init__(self, mode=None):
        self.mode = mode

    def start_requests(self):
        item = ElasticSearchItem()

        urls = {
            True: [
                "http://www.natcm.gov.cn/a/tzgg/",
                "http://www.natcm.gov.cn/a/gzdt/",
                "http://www.natcm.gov.cn/a/bgs_xwfb/",
                "http://www.satcm.gov.cn/a/zcwj/",
                "http://www.satcm.gov.cn/a/zcjd/",
                "http://www.satcm.gov.cn/a/fjs_flfg/",
            ],
            False: ["http://www.natcm.gov.cn/a/tzgg/"],
        }[hasattr(self, "mode") and self.mode == "prod"]

        for url in urls:
            # change url depending on pages
            for num in (
                # page 1 url : "http://www.natcm.gov.cn/a/tzgg/index.html"
                # page 2 url : "http://www.natcm.gov.cn/a/tzgg/index_2.html"
                range(1, 1000)
                if (hasattr(self, "mode") and self.mode == "prod")
                else range(1, 3)
            ):
                # eg. default fetch data from 'http://www.natcm.gov.cn/a/tzgg/'
                new_url = url

                if num == 1:
                    new_url = url + "index.html"
                else:
                    new_url = url + f"index_{num}.html"

                if requests.head(
                    new_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                    },
                ).ok:
                    logging.debug(
                        "The new_url in start_request to NATCM_contentPage: {}".format(
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
        if bool(response.css(".box").xpath("//td/ul/li")):
            for quote in response.css(".box").xpath("//td/ul/li"):
                url = quote.css("li a::attr(href)").get()
                if ".html" not in url:
                    item["title"] = quote.css("li a::attr(title)").get()
                    item["article"] = quote.css("li a::attr(title)").get()
                    item["plaintext"] = quote.css("li a::attr(title)").get()
                    item["urlSource"] = url

                    today = date.today()
                    d1 = today.strftime("%Y-%m-%d")
                    item["scrapyDate"] = d1

                    tmpDate = quote.css("span::text").get()
                    item["publishingDate"] = re.search(r"\S+", tmpDate).group(0)
                    item["attachment"] = [
                        {"mark": quote.css("li a::attr(title)").get(), "link": url}
                    ]

                    item["source"] = "国家中医药管理局"
                    yield item
                else:
                    content_urls.append(
                        response.urljoin(quote.css("li a::attr(href)").get())
                    )

            for content_url in content_urls:
                for num in range(0, 25):
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

        title_origin = response.css(".nrbt::text").get()
        # delete "\n" and spaces in title
        title_new = title_origin.strip(" \n")
        item["title"] = re.sub(r"\s", "", title_new)

        date_origin = response.css(".fbsj::text").get()
        # change    "时间：2020-12-10 15:40:19"    to      "2020-12-10"
        item["publishingDate"] = re.search("(?<=：)\S*", date_origin).group(0)

        item["source"] = "国家中医药管理局"

        article = "".join(response.xpath("//td[@valign]/table[2]//td/span/p").getall())
        item["article"] = remove_tags(article, which_ones=("div"))

        item["plaintext"] = re.sub(r"\s(\s)+", " ", remove_tags(article))

        attachment = []
        ul = response.xpath("//td[@valign]/table[2]//td//a")
        if ul != []:
            for li in ul:
                mark = li.css("a::text").get()
                link = response.urljoin(li.css("a::attr(href)").get())
                attachment.append({"mark": mark, "link": link})
        item["attachment"] = attachment

        yield item
