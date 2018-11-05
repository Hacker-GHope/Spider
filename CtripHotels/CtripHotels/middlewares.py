# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import signals


class CtriphotelsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CtriphotelsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, timeout):
        # 无头浏览器
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"')

        # 启动浏览器
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

        # 指定自启浏览器界面大小
        self.browser.set_window_size(1400, 1000)
        # 页面加载时间
        self.browser.set_page_load_timeout(timeout)
        # 显式等待  针对整个节点的等待
        self.wait = WebDriverWait(self.browser, 3)

    def __del__(self):
        self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings.get("SELENIUM_TIMEOUT"))
        # crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        self.browser.get(request.url)
        city_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txtCity')))
        city_input.clear()
        city_input.send_keys('武汉')

        check_in_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txtCheckIn')))
        check_in_input.clear()
        check_in_input.send_keys('2018-12-07')

        check_out_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txtCheckOut')))
        check_out_input.clear()
        check_out_input.send_keys('2018-12-14')

        room_count_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_roomCount')))
        room_count_input.click()
        time.sleep(3)
        room_3_click = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[@id="J_roomCountList"]/li[3]')))
        room_3_click.click()

        member_click = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="J_RoomGuestInfoTxt"]')))
        member_click.click()
        adult_click = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[@id="J_AdultCount"]//i[@class="icon_numplus"]')))
        adult_click.click()
        adult_click.click()
        adult_click.click()

        baby_click = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[@id="J_ChildCount"]//i[@class="icon_numplus"]')))
        baby_click.click()
        baby_click.click()

        member_ok = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@id="J_RoomGuestInfoBtnOK"]')))
        member_ok.click()

        search = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@id="btnSearch"]')))
        search.click()

        time.sleep(10)

        # self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#btnSearch::attr(value)'), '搜索'))
        # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txtCity')))
        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                            status=200)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
