# -*- coding: utf-8 -*-
# @Time    : 2018/10/25 11:20
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : Spider_jdSeacrh.py
# @Software: PyCharm
import time
import random
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree

# 无头浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# 启动浏览器
browser = webdriver.Chrome(chrome_options=chrome_options)

# 指定自启浏览器界面大小
browser.set_window_size(1400, 700)
# 设置休眠时间
wait = WebDriverWait(browser, 3)
# 设置关键字
KEYWORD = '古风'


# 模拟切换页面
def get_page(page):
    if page == 1:
        # 第一次访问的地址
        url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % quote(KEYWORD)
        # 访问地址
        browser.get(url)
        # 随机等待时间
        t = random.randint(0, 9)
        # 分六次滚动页面
        for i in range(6):
            str_js = 'var step = document.body.scrollHeight/6;window.scrollTo(0,step*%d)' % (i + 1)
            browser.execute_script(str_js)
            time.sleep(t)
    if page > 1:
        # 分六次滚动页面
        t = random.randint(0, 9)
        for i in range(6):
            str_js = 'var step = document.body.scrollHeight/6;window.scrollTo(0,step*%d)' % (i + 1)
            browser.execute_script(str_js)
            time.sleep(t)
        # 获取页数输入框
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage input.input-txt')))
        # 获取确认按钮
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage a.btn.btn-default')))
        # 清空页数输入框
        input.clear()
        # 将目标页数填入到页数输入框
        input.send_keys(page)
        # 点击确认按钮
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_bottomPage a.curr'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList')))

    # 得到访问的页面内容
    page_source = browser.page_source
    return page_source


# 解析获取到的页面
def parse_page(page_source):
    # 创建xpath解析对象
    etree_html = etree.HTML(page_source)
    # print(page_source)
    # print(type(etree_html))
    # 得到单个商品(解决一个商品单个属性中多个信息的选择)
    goods_list = list(etree_html.xpath('//div[@id="J_goodsList"]/ul/li'))
    # print(len(goods_list))
    goods_db = []
    for goods in goods_list:
        item = {}
        # 解析标识
        goods_sku = goods.xpath('./@data-sku')
        # print(goods_sku[0])
        item['sku'] = goods_sku[0]
        # 解析描述(.表示当前目录)
        goods_title = goods.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()')
        # print(goods)
        # print(goods_title)
        title = ''
        for i in goods_title:
            title += i
        # print(title)
        # print(len(goods_title))
        item['title'] = title.replace(' ', '')
        # 解析价格
        goods_price = goods.xpath('.//div[@class="p-price"]/strong/i/text()')
        # print(goods_price[0])
        item['price'] = goods_price[0]
        # 解析商家
        goods_shop = goods.xpath('.//div[@class="p-shop"]/span/a/@title')
        # print(goods_shop[0])
        item['shop'] = goods_shop[0]
        # 解析评价数量
        goods_commit = goods.xpath('.//div[@class="p-commit"]/strong/a/text()')
        # print(goods_commit[0])
        item['commit'] = goods_commit[0]
        # 解析图片地址(部分图片加载不到，设置重复更新后多次爬取)
        goods_img = goods.xpath('.//div[@class="p-img"]/a/img/@src')
        # print(goods_img)
        item['img'] = goods_img
        if goods_img:
            item['img'] = goods_img[0]
        else:
            item['img'] =''
        # 解析商品链接
        goods_link = goods.xpath('.//div[@class="p-img"]/a/@href')
        # print(goods_link)
        item['link'] = goods_link[0]
        # 将解析好的单品信息加入返回结果中
        goods_db.append(item)
    return goods_db


def join_MySql(goods_db):
    # 设置数据库参数
    host = '127.0.0.1'
    user = 'root'
    password = 'root'
    port = 3306
    db = 'jdSeacrh'
    db = pymysql.connect(host=host, user=user, password=password, port=port, db=db)
    # 连接数据库
    cursor = db.cursor()
    for i in range(len(goods_db)):
        sql = "INSERT INTO seacrh_gufeng(sku,title,price,shop,commit,img,link)" \
              " VALUES('{}','{}','{}','{}','{}','{}','{}')".format(goods_db[i]['sku'], goods_db[i]['title'],
                                                                  goods_db[i]['price'], goods_db[i]['shop'],
                                                                  goods_db[i]['commit'],
                                                                  goods_db[i]['img'], goods_db[i]['link'])
        # print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print('元素已存在')
    db.close()


def main():
    for page in range(100):
        # 动态增加页数
        page_source = get_page(page + 1)
        # 解析页面内容
        goods_db = parse_page(page_source)
        join_MySql(goods_db)


if __name__ == '__main__':
    main()
