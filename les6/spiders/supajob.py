# final_branch

import scrapy
from scrapy.http import HtmlResponse
from les6.items import Les6Item


class SupajobSpider(scrapy.Spider):
    name = 'supajob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://spb.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        vac_links = response.xpath("//div[@class='_1ID8B']//a[contains(@class,'icMQ_ _6AfZ9')]//@href").extract()
        next_page = response.xpath("//a[@rel='next' and contains(@class,'dalshe')]/@href").extract_first()
        for element in vac_links:
            yield response.follow(element, callback=self.vac_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vac_parse(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").extract_first()
        vac_sal = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").extract()
        vac_link = response.url
        vac_src = SupajobSpider.allowed_domains[0]
        scrap = 'superjob_ru'
        item = Les6Item(name=vac_name, salary=vac_sal, link=vac_link, source=vac_src, scrap=scrap)
        yield item