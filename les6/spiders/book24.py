# final_branch

import scrapy
from scrapy.http import HtmlResponse
from les6.items import Les6Item


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/ezotericheskie-khudozhestvennye-knigi-1664']
    pagination = int(2)

    def parse(self, response: HtmlResponse):
        vac_links = response.xpath("//a[@class='product-card__image-link smartLink']//@href").extract()
        next_page = self.start_urls[0] + f'/page-{self.pagination}'
        self.pagination += 1
        for element in vac_links:
            yield response.follow(element, callback=self.book_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        title = response.xpath("//h1[@class='product-detail-page__title']/text()").extract_first().replace('\n', '').replace('  ','')
        book_link = response.url
        author = response.xpath("//span[@itemprop='author']/meta[@itemprop='name']/@content").extract_first()
        new_price = response.xpath("//meta[@property='product:price:amount']/@content").extract_first()
        old_price = response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").extract_first()
        rate = response.xpath("//meta[@itemprop='ratingValue']/@content").extract_first()
        src = Book24Spider.allowed_domains[0]
        scrap = 'book24_ru'
        item = Les6Item(title=title, link=book_link, author=author, new_price=new_price, \
                        old_price=old_price, rate=rate, source=src, scrap=scrap)
        yield item