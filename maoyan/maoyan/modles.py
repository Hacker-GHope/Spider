# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 14:49
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : modles.py
# @Software: PyCharm

from mongoengine import *


class Movie(Document):
    name = StringField(max_length=512)
    actor = StringField(max_length=512)
    release_time = StringField(max_length=128)
    score = StringField(max_length=32)
