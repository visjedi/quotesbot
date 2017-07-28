# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

class QuotesbotPipeline(object):
	
	def process_item(self, item, spider):
		print('Processed item of rank {}'.format(item['rank']))
		item['date_added'] = datetime.now()
		return item
