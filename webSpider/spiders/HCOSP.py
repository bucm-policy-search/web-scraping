#author @hyl
import scrapy
from webSpider.items import ElasticSearchItem
import re
from lxml import etree
import requests
from datetime import date
from time import strftime
import logging
from w3lib.html import remove_tags
from scrapy.utils.log import configure_logging
class QuoteSpider(scrapy.Spider):
    name="HCOSP"
    allowed_domains=["wjw.shanxi.gov.cn"]

    def __init__(self):
        #loggingRoot = False if (hasattr(self, "mode")) else True
        #configure_logging(install_root_handler=loggingRoot)
        current_time = strftime("%Y-%m-%dT%H:%M:%S%z")
        logging.basicConfig(
            format='%(asctime)s %(filename)s %(levelname)s %(message)s',
            filename=f"./logs/scrapy_{current_time}.log", 
            level=logging.WARNING,
        )# ISO 8601 Timestamp format
    
    def start_requests(self):
        
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52"}
        url="http://wjw.shanxi.gov.cn/zyygljl01/index.hrh"
        res=requests.get(url=url,headers=headers)
        tree=etree.HTML(res.text)
        page=tree.xpath("//div[@class='fenye']/div/text()")[0]
        page=re.search(r"(/\d{1,2})",page).group(0)[1:3]
        
        for i in range(1,int(page)+1):
            url="http://wjw.shanxi.gov.cn/zyygljl01/index_{}.hrh".format(i)
            logging.warning("start to get----{}".format(url))
            yield scrapy.Request(url=url,callback=self.parse)
    
    def parse(self, response):
        url_list=response.xpath("//div[@class='demo-right']/ul/li")
        for i in url_list:
            url_article=i.xpath("./a/@href").extract_first()
            if url_article!=None:
                yield scrapy.Request(url=url_article,callback=self.content_url)
                
    def content_url(self,response):
        item=ElasticSearchItem()
        try:
            publishingDate=response.xpath("//div[@class='artxx']/text()").extract_first()
            
            item["publishingDate"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",publishingDate).group(0)

            item['urlSource']=response.url

            article=response.css("div.ze-art").get()
            item["article"] = article
            plaintext=re.sub(r"\s(\s)+", " ", remove_tags(article))
            item["plaintext"] = plaintext

            title=response.xpath("//h3/text()").extract_first()
            item['title']=title
            
            item["source"] = "山西省卫生健康委员会"

            today = date.today()
            d1 = today.strftime("%Y-%m-%d")
            item["scrapyDate"] = d1

            attachment = []
            attachment_list_a = response.xpath("//div[@class='ze-art']/p/a")
            if attachment_list_a!=None:
                for i in attachment_list_a:
                    response.urljoin
                    mark=i.xpath("./text()").extract_first()
                    link=response.urljoin(i.xpath("./@href"))
                    attachment.append({"mark": mark, "link": link})
                item["attachment"] = attachment
            logging.warning("scrapy url----{}".format(response.url))
            yield item
        except:
             logging.error("Erro url----{}".format(response.url)) 
        
            
        
        
        