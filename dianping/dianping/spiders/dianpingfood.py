# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DianpingItem
from ..Logging import Logging
from lxml import etree

class DianpingfoodSpider(CrawlSpider):
    name = 'dianpingfood'
    allowed_domains = ['www.dianping.com']
    start_urls = ['https://www.dianping.com/tianjin/food']

    # https://www.dianping.com/search/category/10/10/r51p1
    rules = (
        Rule(LinkExtractor(allow=r'.*?/search/category/10/10/.*?'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        Logging.debug('<---------- 开始解析 ---------->')
        Logging.info('url: %s' % response.url)

        item = DianpingItem()
        # 解析
        names = []
        stars = []
        cuisines = []
        districts = []
        comment_counts = []
        avg_prices = []
        streets = []
        datas = response.xpath('//li[@class=""]/div[@class="txt"]').extract()
        for index in range(len(datas)):
            Logging.debug('<---------- %d ---------->' % index)
            data = datas[index]
            selector = etree.HTML(data)

            name_list = selector.xpath('//div[@class="tit"]/a/h4/text()')
            names.append(name_list[0].encode('u8')) if len(name_list) != 0 else names.append('')

            star_list = selector.xpath('//div[@class="comment"]/span/@title')
            stars.append(star_list[0].encode('u8')) if len(star_list) != 0 else stars.append('')

            tag_addrs_list = selector.xpath('//div[@class="tag-addr"]/a/span[@class="tag"]/text()')
            cuisines.append(tag_addrs_list[1].encode('u8')) if len(tag_addrs_list)>=1 else cuisines.append('')
            districts.append(tag_addrs_list[0].encode('u8')) if len(tag_addrs_list)>0 else districts.append('')

            comment_count_list = selector.xpath('//div[@class="comment"]/a[@class="review-num"]/b/text()')
            comment_counts.append(comment_count_list[0].encode('u8')) if len(comment_count_list) != 0 else comment_counts.append('0')

            avg_price_list = selector.xpath('//div[@class="comment"]/a[@class="mean-price"]/b/text()')
            avg_prices.append(avg_price_list[0].encode('u8')) if len(avg_price_list) != 0 else avg_prices.append('')

            street_list = selector.xpath('//div[@class="tag-addr"]/span[@class="addr"]/text()')
            streets.append(street_list[0].encode('u8')) if len(street_list) != 0 else streets.append('')

            Logging.info('name: %s' % names[index])
            Logging.info('star: %s' % stars[index])
            Logging.info('cuisine: %s' % cuisines[index])
            Logging.info('comment_count: %s' % comment_counts[index])
            Logging.info('avg_price: %s' % avg_prices[index])
            Logging.info('district: %s' % districts[index])
            Logging.info('street: %s' % streets[index])

            Logging.debug('<---------- %d ---------->' % index)

        item['name'] = names
        item['star'] = stars
        item['cuisine'] = cuisines
        item['comment_count'] = comment_counts
        item['avg_price'] = avg_prices
        item['district'] = districts
        item['street'] = streets

        # [Logging.info('name: %s' % name) for name in item['name']]
        #
        # item['star'] = response.xpath('//li[@class=""]/div[@class="txt"]/div[@class="comment"]/span/@title').extract()
        # [Logging.info('star: %s' % star) for star in item['star']]
        #
        # tag_addrs = response.xpath('//li[@class=""]/div[@class="txt"]/div[@class="tag-addr"]/a/span['
        #                                  '@class="tag"]/text()').extract()
        #
        # item['cuisine'] = tag_addrs[::2]
        # [Logging.info('cuisine: %s' % cuisine) for cuisine in item['cuisine']]
        #
        # item['comment_count'] = response.xpath('//li[@class=""]/div[@class="txt"]/div[@class="comment"]/a['
        #                                        '@class="review-num"]/b/text()').extract()
        # [Logging.info('comment_count: %s' % comment_count) for comment_count in item['comment_count']]
        #
        # item['avg_price'] = response.xpath('//li[@class=""]/div[@class="txt"]/div[@class="comment"]/a['
        #                                    '@class="mean-price"]/b/text()').extract()
        # [Logging.info('avg_price: %s' % avg_price) for avg_price in item['avg_price']]
        #
        # item['district'] = tag_addrs[1::2]
        # [Logging.info('district: %s' % district) for district in item['district']]
        #
        # item['street'] = response.xpath('//li[@class=""]/div[@class="txt"]/div[@class="tag-addr"]/span['
        #                                 '@class="addr"]/text()').extract()
        # [Logging.info('street: %s' % street) for street in item['street']]

        Logging.debug('<---------- 解析完成 ---------->')

        return item
