# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random
from scrapy import signals
import pymysql


class ProxyMysqlMiddleware(object):
    def __init__(self, host, database, user, password, port):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )


    def get_proxy(self):
        '''
        调用代理池，获取一个随机代理
        :return: random proxy
        '''
        try:
            self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
            self.cursor = self.db.cursor()
            sql = 'select IP,Port,Organization from proxypool where Country_ID != "CN" and Updatetime>date_sub(NOW(),INTERVAL 2 day) order by -UseDatetime LIMIT 1,100'
            self.cursor.execute(sql)
            self.result = self.cursor.fetchall()
            self.proxy_list = list(map(lambda li:li[0]+':'+li[1], [li for li in self.result]))
            return random.choice(self.proxy_list)
        except:
            self.logger.debug('代理未获取')
            'something error!!'
        finally:
            self.db.close()


    def process_request(self, request, spider):
        proxy = self.get_proxy()
        if proxy:
            url = 'https://{proxy}'.format(proxy=proxy)
            self.logger.debug('使用代理: ' + proxy)
            request.meta['proxy'] = url


class ProxyLocalMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        proxy = 'localhost:1080'
        self.logger.debug('使用本机代理: '+proxy)
        request.meta['proxy'] = proxy