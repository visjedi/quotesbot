# -*- coding: utf-8 -*-

import scrapy
from datetime import datetime
from quotesbot.items import QuotesbotItem

class RequestGenerator():

	def __init__(self):

		self.items_per_page = 10
		self.urls = ['http://quotes.toscrape.com/page/{}'.format(pageno) for pageno in range(2,11)] # 2,3..10, 1 is already in start_urls
		#self.urls[3] = 'https://seedrs.imgix.net/uploads/startup/entrepreneur/photo/31825/56w2hm49d48irib0d3xerb4ot3uo4au/jos_hermens'
		#self.urls[4] = 'http://alexandre'
		#self.urls[5] = 'http://robert'
		self.i = 0 # counter to track which was last returned

	def get_items_per_page(self):
		return self.items_per_page

	def get_next_page_url(self): 
		try:
			pageno =  self.urls.pop(self.i)
			self.i += 1
		except IndexError as ie:
			return None
		return pageno


#-----------------------------------------------------------------------------------------------------------------
# A version of quotes spider when the requests are known before-hand.
#-----------------------------------------------------------------------------------------------------------------

class ManiQuoteScrape(scrapy.Spider):

	name = 'maniquotescrape' # should be here, otherwise scrapy wont pick it up in $ scrapy crawl commands
	start_urls = [
	'http://quotes.toscrape.com/page/1',
	]

	def __init__(self, **kwargs):
		print('self.name = {}'.format(self.name))
		super(ManiQuoteScrape, self).__init__(name=self.name, **kwargs)
		self.requestgenerator = RequestGenerator()
		self.ITEMS_PER_PAGE = self.requestgenerator.get_items_per_page()


	def parse(self, response):

		corresponding_request_url = response.request.url
		print('MANI : parse called for {}'.format(corresponding_request_url))

		page_no = int(corresponding_request_url.split('/')[-2])-1 # ['http:', '', 'quotes.toscrape.com', 'page', '3', '']
		
		item_count=0
		for quote in response.xpath('//div[@class="quote"]'):
			item_count += 1
			itm = QuotesbotItem()
			itm['text'] 	= quote.xpath('./span[@class="text"]/text()').extract_first()
			itm['author'] 	= quote.xpath('.//small[@class="author"]/text()').extract_first()
			itm['tags'] 	= quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
			itm['rank'] 	= str(page_no*self.ITEMS_PER_PAGE+item_count)
			#print('MANI : about to yield item from parse')
			yield itm

		# I am getting the next page to scrape through an external class which handles this url generation
		next_page_url = self.requestgenerator.get_next_page_url()
		if next_page_url is not None:
			print('yielding next request url : {}'.format(next_page_url))
			yield scrapy.Request(next_page_url, callback=self.parse, errback=self.on_error, dont_filter=True)
		else:
			return


	def on_error(self, response):
		print('YIPEEE : error callback works')
		print('Errored out request = {}'.format(response.request.url))


#-----------------------------------------------------------------------------------------------------------------
# A more fancy generator function which provides the next urls for the class below
#-----------------------------------------------------------------------------------------------------------------

def get_next_page_url():
    pageno = 2 # 1 will already be in start_urls
    while True: 
    	if pageno<=10:
    		url = 'http://quotes.toscrape.com/page/{}'.format(pageno)
    		yield url
    		pageno+=1
    	else:
            yield None # otherwise the control will stay in the while loop

class ManiQuoteScrapeFancy(scrapy.Spider):
	'''
	# A version of quotes spider which gets its next urls to scrape from a generator function
	'''
	name = 'maniquotescrapefancy'
	requestgenerator = get_next_page_url() # a generator object;see below for its definition


	def parse(self, response):
		print('parse called')

		for quote in response.xpath('//div[@class="quote"]'):
			yield 
			{
			'text'  : quote.xpath('./span[@class="text"]/text()').extract_first(),
			'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
			'tags'  : quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
			}

		# I am getting the next page to scrape
		next_page_url = next(self.requestgenerator) # from generator function

		if next_page_url is not None:
			print('### About to yield next request : {}'.format(next_page_url))
			yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)

