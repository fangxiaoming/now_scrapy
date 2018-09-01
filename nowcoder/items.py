# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NowcoderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into nowcoder(title)
            VALUES (%s) ON DUPLICATE KEY UPDATE title=VALUES(title)
        """
        params = (self["title"])
        return insert_sql, params