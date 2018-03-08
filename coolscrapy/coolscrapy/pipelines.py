# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from contextlib import contextmanager
from scrapy.exporters import JsonItemExporter
from scrapy import signals
from sqlalchemy.orm import sessionmaker
from .models import db_connect, create_news_table, Huxiu

_log = logging.getLogger(__name__)


class JsonExportPipeline(object):
    def __init__(self):
        _log.info('JsonExportPipeline.init....')
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        _log.info('JsonExportPipeline.from_crawler....')
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        _log.info('JsonExportPipeline.spider_opened....')
        file = open('%s.json' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        _log.info('JsonExportPipeline.spider_closed....')
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        _log.info('JsonExportPipeline.process_item....')
        self.exporter.export_item(item)
        return item


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    # 终止 on commit = false
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class HuxiuDataBasePipeline(object):
    def __init__(self):
        # 建立数据库连接
        engine = db_connect()
        # create 表
        create_news_table(engine)
        # 建立session
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        a = Huxiu(
            title=item["title"].encode("utf-8"),
            link=item["link"].encode("utf-8"),
            published=item["published"]
        )
        # Session对象经过session_scope事务机制处理 为 session
        with session_scope(self.Session) as session:
            session.add(a)

    def close_spider(self, spider):
        pass
