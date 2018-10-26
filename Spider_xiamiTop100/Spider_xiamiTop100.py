# -*- coding: utf-8 -*-
# @Time    : 2018/10/26 11:12
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : Spider_xiamiTop100.py
# @Software: PyCharm
import json
import random
import time
import requests
from lxml import etree
from selenium import webdriver
from kaisa import dataMp3

# 无头浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# 启动浏览器
browser = webdriver.Chrome(chrome_options=chrome_options)


def get_html(url):
    browser.get(url)
    # 网速不好的时候使用延长加载时间
    # # 随机等待时间
    # t = random.randint(0, 9)
    # # 分六次滚动页面
    # for i in range(6):
    #     str_js = 'var step = document.body.scrollHeight/6;window.scrollTo(0,step*%d)' % (i + 1)
    #     browser.execute_script(str_js)
    #     time.sleep(t)
    page_source = browser.page_source
    return page_source


def download(name, path):
    items = []
    for i in range(len(name)):
        item = {}
        # item_name = name[i]
        # item_path = dataMp3(path[i])
        item['name'] = name[i]
        real_path = dataMp3(path[i])
        item['path'] = real_path
        items.append(item)
        # 将下载到本地的代码
        # filename = "./download/%s.mp3" % item_name
        # r = requests.get(item_path)
        # with open(filename, "wb") as f:
        #     f.write(r.content)
        # 网速不好逐条添加
        # music_json = json.dumps(item, ensure_ascii=False, check_circular=True)
        # filename = './虾米Top100'
        # with open(filename, "a", encoding='utf-8') as f:
        #     f.write(music_json)
    music_json = json.dumps(items, ensure_ascii=False, check_circular=True)
    filename = './虾米Top100'
    with open(filename, "w", encoding='utf-8') as f:
        f.write(music_json)


def parse_html(page_source):
    # print(page_source)
    etree_html = etree.HTML(page_source)
    name = etree_html.xpath('//div[@id="chart"]/table/tr/@data-title')
    # print(name)
    path = etree_html.xpath('//div[@id="chart"]/table/tr/@data-mp3')
    # print(path)
    download(name, path)


def main():
    url = 'https://www.xiami.com/chart'
    page_source = get_html(url)
    parse_html(page_source)


if __name__ == '__main__':
    main()
