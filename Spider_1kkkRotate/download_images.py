# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 15:53
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : download_images.py
# @Software: PyCharm
from io import BytesIO
import requests
from PIL import Image


def write_image(url):
    r = requests.get(url)
    filename = url.split('?')[-1][-3:]
    img_content = r.content
    img = Image.open(BytesIO(img_content))
    for j in range(4):
        rotate_img = img.crop((76 * j, 0, 76 * (j + 1), 76))
        rotate_img.save('./images/%s%d.png' % (filename,j))
    # with open(filename, "wb") as f:
    #     f.write(r.content)


def main():
    for i in range(361):
        time = 'image3.ashx?t=1540803643' + str(i).rjust(3,'0')
        url = 'http://www.1kkk.com/' + str(time)
        write_image(url)


if __name__ == '__main__':
    main()
