import scrapy

from scrapy.loader import ItemLoader

from ..items import BankonemuItem
from itemloaders.processors import TakeFirst


class BankonemuSpider(scrapy.Spider):
	name = 'bankonemu'
	start_urls = ['https://bankone.mu/en/latest-news/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="btn-with-hover"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="col-md-6 col-sm-6 col-xs-12 single-actu-subtitle"]/h1/text()').get()
		description = response.xpath('//div[@class="col-md-9 content-actu"]//text()[normalize-space() and not(ancestor::div[@class="next-prev"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="col-md-6 col-sm-6 col-xs-12 single-actu-subtitle"]/div[@class="date"]/text()').get()

		item = ItemLoader(item=BankonemuItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
