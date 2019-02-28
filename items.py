# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PinduoduoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'store'  # 数据库表名

    goods_id = scrapy.Field()  # 商品ID
    goods_name = scrapy.Field()  # 商品名字
    price = scrapy.Field()  # 拼团价格 返回的字段多乘了100
    sales = scrapy.Field()  # 已拼单数量
    normal_price = scrapy.Field()  # 单独购买价格
    # comments = scrapy.Field()  # 商品评价
    opt_id = scrapy.Field()  # 小分类ID
    opt_name = scrapy.Field()  # 小分类名字
    link_url = scrapy.Field()  # 商品地址
    mall_id = scrapy.Field()  # 店铺ID
    mall_name = scrapy.Field()  # 店铺名字
