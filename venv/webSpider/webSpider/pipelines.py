# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from time import strftime
import logging
import os

logging.basicConfig(filename='./logs/scrapy_pipelines_{}.log'.format(strftime("%Y/%m/%d-%H:%M:%S_UTC%z")), encoding='utf-8', level=logging.DEBUG)

class ElasticSearchPipeline:
    def open_spider(self, spider):
        load_dotenv()
        logging.debug('print config value: %s', os.environ)

        username = os.environ['USERNAME']
        PASSWORD = os.environ['PASSWORD']
        URL = os.environ['URL']
        es = Elasticsearch(
            ['http://{}:{}@{}/'.format(username, PASSWORD, URL)]
        )

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        logging.debug('Processing items in pipelines: {}'.format(item))
        return item
