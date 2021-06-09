# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy.loader.processors import MapCompose, TakeFirst
# from w3lib.html import remove_tags

# def remove_whitesapce(value):
#     return value.strip()


class ElasticSearchItem(scrapy.Item):
    urlsource = scrapy.Field()
    scrapyDate = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    source = scrapy.Field()
    article = scrapy.Field()
    plaintext = scrapy.Field()
    attachment = scrapy.Field()
