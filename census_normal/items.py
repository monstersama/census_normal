# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CensusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Datetime = scrapy.Field()
    value = scrapy.Field()
    Species = scrapy.Field()
    Measurment = scrapy.Field()
    Period = scrapy.Field()
    Source = scrapy.Field()
    Organization = scrapy.Field()
    Updatetime = scrapy.Field()
    table = ''

class us_m3_durable_goods_new_order_mItem(CensusItem):
    table = 'us_m3_durable_goods_new_order_m'

class us_m3_durable_goods_inventory_mItem(CensusItem):
    table = 'us_m3_durable_goods_inventory_m'

class us_m3_durable_goods_shipment_mItem(CensusItem):
    table = 'us_m3_durable_goods_shipment_m'

class us_m3inventories_mItem(CensusItem):
    table = 'us_m3inventories_m'

class us_m3neworders_mItem(CensusItem):
    table = 'us_m3neworders_m'

class us_m3value_of_shipment_mItem(CensusItem):
    table = 'us_m3value_of_shipment_m'