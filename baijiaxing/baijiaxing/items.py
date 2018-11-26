# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Names(scrapy.Item):
    surname = scrapy.Field()
    name = scrapy.Field()


class NamesDetails(scrapy.Item):
    name = scrapy.Field()
    # 藏头诗
    acrostic_poetry = scrapy.Field()
    # 五行
    five_elements = scrapy.Field()
    # 三才
    npf = scrapy.Field()
    # 五格
    five = scrapy.Field()
    # 五格剖象法分析
    five_profile_analysis = scrapy.Field()
    # 男性使用概率
    boy_probability = scrapy.Field()
    # 女性使用概率
    girl_probability = scrapy.Field()


class BaijiaxingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    surname = scrapy.Field()
