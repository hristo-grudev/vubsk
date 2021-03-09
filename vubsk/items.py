import scrapy


class VubskItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
