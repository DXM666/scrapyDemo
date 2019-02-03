# -- coding: UTF-8 -- 
import scrapy
from scrapy.linkextractors import LinkExtractor ##配合Rule进行URL规则匹配
from scrapyDemo.items import ScrapydemoItem,ScrapyProxyItem
from scrapy.loader import ItemLoader
from pyquery import PyQuery
from scrapy.spiders import CrawlSpider,Rule,Request,XMLFeedSpider,CSVFeedSpider,Spider
import random
import re
import codecs
import json
from scrapy import FormRequest ##Scrapy中用作登录使用的一个包


# class MySpider(scrapy.Spider):
#
#     name = 'scrapyDemo'
#     start_urls = "https://www.jianshu.com/"
#
#     def start_requests(self):
#         yield Request(url=self.start_urls)
#
#     def parse(self,response):
#         doc = PyQuery(response.body,parser='html')
#         hreflist = doc('.note-list').children().items()
#         for href in hreflist:
#             url_path = href('.title').attr('href')
#             url = response.urljoin(url_path)
#             yield Request(url,callback=self.parse_dir_contents)
#
#     def parse_dir_contents(self, response):
#         item = ScrapydemoItem()
#         abstractList = []
#         item['title'] = response.xpath('//h1[@class="title"]//text()').extract()[0]
#         for i in response.xpath('//div[@class="show-content-free"]//text()').extract():
#             abstractList.append(i)
#         item['abstract'] = ''.join(abstractList).replace('\n','')
#         item['author'] = response.xpath('//span[@class="name"]//text()').extract()[0]
#         # with codecs.open('jianshu.json', 'w') as f:
#         #     f.write(json.dumps(dict(item),ensure_ascii=False))
#         print(item)
#         yield item

# class MyCrawlSpider(CrawlSpider):
#     name = 'scrapyDemo'
#     start_urls = ["https://www.jianshu.com/"]
#
#     rules = (
#         Rule(LinkExtractor(allow=('p/',)),callback='parse_item',follow=True,),
#     )
#
#     def parse_item(self, response):
#         print(response.url)
#         pass

class MyXMLFeedSpider(XMLFeedSpider):
    name = 'scrapyDemo'
    start_urls = ["https://www.jianshu.com/"]
    iterator = 'iternodes'
    itertag = 'body'


    # def start_requests(self):
    #     f = open('proxy.json','r')
    #     res = json.load(f)
    #     proxy = random.choice(res)
    #     print(proxy)
    #     yield Request(url=self.start_urls,meta={'proxy':'http://61.135.217.7:80'})

    def adapt_response(self, response):
        print('-'*10+'analysis response'+'-'*10)
        return response

    def parse_node(self, response, selector):
        item = ScrapydemoItem()
        item['title'] = selector.xpath("//ul[@class='note-list']/li/div/a/text()").extract()
        item['author'] = selector.xpath("//ul[@class='note-list']/li/div/div/a[@class='nickname']/text()").extract()
        return item

    def get_content(self,response):
        print('come here ------------------')
        l = ItemLoader(item = ScrapydemoItem(),response = response)
        # item = ScrapydemoItem()
        abstractList = []
        for i in response.xpath('//div[@class="show-content-free"]//text()').extract():
            abstractList.append(i)
        l.add_value('num',response.meta['num'])
        l.add_value('title',response.meta['title'])
        l.add_value('author',response.meta['author'])
        l.add_value('abstract',''.join(abstractList).replace('\n', ''))
        # item['num'] = response.meta['num']
        # item['title'] = response.meta['title']
        # item['author'] = response.meta['author']
        # item['abstract'] = ''.join(abstractList).replace('\n', '')
        yield l.load_item()

    def process_results(self, response, results):
        urllist = response.xpath("//ul[@class='note-list']/li/div/a/@href").extract()
        for url_path in urllist:
            item = {}
            item['num'] = str(urllist.index(url_path) + 1)
            item['title'] = results[0]['title'][urllist.index(url_path)]
            item['author'] = results[0]['author'][urllist.index(url_path)]
            url = response.urljoin(url_path)
            yield Request(url=url, callback=self.get_content,meta=item)


# class MyCSVFeedSpider(CSVFeedSpider):
#     name = 'scrapyDemo'
#     start_urls = ["http://yum.iqianyue.com/weisuenbook/pyspd/part12/mydata.csv"]
#     headers = ['name','sex','addr','email']
#     delimiter = ','
#
#     def parse_row(self, response, row):
#         item = ScrapydemoItem()
#         item['name'] = row['name'].encode('utf8')
#         item['author'] = row['sex'].encode()
#         print("名字是：")
#         print(item['name'])
#         print("性别是：")
#         print(item['author'])
#         print("-------------------------------")

# class MyProxySpider(Spider):
#     name = 'scrapyDemo'
#     start_urls = ["https://www.xicidaili.com/wn/"]
#
#     def parse(self, response):
#         item = ScrapyProxyItem()
#         item['path'] = response.xpath('//table[@id="ip_list"]//tr[@class="odd"]//td[2]//text()').extract()
#         item['port'] = response.xpath('//table[@id="ip_list"]//tr[@class="odd"]//td[3]//text()').extract()
#         item['proxies'] = []
#         for i in range(len(item['path'])):
#             item['proxies'].append("https://" + (item['path'][i] + ":" + item['port'][i]))
#             with open('proxy.json','w') as f:
#                 f.write(json.dumps(item['proxies'],ensure_ascii=False))
#             yield item