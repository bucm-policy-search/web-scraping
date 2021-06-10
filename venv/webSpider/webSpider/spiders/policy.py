import scrapy
import sys, os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# sys.path.append(os.path.join(sys.path[0],'websites'))
from webSpider.spiders.websites.BATCM import BATCM

process = CrawlerProcess(get_project_settings())
process.crawl(BATCM)
process.start() # the script will block here until all crawling jobs are finished