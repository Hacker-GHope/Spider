# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 20:47
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : compar.py
# @Software: PyCharm

import os
import hashlib

from PIL import Image


def filecount():
    filecount = int(os.popen('dir /B |find /V /C ""').read())
    return (filecount)

def getAvg(ls):#获取平均灰度值
   return sum(ls)/len(ls)


def getGray(image_file):
    tmpls = []
    for h in range(0, image_file.size[1]):  # h
        for w in range(0, image_file.size[0]):  # w
            tmpls.append(image_file.getpixel((w, h)))

    return tmpls

def md5sum(filename):
    image_file = Image.open(filename)  # 打开
    image_file = image_file.resize((12, 12))  # 重置图片大小我12px X 12px
    image_file = image_file.convert("L")  # 转256灰度图
    Grayls = getGray(image_file)  # 灰度集合
    avg = getAvg(Grayls)  # 灰度平均值
    bitls = ''  # 接收获取0或1
    # 除去变宽1px遍历像素
    for h in range(1, image_file.size[1] - 1):  # h
        for w in range(1, image_file.size[0] - 1):  # w
            if image_file.getpixel((w, h)) >= avg:  # 像素的值比较平均值 大于记为1 小于记为0
                bitls = bitls + '1'
            else:
                bitls = bitls + '0'
    return bitls


def delfile():
    all_md5 = {}
    file_dir = os.walk('./images')
    # print(type(file_dir))
    for i in file_dir:
        for item in i[2]:
            if md5sum(item) in all_md5.values():
                os.remove(item)
            else:
                all_md5[item] = md5sum(item)


if __name__ == '__main__':
    oldf = filecount()
    print('去重前有', oldf, '个文件\n\n\n请稍等正在删除重复文件...')
    delfile()
    print('\n\n去重后剩', filecount(), '个文件')
    print('\n\n一共删除了', oldf - filecount(), '个文件\n\n')