# -*- coding: utf-8 -*-
import scrapy
import json
from youyaoqi.items import YouyaoqiItem


class YaoqiSpider(scrapy.Spider):
    name = 'yaoqi'
    allowed_domains = ['u17.com']
    start_urls = ['http://www.u17.com/comic_list/th99_gr99_ca99_ss99_ob0_ac0_as0_wm0_co99_ct99_p1.html?order=2']

    def get_headers(self):
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept': 'application/json, text/plain, */*',
            'Host': 'www.u17.com',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        return headers

    def start_requests(self):
        data = {
            'data[group_id]': 'no',
            'data[theme_id]': 'no',
            'data[is_vip]': 'no',
            'data[accredit]': 'no',
            'data[color]': 'no',
            'data[comic_type]': 'no',
            'data[series_status]': 'no',
            'data[order]': '2',
            'data[page_num]': '1',
            'data[read_mode]': 'no'
        }

        url = 'http://www.u17.com/comic/ajax.php?mod=comic_list&act=comic_list_new_fun&a=get_comic_list'



        for page in range(500):
            data['data[page_num]'] = '%s' % (page + 1)
            yield scrapy.FormRequest(url=url,
                                     headers=self.get_headers(),
                                     method='POST',
                                     formdata=data,
                                     callback=self.parse)



    def parse(self, response):
        json_result = json.loads(response.text)
        comic_list = json_result['comic_list']
        for comic in comic_list:
            item = YouyaoqiItem()
            item['comic_id'] = comic['comic_id']
            item['name'] = comic['name']
            item['cover'] = comic['cover']
            item['category'] = comic['line2']
            yield item
