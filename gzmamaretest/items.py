# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

def defSerializer(value):
    return value

def mySerializer(value):
    return "my define" % value

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # scrapy.Field()代表的0,N的元素概念
    # 标题名称
    title = scrapy.Field(serializer=defSerializer)
    # URL路径
    URL = scrapy.Field(serializer=defSerializer)
    # 图片路径
    imgSet = scrapy.Field(serializer=defSerializer)
    # 评论信息（带时间）
    extraInfo = scrapy.Field(serializer=mySerializer)
    # 主贴文字信息（带时间）
    wordInfo = scrapy.Field(serializer=mySerializer)
    # 表格信息
    formInfo = scrapy.Field(serializer=mySerializer)
    # 附加域
    #num = scrapy.Field(serializer=defSerializer)
    



