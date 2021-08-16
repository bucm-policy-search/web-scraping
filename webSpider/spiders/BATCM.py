import scrapy
import re
import sys
import requests
import logging
from scrapy.utils.log import configure_logging
from time import strftime
from webSpider.items import ElasticSearchItem
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from datetime import date
import random
from faker import Faker

"""
Debug
--------------------------------------------------------
Unhandled Runtime Error
TypeError: Cannot read property '_source' of undefined
--------------------------------------------------------

 |   <div className="mt-8 mx-12 mb-16 text-lg" key={value._source.title}>
> 72 |     <h1 className="font-bold text-3xl">{value._source.title}</h1>
     |                                              ^
  73 |     <p className="text-lg mt-10">
  74 |       原文地址：
  75 |       <a className="underline" href={value._source.urlSource}>
"""


class BATCM(scrapy.Spider):

    # 北京市中医药管理局（Beijing Administration of Traditional Chinese Medicine）
    name = "BATCM"

    def __init__(self, mode):
        loggingRoot = False if (hasattr(self, "mode")) else True
        configure_logging(install_root_handler=loggingRoot)

        current_time = strftime("%Y-%m-%dT%H:%M:%S%z")
        logging.basicConfig(
            format="%(asctime)s %(levelname)s:%(message)s",
            filename=f"./logs/scrapy_{current_time}.log",
            level=logging.WARNING,
        )  # ISO 8601 Timestamp format

    def start_requests(self):
        item = ElasticSearchItem()

        urls = {
            True: [
                "http://zyj.beijing.gov.cn/sy/tzgg/",
                "http://zyj.beijing.gov.cn/sy/zcfg/",
                "http://zyj.beijing.gov.cn/zcjd/wjjd/",
            ],
            False: ["http://zyj.beijing.gov.cn/sy/tzgg/"],
        }[hasattr(self, "mode") and self.mode == "prod"]

        for url in urls:
            # change url depending on pages
            for num in (
                range(0, 1000)
                if (hasattr(self, "mode") and self["mode"] == "prod")
                else range(0, 2)
            ):
                # eg. default fetch data from 'http://zyj.beijing.gov.cn/sy/tzgg'
                new_url = url
                if num != 0:
                    # eg. fetch data from 'http://zyj.beijing.gov.cn/sy/tzgg/index_1.html'
                    new_url = url + "index_{num}.html".format(num=num)

                if requests.head(
                    new_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                    },
                ).ok:
                    logging.debug(
                        "The new_url in start_request to BATCM_contentPage: {}".format(
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
        if bool(response.css("div.oursv_b_f li")):
            for quote in response.css("div.oursv_b_f li"):
                url = response.urljoin(quote.css("div a::attr(href)").get())
                if ".html" not in url:
                    item["title"] = quote.css("div a::attr(title)").get()
                    item["article"] = quote.css("div a::attr(title)").get()
                    item["plaintext"] = quote.css("div a::attr(title)").get()
                    item["urlSource"] = url

                    today = date.today()
                    d1 = today.strftime("%Y-%m-%d")
                    item["scrapyDate"] = d1

                    tmpDate = quote.css("span::text").get()
                    item["publishingDate"] = re.search("\S+", tmpDate).group(0)
                    item["attachment"] = [
                        {"mark": quote.css("div a::attr(title)").get(), "link": url}
                    ]

                    item["source"] = "北京市中医管理局"
                    yield item
                else:
                    content_urls.append(
                        response.urljoin(quote.css("div a::attr(href)").get())
                    )

            for content_url in content_urls:
                for num in range(0, 20):
                    url = {
                        True: content_url,
                        False: content_url + "index_{num}.html".format(num=num),
                    }[num == 0]
                    yield scrapy.Request(
                        url=content_url, callback=self.detailPage, meta={"item": item}
                    )

    def detailPage(self, response):
        item = response.meta["item"]

        item["urlSource"] = response.url

        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        item["scrapyDate"] = d1

        title_origin = response.css("h4::text").get()

        # delete "\n" and spaces in title
        title_new = title_origin.strip(" \n")
        item["title"] = re.sub(r"\s", "", title_new)

        date_origin = response.css("div.zhengwen div::text").get()

        # change "日期：2021-04-29  来源： " to "2021-04-29"
        item["publishingDate"] = re.search("(?<=：)\S*", date_origin).group(0)

        item["source"] = str(response.css("span.ly::text").get()).strip(" ")

        article = {
            True: response.css("div.view").get(),
            False: response.css("div.TRS_PreAppend").get(),
        }[response.css("div.view").get() is not None]
        item["article"] = article

        item["plaintext"] = re.sub(r"\s(\s)+", " ", remove_tags(article))

        attachment = []
        ul = response.css("ul.tdbgimgdog li")
        if ul != []:
            for li in ul:
                mark = li.css("a::text").get()
                link = response.urljoin(li.css("a::attr(href)").get())
                attachment.append({"mark": mark, "link": link})
        item["attachment"] = attachment

        yield item
