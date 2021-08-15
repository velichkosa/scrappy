from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from les6 import settings
from les6.spiders.hhru import HhruSpider
from les6.spiders.supajob import SupajobSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SupajobSpider)

    process.start()
