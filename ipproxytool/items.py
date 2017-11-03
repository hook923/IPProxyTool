# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field


class IpProxyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = Field()
    port = Field()
    country = Field() #国家地区
    anonymity = Field() #1:高匿，2：匿名，3，透明
    https = Field() #https:yes;http:no; http,https:all
    httptype = Field() #
    speed = Field()    #速度
    alive = Field() #存活时间
    valid_time = Field() #最后一次验证的时间 mysql的timestamp类型
    valid_count = Field() #总计验证的次数int
    save_time = Field() #初次入库的时间mysql的timestamp类型
    source = Field() #来源的网站
    
