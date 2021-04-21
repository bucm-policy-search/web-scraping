import scrapy
import re


class PolicySpider(scrapy.Spider):
    name = 'policy'
    page_num = 2
    page_urls = []

    def start_requests(self):

        urls = [
            'http://zyj.beijing.gov.cn/sy/tzgg/',
        ]
        #   'http://zyj.beijing.gov.cn/sy/zcfg/',
        #   'http://zyj.beijing.gov.cn/zcjd/wjjd/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.contentPage)

    def contentPage(self, response):
        content_urls = []
        for quote in response.css("div.oursv_b_f li"):
            content_urls.append(response.urljoin(
                quote.css('div a::attr(href)').get()))

        for content_url in content_urls:
            yield scrapy.Request(url=content_url, callback=self.detailPage)

        page_urls = response.css('div.fanye')

    def detailPage(self, response):
        urlsource = response.request.url
        title_origin = response.css('h4::text').get()
        title = re.search('\S+(?=\\n)', title_origin).group(0)

        date_origin = response.css("div.zhengwen div::text").get()
        date = re.search('(?<=：)\S*', date_origin).group(0)

        source = response.css('span.ly::text').get()
        article = response.css('div.trs_word').get()

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
            'attachment': attachment
        }
