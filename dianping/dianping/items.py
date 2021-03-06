# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    # 菜系分类
    cuisine = scrapy.Field()
    # 店名
    name = scrapy.Field()
    # 店址
    shop_url = scrapy.Field()
    # 星级
    star = scrapy.Field()
    # 点评数
    comment_count = scrapy.Field()
    # 人均消费
    avg_price = scrapy.Field()
    # 区
    district = scrapy.Field()
    # 街道
    street = scrapy.Field()
    # 更新时间
    update_time = scrapy.Field()

