# -*- coding: utf-8 -*-
# @Time    : 2018/10/31 12:07
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : join_mongo.py
# @Software: PyCharm

from pymongo import MongoClient

client = MongoClient()
db = client.company

def insert_company(company_dict):
    db.comps.insert(company_dict)