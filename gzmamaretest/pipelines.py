# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.exceptions import DropItem
import logging
from pymongo import MongoClient

from scrapy.utils.log import configure_logging

from scrapy.contrib.exporter import CsvItemExporter as csvep


# configure_logging(install_root_handler=False)
# #定义了logging的些属性
# logging.basicConfig(
#     filename='log22.txt',
#     format='%(levelname)s: %(levelname)s: %(message)s',
#     level=logging.DEBUG
# )
#运行时追加模式
logging.info('进入Log文件')
logger = logging.getLogger('GzmamaretestPipeline')
logger.warning("也要进入Log文件")


class GzmamaretestPipeline(object):
	def open_spider(self, spider):
		self.connection = MongoClient('localhost', 27017)
		self.database = self.connection['test']
		self.collection = self.database['aaaa']
		#self.log('GzmamaretestPipeline - open_spider FUNC',logging.DEBUG)
		logger.info("GzmamaretestPipeline - open_spider FUNC - process_item FUNC")
		#print('find mongod data',self.collection.find_one())

	def process_item(self, item, spider):
		#self.log('GzmamaretestPipeline - process_item FUNC',logging.DEBUG)
		#self.log(item,logging.DEBUG)
		logger.info("GzmamaretestPipeline - process_item FUNC")
		postItem = dict(item)
		self.collection.insert(postItem)
		return item

class UsedCsvItemExporter(object):
    def __init__(self):
        #file = open('e:\\657.csv','wb+',encoding='UTF-8')
        file = open('e:\\657.csv','wb+')
        self.csvwriter = csvep(file,('Title','Url','CommentInfo','ImgSet','WordInfo','FormInfo'))
        pass
    def process_item(self, item, spider):
    	#有些字段可能不存在 error
        rows = zip(item['URL'],item['title'],item['extraInfo'])
        for row in rows:
            logger.debug(row)
            self.csvwriter.csv_writer.writerow(row)
        return item