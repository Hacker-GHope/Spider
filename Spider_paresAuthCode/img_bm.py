# -*- coding: utf-8 -*-
# @Time    : 2018/10/26 11:49
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : img_bm.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from PIL import Image
from chaojiying import main1
from io import BytesIO

# 无头浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# 启动浏览器
browser = webdriver.Chrome(chrome_options=chrome_options)

# 指定自启浏览器界面大小
browser.set_window_size(1920, 1080)
# 显式等待  针对整个节点的等待
wait = WebDriverWait(browser, 3)


def get_page():
    url = 'http://bm.e21cn.com/log/reg.aspx'
    browser.get(url)
    html = browser.page_source
    return html


def get_screen_shot():
    """
    获取网页截图
    :return: 截图对象
    """
    screen_shot = browser.get_screenshot_as_png()
    screen_shot = Image.open(BytesIO(screen_shot))
    return screen_shot


def get_position():
    """
    获取验证码位置
    :return: 验证码位置元组
    """
    img = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#imgCheckCode')))
    time.sleep(2)
    location = img.location
    # print(location)
    size = img.size
    # print(size)
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
        'width']
    return (top, bottom, left, right)


def get_image(img_name):
    """
    获取验证码图片
    :return: 图片对象
    """
    top, bottom, left, right = get_position()
    # print('验证码位置', top, bottom, left, right)
    screen_shot = get_screen_shot()
    captcha = screen_shot.crop((left, top, right, bottom))
    captcha.save(img_name)
    return captcha


def get_msg():
    # 模拟注册，发现需要短信验证码，暂且搁置
    username = 'yiersan'
    password = '123456'
    tel = '18011405897'
    img_name = 'yzm.png'
    img = get_image(img_name)
    print(img)
    check_msg = main1(img_name)
    # 输出图片验证码结果
    print(check_msg)
    input_username = wait.until(expected_conditions.presence_of_element_located
                                ((By.CSS_SELECTOR, 'input#username')))
    input_password1 = wait.until(expected_conditions.presence_of_element_located
                                 ((By.CSS_SELECTOR, 'input#pwd')))
    input_password2 = wait.until(expected_conditions.presence_of_element_located
                                 ((By.CSS_SELECTOR, 'input#pwd_Q')))
    input_tel = wait.until(expected_conditions.presence_of_element_located
                           ((By.CSS_SELECTOR, 'input#tel')))
    input_check = wait.until(expected_conditions.presence_of_element_located
                             ((By.CSS_SELECTOR, 'input#CheckCode')))
    sublime = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'input#btn_login')))
    input_username.send_keys(username)
    input_password1.send_keys(password)
    input_password2.send_keys(password)
    input_tel.send_keys(tel)
    input_check.send_keys(check_msg)
    time.sleep(2)
    sublime.click()


def main():
    get_page()
    get_msg()


if __name__ == '__main__':
    main()
