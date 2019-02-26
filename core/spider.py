# -*- coding: utf-8 -*-

import time
import chardet
import requests
from lxml import etree
from threading import Thread

from core import settings

# 1.1爬取ip并解析
class Spider(object):
    def __init__(self,rule,all_queue,my_mongo):
        self.rule = rule  # 一个规则
        self.all_queue = all_queue
        my_mongo.connect()
        self.my_mongo = my_mongo

    def get_html(self,url):
        # 获取页面
        try:
            html = requests.get(url, headers=settings.HEADER)
        except:
            print("%s请求失败...使用代理..")
            html = requests.get(url, headers=settings.HEADER, proxies=self.my_mongo.find(False))
            self.my_mongo.close()
        finally:
            print("获取页面成功，开始解析..")
            html.encoding = chardet.detect(html.content)['encoding']  # 检测编码
            self.parse(url,html.text)  # 解析

    def parse(self,url,response):
        if self.rule['type'] == 're':  #
            pass
        elif self.rule['type'] == 'xpath':
            self.xpath(url,response)

    def re_type(self,response):
        pass

    def xpath(self,url,response):
        # URL可以去除，此处仅为查看那页爬取失败
        try:
            html = etree.HTML(response)
            nodes = html.xpath(self.rule['pattern'])
            for index,node in enumerate(nodes):
                proxy = {}
                try:
                    proxy['ip'] = node.xpath(self.rule['data']['ip'])[0]
                    proxy['port'] = node.xpath(self.rule['data']['port'])[0]
                    try:
                        proxy['addr'] = node.xpath(self.rule['data']['addr'])[0]
                    except:
                        proxy['addr'] = '无'
                except:
                    print(index,url,"获取ip、port、addr出错...")
                else:
                    self.all_queue.put(proxy)
        except:
            print("此页面解析出错...",url,'请检查请求头或网站')

    def run(self):
        # 遍历一种规则的url
        for url in self.rule['url']:
            self.get_html(url)
            time.sleep(2)
# 1.2 爬取class实例化并运行
def spider_instance_func(rule, all_queue,my_mongo):
    spider = Spider(rule, all_queue,my_mongo)
    spider.run()
# 1.3 进程调用
def ip_spider_process(rules,all_queue,my_mongo):
    thread_list = []
    '''每一个规则用一个线程'''
    for rule in rules:
        t1 = Thread(target=spider_instance_func, args=(rule, all_queue,my_mongo))
        thread_list.append(t1)

    for t in thread_list:
        t.start()








