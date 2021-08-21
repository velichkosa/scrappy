# final_branch

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VacancyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    scrap = scrapy.Field()
    _id = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    new_price = scrapy.Field()
    old_price = scrapy.Field()
    rate = scrapy.Field()
    source = scrapy.Field()
    scrap = scrapy.Field()
    _id = scrapy.Field()
    pass
