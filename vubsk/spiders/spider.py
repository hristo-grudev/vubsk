import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import VubskItem
from itemloaders.processors import TakeFirst


class VubskSpider(scrapy.Spider):
	name = 'vubsk'
	start_urls = ['https://www.vub.sk/vub-novinky/']

	def parse(self, response):
		years_links = response.xpath('//a[@class="news-link"]/@href').getall()
		yield from response.follow_all(years_links, self.parse_year)

	def parse_year(self, response):
		post_links = response.xpath('//a[@class="news-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('/@href').getall()
		yield from response.follow_all(next_page, self.parse_year)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content-box"]//text()[normalize-space() and not(ancestor::h1 | ancestor::span[@class="perex-date"])]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="perex-date"]/text()').get()

		item = ItemLoader(item=VubskItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
