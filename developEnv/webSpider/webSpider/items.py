# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy.loader.processors import MapCompose, TakeFirst
# from w3lib.html import remove_tags


# def remove_whitesapce(value):
#     return value.strip()


class WebspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    # policy_text = scrapy.Field(
    #     input_process=MapCompose(remove_tags, remove_whitesapce),
    #     output_process = TakeFirst()
    # )
