# -*- coding: utf-8 -*-
import gevent
import requests

from core import settings


# 2.1 验证爬取ip存入mongdb
from core.flask_server import start_server


def checkout_func(proxy, my_mongo):
    ip = "{}:{}".format(proxy['ip'],proxy['port'])
    proxy_dict = {
        'http':'http://' + ip,
        'https':'https://' + ip,
    }
    try:
        # 简单验证ip可用否
        r = requests.get('https://www.baidu.com', headers=settings.HEADER, proxies=proxy_dict, timeout=settings.TIMEOUT)
    except:
        print("%s不可用.." % ip)
    else:
        if r.ok:
            print("%s可用..加入队列.." % ip)
            my_mongo.connect()
            my_mongo.insert(proxy)
            my_mongo.close()
# 2.2 进程调用
def check_all_ip_process(all_queue, my_mongo):
    proxy_dict_list = []
    while True:
        if not all_queue.empty():
            proxy_dict = all_queue.get()
            proxy_dict_list.append(proxy_dict)
            if len(proxy_dict_list) > 10:
                # print("ip获取大于10，开始检测...")
                spawns = []
                # 协程
                for proxy in proxy_dict_list:
                    spawns.append(gevent.spawn(checkout_func, proxy, my_mongo))
                gevent.joinall(spawns)
                proxy_dict_list = []

# 3.1 验证mongdb内ip是否过期
def check_db_func(proxy,my_mongo):
    ip = "{}:{}".format(proxy['ip'], proxy['port'])
    proxy_dict = {
        'http': 'http://' + ip,
        'https': 'https://' + ip,
    }
    try:
        # 简单验证ip可用否
        r = requests.get('https://www.baidu.com', headers=settings.HEADER, proxies=proxy_dict, timeout=settings.TIMEOUT)
    except:
        print("过期不可用去除%s" % ip)
        my_mongo.delete(proxy)
        my_mongo.close()
    else:
        if r.ok :
            print("%s还可继续使用..." % ip)

# 3.2 进程调用
def check_db_process(my_mongo):
    start_server()
    while True:
        try:
            my_mongo.connect()
            proxy_dict_list = my_mongo.find(False)
        except:
            pass
        else:
            if len(proxy_dict_list) > 5: # 数据库ip大于5再验证
                spawns = []
                # 协程
                for proxy in proxy_dict_list:
                    spawns.append(gevent.spawn(check_db_func, proxy,my_mongo))
                gevent.joinall(spawns)
