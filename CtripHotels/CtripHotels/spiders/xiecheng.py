# -*- coding: utf-8 -*-
import scrapy
from CtripHotels.items import CtriphotelsItem


class XiechengSpider(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://hotels.ctrip.com/hotel/chengdu28#ctm_ref=hod_hp_sb_lst']



    def parse(self, response):
       results = response.xpath('//div[@id="hotel_list"]//ul[@class="hotel_item"]')
       for result in results:
           hotel = CtriphotelsItem()
           hotel['hotel_name'] = result.xpath('.//h2[@class="hotel_name"]/a/@title').extract_first()
           yield hotel

