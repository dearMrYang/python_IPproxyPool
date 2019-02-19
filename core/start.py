# -*- coding: utf-8 -*-
import gevent
from gevent import monkey
monkey.patch_all()
from core import settings
from core.check import check_all_ip_process, check_db_process
from core.db_mongo import MyMongo
from core.flask_server import start_server
from core.spider import ip_spider_process


def main():
    from multiprocessing import Queue
    all_queue = Queue()  # 获取的所有IP地址
    my_mongo = MyMongo()
    if settings.DEBUG:
        my_mongo.connect()
        my_mongo.clear()
        my_mongo.close()
    from multiprocessing import Process
    p1 = Process(target=ip_spider_process, args=(settings.RULES, all_queue,my_mongo))  # 获取ip进程
    p2 = Process(target=check_all_ip_process, args=(all_queue,my_mongo))  # 验证ip进程
    p3 = Process(target=check_db_process, args=(my_mongo,))  # 验证数据库ip进程
    p4 = Process(target=start_server)  # flask
    p1.start()
    p2.start()
    p3.start()
    p4.start()