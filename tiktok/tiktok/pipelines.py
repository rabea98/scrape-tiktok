# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

class MongoDBPipeline(object):

	def __init__(self):
		settings = get_project_settings() 
		connection = MongoClient("mongodb+srv://user:pass@tiktok-ycelo.mongodb.net/test?retryWrites=true&w=majority")
		db = connection.get_database('tiktok')
		self.collection = db.users
		

	def process_item(self, item, spider):
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))
		if valid:
			inserted = False
			if self.collection.find({'ChannelName': dict(item)['ChannelName']}).limit(1).count() > 0:
				inserted = True	
			if not inserted:
				self.collection.insert(dict(item))
		return item
