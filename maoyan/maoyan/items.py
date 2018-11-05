# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    actor = scrapy.Field()
    release_time = scrapy.Field()
    score = scrapy.Field()