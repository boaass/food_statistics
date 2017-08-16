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
path = os.path.abspath('../..') + '/' + 'config.cfg'
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

        cuisines = item['cuisine']
        names = item['name']
        stars = item['star']
        comment_counts = item['comment_count']
        avg_prices = item['avg_price']
        districts = item['district']
        streets = item['street']

        for index in range(len(names)):
            model = DianPing(cuisine=cuisines[index],
                             name=names[index],
                             star=stars[index],
                             comment_count=comment_counts[index],
                             avg_price=avg_prices[index],
                             district=districts[index],
                             street=streets[index])
            self.db_session.add(model)
        self.db_session.commit()

        return item

    def close_spider(self, spider):
        self.db_session.close()
