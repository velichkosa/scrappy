import scrapy
from scrapy.http import HtmlResponse
from les6.items import Les6Item


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://spb.hh.ru/search/vacancy?clusters=true&area=2&no_magic=true&ored_clusters=true&items_on_page=20'
        '&enable_snippets=true&salary=&st=searchVacancy&text=Python']

    def parse(self, response: HtmlResponse):
        vac_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']//@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        for element in vac_links:
            yield response.follow(element, callback=self.vac_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vac_parse(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").extract_first()
        vac_sal = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract_first()
        vac_link = response.url
        vac_src = HhruSpider.allowed_domains[0]
        item = Les6Item(name=vac_name, salary=vac_sal, link=vac_link, source=vac_src)
        yield item
        print()
