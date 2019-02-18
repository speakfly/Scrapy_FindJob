# -*- coding: utf-8 -*-
import scrapy
from findjob.settings import KEYWORD_LIST
import json
from findjob.items import FindjobItem
import re

class ZhilianSpiderSpider(scrapy.Spider):
    name = 'zhilian_spider'
    allowed_domains = ['fe-api.zhaopin.com', 'jobs.zhaopin.com']

    # 从settings.py中读取 搜索关键字
    start_urls = []
    for KEYWORD in KEYWORD_LIST:
        start_urls.append('https://fe-api.zhaopin.com/c/i/sou?pageSize=100&kw=%s&kt=3&start=0'%KEYWORD)

    # 设置保存方法
    custom_settings = {
                        "ITEM_PIPELINES":{
                                        'findjob.pipelines.ZhiLianPipeline': 300,
                                        }
                      }

    def parse(self, response):

        # 将获取的json文件转化成 字典
        data_list_dict = json.loads(response.text)

        # 获取数据列表
        data_list = data_list_dict['data']['results']

        for i_item in range(len(data_list)):
            """获取信息"""
            # 跟新时间
            update_date = data_list[i_item]['updateDate']
            # 详细URL
            URL = data_list[i_item]['positionURL']
            # 传递跟新时间 因为在详细URL页面没有标明 跟新时间
            yield scrapy.Request(URL, callback=self.get_body, meta={'update_date':update_date})

        # 翻页处理
        """
        翻页原理是:
        start的值 表示 从第几个数据开始显示  只要更新url中start的值就能达到翻页效果
        """
        START_PAGE = response.meta.get('START_PAGE', 0)
        if data_list_dict['data']['numTotal'] > START_PAGE:
            old_start_page = 'start=' + str(START_PAGE)
            START_PAGE = START_PAGE + 100
            new_start_page = 'start=' + str(START_PAGE)
            yield scrapy.Request(response.url.replace(old_start_page, new_start_page), callback=self.parse, meta={'START_PAGE':START_PAGE})

    def get_body(self, response):
        findjob_item = FindjobItem()
        findjob_item['postn_url'] = response.url
        findjob_item['requirements'] = ''.join(response.css('.pos-ul ::text').extract()).replace('\n', '').replace('\xa0', '').strip()
        findjob_item['welfare'] = response.xpath('//*').re("JobWelfareTab = '(.*)'")[0].split(',')
        findjob_item['address'] = response.xpath('/html/body/div[1]/div[3]/div[4]/div/ul/li[2]/div[2]/span[1]/a/text()').extract_first()
        findjob_item['salary'] = response.xpath('/html/body/div[1]/div[3]/div[4]/div/ul/li[1]/div[1]/strong/text()').extract_first()
        findjob_item['create_time'] = response.meta.get('update_date', '')
        findjob_item['company_name'] = response.xpath('/html/body/div[1]/div[3]/div[4]/div/ul/li[2]/div[1]/a/text()').extract_first()
        findjob_item['position_id'] = response.url.split('/')[-1].split(".")[0]
        findjob_item['position_name'] = response.xpath('/html/body/div[1]/div[3]/div[4]/div/ul/li[1]/h1/text()').extract_first()

        # 使用正则表达式 获取 最低工作经验年数
        worked_year_string = response.xpath('/html/body/div[1]/div[3]/div[4]/div/ul/li[2]/div[2]/span[2]/text()').extract_first()
        worked_year_result = re.search('(\d+)', worked_year_string)
        if worked_year_result:
            findjob_item['worked_year'] = worked_year_result.group(1)
        else:
            findjob_item['worked_year'] = "不限"

        findjob_item['educational'] = response.xpath('/html/body/div[1]/div[3]/div[4]/div/ul/li[2]/div[2]/span[3]/text()').extract_first()

        yield findjob_item
