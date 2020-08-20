# -*- coding: utf-8 -*-
# @Time    : 2020-08-20 9:40
# @Author  : 呆呆
# @Email   : 2821212670@qq.com
# @File    : Connect_database.py
# @Software: PyCharm

from pymongo import MongoClient

# host = "192.168.33.62"  # 我的ip
client = MongoClient('localhost', 27017)  # 建立数据库连接
db = client.videomonitor
collection = db.props  # 查询props表
for item in collection.find():
    print(item)


collection = db.records  #连接数据库的records表
collection.insert({"_id": "001", "picname": "张", "time": "2020-08-20", "status": "0"})
client.close()
