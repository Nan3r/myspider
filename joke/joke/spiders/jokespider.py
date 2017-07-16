#coding:utf-8
#__author__='Nan3r'

#http://www.jokeji.cn/list_1.htm
import  scrapy
from scrapy.http import Request
from joke.items import JokeItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class JokeSpider(scrapy.Spider):

	name = 'joke'
	allowed_domains = ['www.jokeji.cn']
	start_urls = []

	def start_requests(self):
		url_head = 'http://www.jokeji.cn/list_'
		for page in range(1, 500):
			self.start_urls.append(url_head+str(page)+'.htm')

		for url in self.start_urls:
			yield self.make_requests_from_url(url)

	def parse(self, response):
		hx = scrapy.selector.HtmlXPathSelector(response)
		firstUrl = hx.select('//div[@class="main"]/div[@class="joke_left"]/div[@class="list_title"]/ul/li/b/a/@href').extract()
		#firstTitle = hx.select('//div[@class="main"]/div[@class="joke_left"]/div[@class="list_title"]/ul/li/b/a/text()').extract()
		if firstUrl:
			for i in firstUrl:
				yield Request('http://www.jokeji.cn'+i, callback=self.parse_item)

	def parse_item(self, response):
		hx = scrapy.selector.HtmlXPathSelector(response)
		content = hx.select('//div[@class="main"]/div[@class="left"]/div[@class="left_up"]/ul/span[@id="text110"]/p/text()').extract()
		item = JokeItem()
		item['content'] = '<br/>'.join(content).strip()
		yield item


