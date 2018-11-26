# -*- coding: utf-8 -*-
import scrapy
from baijiaxing.items import BaijiaxingItem, Names, NamesDetails
from urllib.request import unquote


class XingSpider(scrapy.Spider):
    name = 'xing'
    allowed_domains = ['resgain.net']
    start_urls = ['http://www.resgain.net/xmdq.html']

    def get_headers(self):
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        return headers

    def start_requests(self):
        yield scrapy.Request(url='http://www.resgain.net/xmdq.html',
                             headers=self.get_headers(),
                             method='GET',
                             callback=self.parse,
                             )

    def parse(self, response):
        surnames = response.xpath('/html/body/div[3]/div/div/div[2]/a')
        for surname in surnames:
            surname_item = BaijiaxingItem()
            surname_item['surname'] = surname.xpath('./text()').extract_first()
            # yield surname_item

            url_name_next = 'http:' + str(surname.xpath('./@href').extract_first())
            yield scrapy.Request(url=url_name_next, headers=self.get_headers(),
                                 callback=lambda response, url_name_next=url_name_next: self.parse_name(response,
                                                                                                        url_name_next))
        # surname_item = BaijiaxingItem()
        # yield surname_item

    def parse_name(self, response, url_name_next):
        names = response.xpath('/html/body/div[3]/div[2]/div[1]/div/a')
        for name in names:
            name_item = Names()
            name_item['surname'] = name.xpath('./text()').extract_first()[0]
            name_item['name'] = name.xpath('./text()').extract_first()
            yield name_item

            url_name = url_name_next.split('//')[1].split('/')[0]
            # s = name.xpath('./@href').extract_first().decode('utf8')
            url_next = 'http:' + url_name + unquote(str(name.xpath('./@href').extract_first()))
            yield scrapy.Request(url=url_next,
                                 headers=self.get_headers(),
                                 callback=lambda response, name=name: self.parse_name_details(response, name))
        for i in range(2, 11):
            url_page = url_name_next.split('.html')[0] + '_%d' % i + '.html'
            yield scrapy.Request(url=url_page,
                                 headers=self.get_headers(),
                                 callback=lambda response, url_page=url_page: self.parse_page_name(response, url_page),
                                 )

    def parse_page_name(self, response, url_page):
        names = response.xpath('/html/body/div[3]/div[2]/div[1]/div/a')
        for name in names:
            name_item = Names()
            name_item['surname'] = name.xpath('./text()').extract_first()[0]
            name_item['name'] = name.xpath('./text()').extract_first()
            yield name_item

            url_name = url_page.split('/')[0]
            # s = name.xpath('./@href').extract_first().decode('utf8')
            url_next = 'http:' + url_name + unquote(str(name.xpath('./@href').extract_first()))
            name = name_item['name']
            yield scrapy.Request(url=url_next, headers=self.get_headers(),
                                 callback=lambda response, name=name: self.parse_name_details(response, name))

    def parse_name_details(self, response, name):
        # pass
        name_details = NamesDetails()
        name_details['name'] = name
        name_details['acrostic_poetry'] = response.xpath('/html/body/div[2]/div/div[4]/div[1]/div[2]/h4').extract()
        name_details['five_elements'] = response.xpath('/html/body/div[2]/div/div[4]/div[2]/div/div[2]/div[1]/blockquote/text()').extract_first()
        name_details['npf'] = response.xpath('/html/body/div[2]/div/div[4]/div[2]/div/div[2]/div[2]/blockquote/text()').extract_first()
        name_details['five'] = response.xpath('')
        yield name_details
