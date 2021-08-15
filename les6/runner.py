# final_branch

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from les6 import settings
from les6.spiders.hhru import HhruSpider
from les6.spiders.supajob import SupajobSpider
from les6.spiders.labirint import LabirintSpider
from les6.spiders.book24 import Book24Spider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SupajobSpider)
    process.crawl(LabirintSpider)
    process.crawl(Book24Spider)
    process.start()