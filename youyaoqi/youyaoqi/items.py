# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YouyaoqiItem(scrapy.Item):
    # define the fields for your item here like:
    comic_id = scrapy.Field()
    name = scrapy.Field()
    cover = scrapy.Field()
    category = scrapy.Field()


