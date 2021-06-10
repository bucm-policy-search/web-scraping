import scrapy
import re
import sys
import requests
import logging
from webSpider.items import ElasticSearchItem
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from datetime import date


class PolicySpider(scrapy.Spider):
    name = 'policy'

    def __init__(self, *args, **kwargs):
        super(PolicySpider, self).__init__(*args, **kwargs)

    page_num = 2
    page_urls = []

    def start_requests(self):
        item = ElasticSearchItem()
        urls = [
            'http://zyj.beijing.gov.cn/sy/tzgg/',
        ]
        # 'http://zyj.beijing.gov.cn/sy/zcfg/',
        # 'http://zyj.beijing.gov.cn/zcjd/wjjd/']

        for url in urls:
            # change url depending on pages
            for num in range(0, 1000):
                # eg. default catch data from 'http://zyj.beijing.gov.cn/sy/tzgg'
                new_url = url
                if num != 0:
                    # eg. catch data from 'http://zyj.beijing.gov.cn/sy/tzgg/index_1.html'
                    new_url = url + 'index_{num}.html'.format(num=num)

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
                }
                if requests.head(new_url, headers=headers).ok:
                    logging.debug(
                        'The new_url in start_request to BATCM_contentPage: {}'.format(new_url))

                    yield scrapy.Request(url=new_url, callback=self.BATCM_contentPage, meta={'item': item})
                else:
                    break

    # 北京市中医药管理局（Beijing Administration of Traditional Chinese Medicine）
    def BATCM_contentPage(self, response):
        content_urls = []
        item = response.meta['item']
        # Check whether data exist (also check whether this page exist)
        if bool(response.css("div.oursv_b_f li")):
            for quote in response.css("div.oursv_b_f li"):
                content_urls.append(response.urljoin(
                    quote.css('div a::attr(href)').get()))

            for content_url in content_urls:
                for num in range(0, 20):
                    url = ''
                    if num == 0:
                        url = content_url
                    else:
                        url = content_url + 'index_{num}.html'.format(num=num)
                    yield scrapy.Request(url=content_url, callback=self.BATCM_detailPage, meta={'item': item})

    def BATCM_detailPage(self, response):
        # self.logger.info('Hi, this is an item page! %s', response.url)
        item = response.meta['item']

        item['urlsource'] = response.url
        
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        item['scrapyDate'] = d1

        title_origin = response.css('h4::text').get()
        # delete "\n" and spaces in title
        item['title'] = re.search('\S+(?=\\n)', title_origin).group(0)

        date_origin = response.css("div.zhengwen div::text").get()
        # change    "日期：2021-04-29  来源： "    to      "2021-04-29"
        item['date'] = re.search('(?<=：)\S*', date_origin).group(0)

        item['source'] = response.css('span.ly::text').get()

        if(response.css('div.view').get() != None):
            article = response.css('div.view').get()
        else:
            article = response.css('div.TRS_Editor').get()
            
        item['article'] = article

        item['plaintext'] = re.sub(r'\s(\s)+', ' ', remove_tags(article))

        attachment = []
        ul = response.css('ul.tdbgimgdog li')
        for li in ul:
            mark = li.css('a::text').get()
            link = response.urljoin(li.css('a::attr(href)').get())
            attachment.append({
                "mark": mark,
                "link": link
            })
        item['attachment'] = attachment

        yield item
