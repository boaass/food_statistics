# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import ConfigParser
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_table, DianPing
from Logging import Logging

cp = ConfigParser.SafeConfigParser()
path = os.path.abspath('.') + '/dianping' + 'config.cfg'
cp.read(path)


class DianpingPipeline(object):
    def __init__(self):
        # 连接数据库
        try:
            engine = create_engine('mysql://%s:%s@%s:%s/%s' % (
                cp.get('db', 'user'), cp.get('db', 'pwd'), cp.get('db', 'host'), cp.get('db', 'port'),
                cp.get('db', 'dbname')), echo=True)

            DBSession = sessionmaker(bind=engine)
            self.metadata = MetaData(engine)
            self.db_session = DBSession()

        except Exception as e:
            raise e

        # 创建表
        create_table(engine)

    def process_item(self, item, spider):

        commercial_areas = item['commercial_areas']
        cuisine = item['cuisine']
        name = item['name']
        star = item['star']
        comment_count = item['comment_count']
        avg_price = item['avg_price']
        district = item['district']
        street = item['street']

        Logging.debug('commercial_areas: ' + commercial_areas)
        Logging.debug('cuisine: ' + cuisine)
        Logging.debug('name: ' + name)
        Logging.debug('star: ' + star)
        Logging.debug('comment_count: %d' % comment_count)
        Logging.debug('avg_price: %d' % avg_price)
        Logging.debug('district: ' + district)
        Logging.debug('street: ' + street)

        # model = DianPing(commercial_areas=commercial_areas,
        #                  cuisine=cuisine,
        #                  name=name,
        #                  star=star,
        #                  comment_count=comment_count,
        #                  avg_price=avg_price,
        #                  district=district,
        #                  street=street)
        # self.db_session.add(model)
        # self.db_session.commit()

        return item

    def close_spider(self, spider):
        self.db_session.close()
