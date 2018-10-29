# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 20:47
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : compar.py
# @Software: PyCharm

import os
import time
import hashlib


def getmd5(file):
    if not os.path.isfile(file):
        return
    fd = open(file, 'rb')
    md5 = hashlib.md5()
    md5.update(fd.read())
    fd.close()
    return md5.hexdigest()


if __name__ == "__main__":
    allfile = []
    md5list = []
    sizelist = []
    identicallist = []

    start = time.time()
    uipath = './'

    for path, dir, filelist in os.walk(uipath):
        for filename in filelist:
            allfile.append(os.path.join(path, filename))
    # 先比较图片大小，大小都不一样，肯定不是重复图片
    # 大小一样再根据MD5值比较
    for photo in allfile:
        size = os.path.getsize(photo)
        if size not in sizelist:
            sizelist.append(size)
        else:
            md5sum = getmd5(photo)
            if md5sum not in md5list:
                md5list.append(md5sum)
            else:
                identicallist.append(photo)
    end = time.time()
    last = end - start
    print("identical photos: " + str(len(identicallist)))
    print("time: " + str(last) + "s")
    print("count: " + str(len(allfile)))
