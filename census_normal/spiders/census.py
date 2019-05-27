# -*- coding: utf-8 -*-
import scrapy
import datetime
from census_normal.items import us_m3_durable_goods_inventory_mItem, \
    us_m3_durable_goods_shipment_mItem, us_m3_durable_goods_new_order_mItem, us_m3inventories_mItem, \
    us_m3neworders_mItem, us_m3value_of_shipment_mItem


class CensusSpider(scrapy.Spider):
    name = 'census_s'
    allowed_domains = ['www.census.gov']

    def start_requests(self):
        urls = ['https://www.census.gov/econ/currentdata/dbsearch?program=M3&startYear=1992&endYear=2019&categories=MDM&dataType=NO&geoLevel=US&adjusted=1&submit=GET+DATA&releaseScheduleId=',
                'https://www.census.gov/econ/currentdata/dbsearch?program=M3&startYear=1992&endYear=2019&categories=MDM&dataType=TI&geoLevel=US&adjusted=1&submit=GET+DATA&releaseScheduleId=',
                'https://www.census.gov/econ/currentdata/dbsearch?program=M3&startYear=1992&endYear=2019&categories=MDM&dataType=VS&geoLevel=US&adjusted=1&submit=GET+DATA&releaseScheduleId=',
                'https://www.census.gov/econ/currentdata/dbsearch?program=M3&startYear=1992&endYear=2019&categories=MTM&dataType=TI&geoLevel=US&adjusted=1&submit=GET+DATA&releaseScheduleId=',
                'https://www.census.gov/econ/currentdata/dbsearch?program=M3&startYear=1992&endYear=2019&categories=MTM&dataType=NO&geoLevel=US&adjusted=1&submit=GET+DATA&releaseScheduleId=',
                'https://www.census.gov/econ/currentdata/dbsearch?program=M3&startYear=1992&endYear=2019&categories=MTM&dataType=VS&geoLevel=US&adjusted=1&submit=GET+DATA&releaseScheduleId=',]
        for url in urls:
            # meta_proxy = 'localhost:1080'
            yield scrapy.Request(url=url, callback=self.parse)


    def judge_table(self, id1, id2):
        """
        将不同类型数据存入对应的表
        """
        if 'Durable Goods' in id1:
            if 'New' in id2:
                item = us_m3_durable_goods_new_order_mItem()
            elif 'Inventories' in id2:
                item = us_m3_durable_goods_inventory_mItem()
            elif "Shipments" in id2:
                item = us_m3_durable_goods_shipment_mItem()
        else:
            if 'New' in id2:
                item = us_m3neworders_mItem()
            elif 'Inventories' in id2:
                item = us_m3inventories_mItem()
            elif 'Shipments' in id2:
                item = us_m3value_of_shipment_mItem()
        return item

    def parse(self, response):
        # 插入调试
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        identification1 = (response.xpath('//*[@id="report0"]/strong/text()').extract_first()) # 判断统计的货物目录
        identification2 = (response.xpath('//*[@id="report0"]/text()').extract())[3] # 判断货物类型
        months = (response.xpath('.//thead/tr/th/text()').extract())[1:] # 去除第一个非月份
        per_year_results = response.xpath('//tbody/tr') # 获取每一年的所有数据
        for per_year_result in per_year_results:
            year = per_year_result.xpath('.//th/text()').extract_first()
            results = per_year_result.xpath('.//td/text()').extract()
            for month, value in enumerate(results):
                Datetime = datetime.datetime.strptime(months[month]+year, '%b%Y')  # 格式化为datetime
                # 值转为float
                if value == 'NA':
                    value = 0
                else:
                    value = float(value.replace(',', ''))

                item = self.judge_table(identification1, identification2)
                item['Species'] = ''
                item['Measurment'] = 'Millions of Dollars'
                item['Period'] = 'Monthly'
                item['Source'] = 'www.census.gov'
                item['Organization'] = 'U.S. Census Bureau'
                item['Datetime'] = Datetime
                item['value'] = value
                item['Updatetime'] = datetime.datetime.now()
                yield item





