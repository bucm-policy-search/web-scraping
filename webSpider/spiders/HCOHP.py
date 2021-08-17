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

    page_urls = []

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
                if ".html" not in url:
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

                    # 应对微信公众号外链
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
        item["article"] = article

        item["plaintext"] = re.sub(r"\s(\s)+", " ", remove_tags(article))

        attachment = []
        ul = response.css(".fjlist li")
        if ul != []:

            # 用了XHR隐藏附件URL，特殊对待一下
            cid = re.search(r"(?<=\/)[0-9]*(?=\.)", response.url).group(0)

            # 以下内容是从Chrome复制成cURL bash形式，再用Postman转换成python requests形式得到
            url = f"http://wsjkw.hebei.gov.cn/attachment_url.jspx?cid={cid}&n={len(ul)}"
            payload = {}
            headers = {
                "Proxy-Connection": "keep-alive",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "DNT": "1",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
                "Referer": response.url,
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            }

            res = requests.request("GET", url, headers=headers, data=payload)

            appendUrlList = res.json()

            print(response.text)

            for index, li in enumerate(ul):
                mark = li.css("a::text").get()
                attachment.append({"mark": mark, "link": url + appendUrlList[index]})

            item["attachment"] = attachment

            yield item
