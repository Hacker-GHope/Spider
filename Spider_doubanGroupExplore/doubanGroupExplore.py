# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 10:01
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : doubanGroupExplore.py
# @Software: PyCharm
import json
import requests

from lxml import etree


# 获取页面
def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


# 解析页面练习
def parse_with_xpath(html):
    etree_html = etree.HTML(html)
    # print(etree_html)

    # 匹配所有节点 //*
    # result = etree_html.xpath('//*')
    # print(result)
    # print(len(result))

    # 匹配所有子节点 //a     文本获取：text()
    # result = etree_html.xpath('//a/text()')
    # print(result)

    # 查找元素子节点 /
    # result = etree_html.xpath('//div/p/text()')
    # print(result)

    # 查找元素所有子孙节点 //
    # result = etree_html.xpath('//div[@class="channel-item"]//h3/a/text()')
    # print(result)

    # 父节点 ..
    # result = etree_html.xpath('//span[@class="pubtime"]/../span/a/text()')
    # print(result)

    # 属性匹配 [@class="xxx"]
    # 文本匹配 text() 获取所有文本//text()
    # result = etree_html.xpath('//div[@class="article"]//text()')
    # print(result)

    # 属性获取 @href
    # result = etree_html.xpath('//div[@class="bd"]/h3/a/@href')
    # print(result)

    # 属性多值匹配 contains(@class 'xx')
    # result = etree_html.xpath('//div[contains(@class, "grid-16-8")]//div[@class="likes"]/text()[1]')
    # print(result)

    # 多属性匹配 or, and, mod, //book | //cd, + - * div = != < > <= >=
    # result = etree_html.xpath('//span[@class="pubtime" and contains(text(), "09-07")]/text()')
    # print(result)

    # 按序选择 [1] [last()] [poistion() < 3] [last() -2]
    # 节点轴
    # //li/ancestor::*  所有祖先节点
    # //li/ancestor::div div这个祖先节点
    # //li/attribute::* attribute轴，获取li节点所有属性值
    # //li/child::a[@href="link1.html"]  child轴，获取直接子节点
    # //li/descendant::span 获取所有span类型的子孙节点
    # //li/following::* 选取文档中当前节点的结束标记之后的所有节点
    # //li/following-sibling::*     选取当前节点之后的所用同级节点

    # result = etree_html.xpath('//img/attribute::*')
    # print(result)

    result = etree_html.xpath(
        '//div[contains(@class, "channel-group-rec")]//div[@class="title"]/following::*[1]/text()')
    print(result)


# 解析目标页面
def parse_item_xpath(html):
    # 接收参数，使用解析库生成目标对象
    etree_html = etree.HTML(html)
    # 解析小组讨论题目
    result = etree_html.xpath('//div[@class="bd"]/h3/a/text()')
    # print(result)
    result_title = result
    # 解析小组组名
    result = etree_html.xpath('//div[@class="source"]/span/a/text()')
    # print(result)
    result_source = result
    # 解析小组讨论内容简介
    result = etree_html.xpath('//div[@class="block"]/p/text()')
    # print(result)
    result_block = result
    # 解析当前获得喜欢数
    result = etree_html.xpath('//div[@class="likes"]/text()[1]')
    # print(result)
    result_likes = result
    # 解析发布时间
    result = etree_html.xpath('//span[@class="pubtime"]/text()')
    # print(result)
    result_pubtime = result
    # 解析图片地址
    # result = etree_html.xpath('//div[@class="pic"]/div/img/@src')
    # print(result)
    # result_src = result

    items = []
    for i in range(len(result_block)):
        item = {}
        item['title'] = result_title[i]
        item['source'] = result_source[i]
        item['block'] = result_block[i]
        item['likes'] = result_likes[i]
        item['pubtime'] = result_pubtime[i]
        # 有些讨论没有图片
        # item['src'] = result_src[i]
        items.append(item)

    return items


# 将数据本地化
def write_json(items):
    info_json = json.dumps(items, ensure_ascii=False, check_circular=True)
    filename = './豆瓣小组精选'
    with open(filename, "a", encoding='utf-8') as f:
        f.write(info_json)


# 主程序
def main():
    for i in range(1, 298):
        page = str(i * 30)
        url = "https://www.douban.com/group/explore?start=" + page
        if i == 0:
            url = "https://www.douban.com/group/explore"
        html = get_one_page(url)
        # print(html)
        # parse_with_xpath(html)
        items = parse_item_xpath(html)
        write_json(items)


if __name__ == '__main__':
    main()
