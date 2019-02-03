# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-
import json
import codecs

class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('douban.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):

        self.file.write(json.dumps(dict(item), ensure_ascii=False)+',')
        return item

    def spider_closed(self, spider):
        self.file.close()
