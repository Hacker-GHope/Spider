# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 10:16
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : sports.py
# @Software: PyCharm
import json
import pymysql
import requests


# 获取页面
def get_html(url):
    # 伪装请求头
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    # 请求页面
    response = requests.get(url, headers=headers)
    # 判断是否请求成功
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


# 去除不需要的元素
def get_real_content(html):
    # 判断页面存在且有数据
    if html and len(html) > 128:
        # 得到json数据
        i = html.index('(')
        html1 = html[i+1:]
        html1 = html1.replace(');', '')
        return html1
    return None


# 获取所需字段
def get_filed(result):
    # 得到json数据中所需数据模块
    docs = result['result']['wall']['docs']
    # 设置接收数据的容器
    filed = []
    # 遍历数据模块
    for i in range(len(docs)):
        # 设置接收信息的字典
        item = {}
        # 商品描述
        item['title'] = docs[i]['title']
        # 商品图片地址
        item['img'] = docs[i]['img']
        # 原价
        item['orgPrice'] = docs[i]['orgPrice']
        # 已售
        item['sale'] = docs[i]['sale']
        # 收藏
        item['cfav'] = docs[i]['cfav']
        # 现价
        item['price'] = docs[i]['price']
        # 商品链接
        item['link'] = docs[i]['link']
        # 商品唯一标识，设置唯一索引，实现数据去重
        item['tradeItemId'] = docs[i]['tradeItemId']
        # 将所需信息添加到设置的容器中
        filed.append(item)
    # 将包含数据的容器返回
    return filed


# 保存数据到数据库
def join_mysql(filed):
    # 设置数据库参数
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    port = 3306
    db = 'mugujie'
    db = pymysql.connect(host=host, user=user, password=password, port=port, db=db)
    # 连接数据库
    cursor = db.cursor()
    for i in range(len(filed)):
        sql = "INSERT INTO sports(title,img,orgPrice,sale,cfav,price,link,tradeItemId)" \
              " VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(filed[i]['title'],
                                                                   filed[i]['img'], filed[i]['orgPrice'],
                                                                   filed[i]['sale'], filed[i]['cfav'],
                                                                   filed[i]['price'], filed[i]['link'],filed[i]['tradeItemId'])
        # 接收唯一索引抛出的重复数据引起的异常
        try:
            # print(sql)
            cursor.execute(sql)
            db.commit()
        except:
            print('该数据已存在')

    # 关闭连接
    db.close()


# 主程序
def main():
    # 循环启动标志
    flag = False
    # 初始页数
    page = 1
    # 判断是否存在下一页
    while not flag:
        url = 'https://list.mogujie.com/search?callback=jQuery211029443583119290473_1540347760408&_version=8193&ratio=3%3A4&cKey=15&page=' + str(
            page)
        # 得到页面
        html = get_html(url)
        # 得到json格式数据
        html_content = get_real_content(html)
        print(html_content)
        # 将json格式数据转换为Python可以操作的数据格式（字典）
        result = json.loads(html_content)
        # 得到当前页是否为最后一页
        flag = result['result']['wall']['isEnd']
        # print(result)
        # 获取目标数据
        filed = get_filed(result)
        # print(filed)
        # 将数据存到数据库中
        join_mysql(filed)
        # 下一页
        page += 1
        # print(page)


if __name__ == '__main__':
    main()
