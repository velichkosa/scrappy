import scrapy
from scrapy.http import HtmlResponse
from les6.items import Les6Item


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/rating/?id_genre=1852&nrd=1']

    def parse(self, response: HtmlResponse):
        vac_links = response.xpath("//a[@class='cover']//@href").extract()
        next_page = response.xpath("//div[@class='pagination-next']/a/@href").extract_first()
        for element in vac_links:
            yield response.follow(element, callback=self.book_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        title = response.xpath("//div[@id='product-info']/@data-name").extract_first()
        book_link = response.url
        author = response.xpath("//a[@data-event-label='author']/text()").extract_first()
        price = response.xpath("//span[@class='buying-price-val-number']/text()").extract_first()
        new_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        old_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        rate = response.xpath("//div[@id='rate']/text()").extract_first()
        src = LabirintSpider.allowed_domains[0]
        scrap = 'labirint_ru'
        item = Les6Item(title=title, link=book_link, author=author, price=price, new_price=new_price, \
                        old_price=old_price, rate=rate, source=src, scrap=scrap)
        yield item