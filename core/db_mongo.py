# -*- coding: utf-8 -*-
import pymongo
import random
from core import settings


class MyMongo():
    def connect(self):
        self.client = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
        db = self.client['ipProxyPool']
        self.collection = db['item']

    def insert(self,data=None):
        # 插入数据
        if data:
            self.collection.insert(data)
            print(data,'写入数据库...')

    def find(self,flag=False):
        # 查找数据
        data = self.collection.find().limit(30)
        data_list = [item for item in data]
        if flag:
            return random.choice(data_list)
        else:
            return data_list
    def delete(self,data=None):
        # 删除数据
        if data:
            self.collection.remove(data)
            # print('删除数据..',data)
    def clear(self):
        # 清空集合
        self.collection.drop()
    def close(self):
        self.client.close()

if __name__ == '__main__':
    db = MyMongo()
    print('asdfas',db.find(False))
    # db.insert({'ip':'11',"port":11})
    # db.insert({'ip':'22',"port":22})
    # db.insert({'ip':'33',"port":33})
    # db.delete({'ip':'33'})