# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 19:18
# @Author  : G.Hope
# @Email   : 1638327522@qq.com
# @File    : cut_img.py
# @Software: PyCharm

from PIL import Image

def save_images(imagelist):
    index=1
    for image in imagelist:
        image.save('./result/'+str(index)+'.png','PNG')
        if index == 4:
            return
        index+=1


def cut_image(image):
    width,height=image.size
    item_width=int(width/4)
    box_list=[]
    for i in range(4):
        for j in range(4):
            box=(j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
            box_list.append(box)

    image_list=[image.crop(box) for box in box_list]
    return image_list

def fill_image(image):
    width, height = image.size
    new_image_length = width if width > height else height
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    if width > height:
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image, (int((new_image_length - width) / 2),0))
    return new_image

if __name__=='__main__':
    file_path='./cut.png'
    image=Image.open(file_path)
    image=fill_image(image)
    image_list=cut_image(image)
    save_images(image_list)