# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 14:04
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : manyan.py
# @Software: PyCharm
import json
import requests
import re


def get_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    # 名称参数赋值，位置参数会报错
    # response = requests.get(url,headers)
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None


def pares_page(html):
    # 排行
    pattern = re.compile('<i class="board-index board-index-.*?">(.*?)</i>')
    item_rank = re.findall(pattern, html)
    # 电影
    pattern = re.compile('movieId.*?>.*?<img.*?<img.*?alt="(.*?)" class.*?', re.S)
    item_film = re.findall(pattern, html)
    # 海报
    # pattern = re.compile('<dd>.*?<img.*?<img.*?src="(.*?)"', re.S)
    # 主演
    pattern = re.compile('<p class="star">(.*?)</p>',re.S)
    item_star = re.findall(pattern, html)
    # 上映时间
    pattern = re.compile('<p class="releasetime">(.*?)</p>',re.S)
    item_time = re.findall(pattern, html)
    items = []
    for i in range(len(item_film)):
        film = {}
        film['rank'] = item_rank[i]
        film['film'] = item_film[i]
        film['star'] = item_star[i].strip()
        film['time'] = item_time[i]
        items.append(film)

    return items


def write_image(items):
    """
    根据图片地址下载图片到指定目录
    """
    url_parts = items.split("@")
    url_result = url_parts[0]
    filename = "./upload/%s" % url_result.split("/")[-1]
    r = requests.get(items)
    with open(filename, "wb") as f:
        f.write(r.content)


def write_json(items):
    movie_json = json.dumps(items, ensure_ascii=False, check_circular=True)
    filename = './猫眼top100'
    with open(filename,"a",encoding='utf-8') as f:
        f.write(movie_json)

def main():
    for i in range(0, 10):
        page = str(i * 10)
        url = 'http://maoyan.com/board/4?offset=' + page
        print(url)
        html = get_page(url)
        items = pares_page(html)
        # print(html)
        # 列表生成式[]
        # print([item.strip() for item in items])
        # 循环遍历爬取结果
        # for item in items:
        #     write_image(item)
        write_json(items)


if __name__ == '__main__':
    main()
