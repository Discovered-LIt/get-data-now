# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from scrapy.exceptions import DropItem
# import ipdb
# import pdb
import logging
from datetime import datetime

class NewsApiPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):

    # pdb.set_trace()
    today = 'newsAgg_' + datetime.strftime(datetime.now(), "%Y/%m/%d") 


    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py

        # pdb.set_trace()
        return cls (
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
        )


    def open_spider(self, spider):
    #     ## initializing spider
    #     ## opening db connection

        self.client = pymongo.MongoClient("mongodb+srv://discoveredlit:discoveredlit@likefolio-k9tqn.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client.newsAgg
        self.collection = self.db[self.today]
        # pdb.set_trace()


    def close_spider(self, spider):
    #     ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each post

        # pdb.set_trace()

        self.collection.insert(dict(item))

        logging.debug("Post added to MongoDB")
        return item

