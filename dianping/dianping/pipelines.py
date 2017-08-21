# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import ConfigParser, threading
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_table, DianPing
from Logging import Logging
from IPProxyTool import IPProxyTool
from apscheduler.schedulers.blocking import BlockingScheduler

cp = ConfigParser.SafeConfigParser()
path = os.path.abspath('../..') + '/' + 'config.cfg'
cp.read(path)

class DianpingPipeline(object):
    def __init__(self):
        # 连接数据库
        try:
            engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=utf8' % (
                cp.get('db', 'user'), cp.get('db', 'pwd'), cp.get('db', 'host'), cp.get('db', 'port'),
                cp.get('db', 'dbname')), echo=False)

            DBSession = sessionmaker(bind=engine)
            self.metadata = MetaData(engine)
            self.db_session = DBSession()

        except Exception as e:
            raise e

        # 创建表
        create_table(engine)

        self.ipTool = IPProxyTool()
        self.ipTool.destIP = 'https://www.dianping.com'
        self.ipTool.refresh()

        self.thread = threading.Thread(target=self.schedule)
        self.thread.setDaemon(True)
        self.thread.start()


    def process_item(self, item, spider):

        cuisines = item['cuisine']
        names = item['name']
        shop_url = item['shop_url']
        stars = item['star']
        comment_counts = item['comment_count']
        avg_prices = item['avg_price']
        districts = item['district']
        streets = item['street']
        update_times = item['update_time']


        for index in range(len(names)):
            model = DianPing(cuisine=cuisines[index],
                             shop_url=shop_url[index],
                             name=names[index],
                             star=stars[index],
                             comment_count=comment_counts[index],
                             avg_price=avg_prices[index],
                             district=districts[index],
                             street=streets[index],
                             update_time=update_times[index])
            self.db_session.add(model)
        self.db_session.commit()

        return item

    def close_spider(self, spider):
        self.db_session.close()

    def schedule(self):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.ipTool.refresh, 'interval', seconds=300)
        scheduler.start()

