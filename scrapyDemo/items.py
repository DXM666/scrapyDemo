# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
import scrapy


class ScrapydemoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    num = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    author = scrapy.Field()
    abstract = scrapy.Field()
    serialStatus = scrapy.Field()
    serialNumber = scrapy.Field()
    category = scrapy.Field()
    nameID = scrapy.Field()

class ScrapyProxyItem(Item):
    path = scrapy.Field()
    port = scrapy.Field()
    proxies = scrapy.Field()

