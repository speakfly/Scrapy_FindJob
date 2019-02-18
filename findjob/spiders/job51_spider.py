# -*- coding: utf-8 -*-
import scrapy
from findjob.items import FindjobItem
from findjob.settings import KEYWORD_LIST
import re

class Job51SpiderSpider(scrapy.Spider):
    name = 'job51_spider'
    allowed_domains = ['51job.com']

    # 设置开始url
    start_urls = []
    for KEYWORD in KEYWORD_LIST:
        start_urls.append('https://search.51job.com/list/%252C,000000,0000,00,9,99,{},2,1.html'.format(KEYWORD))

    # 该爬虫专属设置
    custom_settings = {
                        "ITEM_PIPELINES":{
                                        'findjob.pipelines.FiveOneJobPipeline': 300,
                                        }
                      }


    def parse(self, response):

        # 详情URL
        URL = response.xpath('/html/body/div[2]/div[4]/div[4]/p/span/a/@href').extract_first()
        yield scrapy.Request(URL, callback=self.parse_item)

        # 最后一页
        LAST_PAGE = response.meta.get('LAST_PAGE', 0)

        # 判断是否是第一页 如果是则获取总共有多少页
        if LAST_PAGE == 0:
            last_page_string = response.xpath('/html/body/div[2]/div[4]/div[55]/div/div/div/span[1]/text()').extract_first()
            LAST_PAGE = int(re.search(('(\d+)'), last_page_string).group(1))

        # 翻页
        PAGE = int(re.search('(\d+)\.html', response.url).group(1))
        if PAGE < LAST_PAGE:
            URL = response.url.replace(str(PAGE)+".html", str(PAGE+1)+".html")
            yield scrapy.Request(URL, callback=self.parse, meta={'LAST_PAGE':LAST_PAGE})


    def parse_item(self, response):
        """
        内容解析
        """

        # 结构体
        findjob_item = FindjobItem()


        # 获取 地点,工作经历,教育程度,招多少人,发布时间 (按顺序排列)
        # 据分析 教育程度 可能不会写出来  其他都会写出来
        long_data = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title').extract_first().replace('\xa0', '').split('|')

        # 地点
        findjob_item['address'] = long_data[0]
        # 工资
        salary_result_string = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').extract_first()

        if salary_result_string:
            salary_result = re.search('(\d+\.?\d?)-(\d+\.?\d?)(\w)', salary_result_string)

            if salary_result:
                if salary_result.group(3) == '万':
                    unit = 10000
                elif salary_result.group(3) == '千':
                    unit = 1000
                findjob_item['salary'] = str(int(float(salary_result.group(1))*unit)) + "-" + str(int(float(salary_result.group(2))*unit))+ "元/月 "

        # 发布时间
        findjob_item['create_time'] = '2019-' + long_data[-1].replace('发布', '')

        # 要求
        findjob_item['requirements'] = ''.join(response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div//p/text()').extract()).strip()

        # 公司名称
        findjob_item['company_name'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/text()').extract_first().strip()

        # 职位id
        findjob_item['position_id'] = re.search('(\d+)\.html', response.url).group(1)

        # 职位名称
        findjob_item['position_name'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/text()').extract_first().strip()

        # 工作经历年数
        worked_year_result = re.search('(\d+)', long_data[1])
        if worked_year_result:
            findjob_item['worked_year'] = worked_year_result.group(1)
        else:
            findjob_item['worked_year'] = '不限'

        # 教育程度
        if len(long_data) == 5:
            findjob_item['educational'] = long_data[2]

        # 详情URL
        findjob_item['postn_url'] = response.url

        # 福利
        findjob_item['welfare'] = ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div//text()').extract()).split()

        yield findjob_item
