# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FindjobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 地点
    address = scrapy.Field()
    # 工资
    salary = scrapy.Field()
    # 发布时间
    create_time = scrapy.Field()
    # 主体
    requirements = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # # 职位id
    position_id = scrapy.Field()
    # 职位名称
    position_name = scrapy.Field()
    # 工作经历年数
    worked_year = scrapy.Field()
    # 教育程度
    educational = scrapy.Field()
    # URL
    postn_url = scrapy.Field()
    # 福利
    welfare = scrapy.Field()
