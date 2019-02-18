# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo
from findjob.settings import MONGO_HOST, MONGO_PORT, MONGO_DB, FIVEONEJOB_MONGO_COLLECTION
from findjob.settings import ZHILIAN_MONGO_COLLECTION

class FindjobPipeline(object):
    def process_item(self, item, spider):
        return item

class FiveOneJobPipeline():

    def process_item(self, item, spider):
        client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        mongo_db = client[MONGO_DB]
        mongo_collection = mongo_db[FIVEONEJOB_MONGO_COLLECTION]

        mongo_collection.insert_one(dict(item))
        return item

class ZhiLianPipeline():

    def process_item(self, item, spider):
        client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        mongo_db = client[MONGO_DB]
        mongo_collection = mongo_db[ZHILIAN_MONGO_COLLECTION]
        mongo_collection.insert_one(dict(item))
        return item
