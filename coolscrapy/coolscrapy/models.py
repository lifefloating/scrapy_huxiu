#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 定义数据库模型实体 表结构
Desc :
"""

import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # URL函数可以接受分开的url参数，和create_engine('xxx')一个效果
    return create_engine('mysql+pymysql://root:root@localhost:3306/spider')


def create_news_table(engine):
    """"""
    # 建立表
    Base.metadata.create_all(engine)


Base = declarative_base()


class Huxiu(Base):
    '''HuXiu item 里面的内容'''
    __tablename__ = 'huxiu'

    # id主键
    id = Column(Integer, primary_key=True)
    # 标题
    title = Column(String(100))
    # 链接
    link = Column(String(120), nullable=True)
    # desc = Column(String(100)
    published = Column(String(30))
