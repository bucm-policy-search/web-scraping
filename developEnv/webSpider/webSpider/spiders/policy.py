import scrapy
import re
import sys
from webSpider.items import WebspiderItem
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

# sys.path.append('~/search-engine/web-scraping/developEnv/webSpider/webSpider/websites')
import BATCM


class PolicySpider(scrapy.Spider):
    name = 'policy'
    page_num = 2
    page_urls = []

    def start_requests(self):

        urls = [
            'http://zyj.beijing.gov.cn/sy/tzgg/',
        # ]
          'http://zyj.beijing.gov.cn/sy/zcfg/',
          'http://zyj.beijing.gov.cn/zcjd/wjjd/']

        for url in urls:
            # change url depending on pages
            for num in range(0, 11):
                # eg. default catch data from 'http://zyj.beijing.gov.cn/sy/tzgg'
                if num != 0:
                    # eg. catch data from 'http://zyj.beijing.gov.cn/sy/tzgg/index_1.html'
                    url = url + 'index_{num}.html'.format(num=num)
                yield scrapy.Request(url=url, callback=self.BATCM_contentPage)

    # 北京市中医药管理局（Beijing Administration of Traditional Chinese Medicine）
    def BATCM_contentPage(self, response):
        content_urls = []

        # Check whether data exist (also check whether this page exist)
        if bool(response.css("div.oursv_b_f li")):
            for quote in response.css("div.oursv_b_f li"):
                content_urls.append(response.urljoin(
                    quote.css('div a::attr(href)').get()))

            for content_url in content_urls:
                for num in range(0, 11):
                    if num == 0:
                        url = content_url
                    else:
                        url = content_url + 'index_{num}.html'.format(num=num)
                    yield scrapy.Request(url=content_url, callback=self.BATCM_detailPage)

        # page_urls = response.css('div.fanye')

    def BATCM_detailPage(self, response):
        urlsource = response.request.url
        title_origin = response.css('h4::text').get()
        # delete "\n" and spaces in title
        title = re.search('\S+(?=\\n)', title_origin).group(0)

        date_origin = response.css("div.zhengwen div::text").get()
        # change    "日期：2021-04-29  来源： "    to      "2021-04-29"
        date = re.search('(?<=：)\S*', date_origin).group(0)

        source = response.css('span.ly::text').get()
        article = response.css('div.view').get()
        plaintext = re.sub(r'\s\s', ' ', remove_tags(article))

        attachment = []
        ul = response.css('ul.tdbgimgdog li')
        for li in ul:
            mark = li.css('a::text').get()
            link = response.urljoin(li.css('a::attr(href)').get())
            attachment.append({
                "mark": mark,
                "link": link
            })

        yield {
            'urlsource': urlsource,
            'title': title,
            'date': date,
            'source': source,
            'article': article,
            'plaintext': plaintext,
            'attachment': attachment
        }
