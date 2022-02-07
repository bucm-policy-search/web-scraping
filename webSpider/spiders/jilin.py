import logging
import scrapy
from webSpider.items import ElasticSearchItem
import re
from datetime import date
from w3lib.html import remove_tags


class JLTCM(scrapy.Spider):
    name = "JLTCM"
    # 吉林省中医药管理局
    allowed_domains = ["jltcm.jl.gov.cn"]

    def __init__(self, mode=None):
        self.mode = mode

    def start_requests(self):
        urls = {
            True: [
                "http://jltcm.jl.gov.cn/tzgg/xgdt/",
                "http://jltcm.jl.gov.cn/tzgg/gsgg/",
                "http://jltcm.jl.gov.cn/zwgk/zcjd/",
            ],
            False: ["http://jltcm.jl.gov.cn/tzgg/xgdt/"],
        }[hasattr(self, "mode") and self.mode == "prod"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url_list = response.xpath(
            "//html/body/div[4]/div[3]/ul/li/a/@href").extract()
        logging.warning(url_list)
        for i in url_list:
            url = response.urljoin(str(i))
            yield scrapy.Request(url=url, callback=self.details)
        for i in range(1, 50):
            url = "http://jltcm.jl.gov.cn/tzgg/xgdt/index_{}.html".format(
                i)
            yield scrapy.Request(url=url, callback=self.parse)

    def details(self, response):
        item = ElasticSearchItem()
        response.body.decode("utf-8")
        publishingDate = re.findall(
            "(\d{4}/\d{1,2}/\d{1,2})", response.xpath("//h2/text()").extract_first())[0]
        article = response.xpath("//div[@class='cont_tx']//text()").extract()
        plaintext = re.sub(r"\s(\s)+", " ", remove_tags(str(article)))
        title = response.xpath("//h1/text()").extract_first()
        scrapy_date = date.today().strftime("%Y-%m-%d")
        attachment = ""

        item["publishingDate"] = publishingDate
        item["article"] = remove_tags(article, which_ones=("div"))
        item["plaintext"] = plaintext
        item["title"] = title
        item["urlSource"] = response.url
        item["source"] = "吉林省中医药管理局"
        item["scrapyDate"] = scrapy_date
        item["attachment"] = attachment

        yield item
