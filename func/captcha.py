import random

import string

import sys

import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 字体的位置，不同版本的系统会有不同

font_path = 'func/arial.ttf'

# 背景颜色，默认为白色

bgcolor = (255, 255, 255)

# 字体颜色，默认为蓝色

fontcolor = (0, 0, 255)

# 干扰线颜色。默认为红色

linecolor = (255, 0, 0)


# 用来随机生成一个字符串

def gene_text(bit=4):
    source = list("qwertyuiopasdfghjklzxcvbnm")

    for index in range(0, 10):
        source.append(str(index))

    return ''.join(random.sample(source, bit))  # number是生成验证码的位数


# 用来绘制干扰线

def gene_line(draw, width, height):
    line_color = random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)

    begin = (random.randint(0, width), random.randint(0, height))

    end = (random.randint(0, width), random.randint(0, height))

    draw.line([begin, end], fill=line_color, width=int(min(width, height) / 25))


# 生成验证码

def gene_code(bit, size, line_number_range):
    width, height = size  # 宽和高

    image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片

    font = ImageFont.truetype(font_path, int(min(size) * 0.8))  # 验证码的字体

    draw = ImageDraw.Draw(image)  # 创建画笔

    text = gene_text(bit)  # 生成字符串

    font_width, font_height = font.getsize(text)

    draw.text(((width - font_width) / bit, (height - font_height) / bit), text,

              font=font, fill=fontcolor)  # 填充字符串

    for i in range(random.randint(line_number_range[0], line_number_range[1])):
        gene_line(draw, width, height)

    # image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲

    # image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲

    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强

    # image.save('idencode.png')  # 保存验证码图片

    # image.show(

    return text, image


if __name__ == "__main__":
    text, image = gene_code(4, (100, 60), (3, 4))
    image.show()
