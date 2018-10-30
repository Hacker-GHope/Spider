# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 15:16
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : qichamao.py
# @Software: PyCharm
import json

import requests
from lxml import etree


class Qichamao:
    def __init__(self):
        self.url = 'https://www.qichamao.com/cert-wall'
        self.headers = {
            'Referer': 'https://www.qichamao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'www.qichamao.com'
        }
        self.session = requests.Session()

    def parse_page(self, html):
        selector = etree.HTML(html)
        company_items = selector.xpath('//div[@class = "firmwall_list_box"]')
        company_list = []
        for company_item in company_items:
            company_dict = {}
            company_name = company_item.xpath('.//*[@class = "firmwall_list_tit toe"]/a/text()')
            company_dict['company_name'] = company_name
            company_list.append(company_dict)
        return company_list

    def get_page(self):
        response = self.session.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            return None

    def post_page(self, page, pagesize):
        data = {'page': page, 'pagesize': pagesize}
        response = self.session.post(self.url, headers=self.headers, data=data, )
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            return None

    def parse_result(self, json_text):
        result_json = json.loads(json_text)
        result_list = result_json['dataList']
        for data in result_list:
            print(data['CompanyName'])


def main():
    qichamao = Qichamao()
    html = qichamao.get_page()
    result = qichamao.parse_page(html)
    print('page:1')
    print('*' * 20)
    for item in result:
        print(str(item[0]['company_name']))
    for i in range(1, 100):
        print('page:%d' % (i + 1))
        print('*' * 20)
        json_text = qichamao.post_page(i + 1, 9)
        qichamao.parse_result(json_text)


if __name__ == '__main__':
    main()
