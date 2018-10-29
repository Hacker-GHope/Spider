# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 15:53
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : download_images.py
# @Software: PyCharm
import random
from selenium import webdriver


# 无头浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# 启动浏览器
browser = webdriver.Chrome(chrome_options=chrome_options)
# 指定自启浏览器界面大小
browser.set_window_size(1920, 1080)



def get_page(time):
    url = 'http://www.1kkk.com/'+str(time)
    browser.get(url)
    html = browser.page_source
    return html

def main():
    for i in range(500):
        time = 'image3.ashx?t=1540803643' + str(random.randint(0, 999))
        img = get_page(time)



if __name__ == '__main__':
    main()
