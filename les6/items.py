# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Les6Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    _id = scrapy.Field()
    pass
