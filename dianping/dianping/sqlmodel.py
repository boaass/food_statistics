# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


def create_table(engine):
    Base.metadata.create_all(engine)


def drop_table(engine):
    Base.metadata.drop_all(engine)


class DianPing(Base):
    __tablename__ = 'dianping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 商区
    commercial_areas = Column(String(20))
    # 菜系分类
    cuisine = Column(String(20))
    # 店名
    name = Column(String(20))
    # 星级
    star = Column(String(20))
    # 点评数
    comment_count = Column(Integer)
    # 人均消费
    avg_price = Column(Integer)
    # 区
    district = Column(String(20))
    # 街道
    street = Column(String(50))

    def __repr__(self):
        return self.name
