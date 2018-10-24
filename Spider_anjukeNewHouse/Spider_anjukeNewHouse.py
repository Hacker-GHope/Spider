# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 15:41
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : Spider_anjukeNewHouse.py
# @Software: PyCharm
import json

import requests
from bs4 import BeautifulSoup


# 获取页面
def get_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


# 解析页面
def parse_soup(html):
    # 创建soup对象
    soup = BeautifulSoup(html,'lxml')
    # 解析小区名称
    result = soup.select('.items-name')
    house_name = result
    # 解析具体位置
    result = soup.select('.list-map')
    house_local = result
    # 解析出售价格
    # 因为网页上有很多暂未开盘的房市及未定价的房屋，所以暂且搁置
    # result = soup.select('.price' or '.around-price')
    # house_price = result
    # print(result)

    house = []
    for i in range(len(house_name)):
        item = {}
        item['name'] = house_name[i].text
        item['local'] = house_local[i].text.replace('\xa0','')
        # item['price'] = house_price[i].text
        house.append(item)
    return house


# 保存本地json数据
def write_json(items):
    house_json = json.dumps(items, ensure_ascii=False, check_circular=True)
    filename = './安居客攀枝花新楼'
    with open(filename, "a", encoding='utf-8') as f:
        f.write(house_json)



# 主程序
def main():
    urls = ['https://pzh.fang.anjuke.com/?from=navigation', 'https://pzh.fang.anjuke.com/loupan/all/p2/']
    for url in urls:
        html = get_page(url)
        items = parse_soup(html)
        write_json(items)


if __name__ == '__main__':
    main()
