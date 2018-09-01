# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from nowcoder.items import NowcoderItem
from scrapy.loader import ItemLoader
from urllib import parse
from nowcoder.settings import user_agent_list

class NowSpider(scrapy.Spider):
    name = 'now'
    allowed_domains = ['www.nowcoder.com']
    start_urls = ['https://www.nowcoder.com/contestRoom']
    headers = {

    }
    custom_settings = {
        "COOKIES_ENABLED" : True
    }

    def parse(self, response):
        #构造随机的user-agent
        import random
        # random_index = random.randint(0, len(user_agent_list)-1)
        # random_agent = user_agent_list[random_index]
        # self.headers['User-Agent'] = random_agent
        domain = 'https://www.nowcoder.com'
        # yield Request(url=response.url, dont_filter=True, headers=self.headers, callback=self.parse_detail)
        yield Request(url=response.url, dont_filter=True, callback=self.parse_detail)
        next_url = response.css(".txt-pager.js-next-pager a::attr(href)").extract_first("")
        if next_url and next_url != 'javascript:void(0)':
            yield Request(url=parse.urljoin(domain, next_url), dont_filter=True, callback=self.parse)


    def parse_detail(self, response):
        title = response.css('div.content-item-brief h1::text').extract()
        for i in range(len(title)):
            title[i] = title[i].replace('\n', '')
        while '' in title:
            title.remove('')
        for i in range(len(title)):
            item_loader = ItemLoader(item=NowcoderItem(), response=response)
            item_loader.add_value("title", title[i])
            now_item = item_loader.load_item()
            print("插入第一批")
            yield now_item
