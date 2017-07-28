# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class QuotesbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # defining these inline with the quotesbot example
    text 		= scrapy.Field()
    author 		= scrapy.Field()
    tags 		= scrapy.Field()
    rank		= scrapy.Field()
    date_added 	= scrapy.Field() # this is my own addition to test the feed exports
