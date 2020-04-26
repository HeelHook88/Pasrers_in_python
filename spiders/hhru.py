# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self):
        self.start_urls = [
            'https://mikhajlovsk-stavropol.hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

    def vacancy_parce(self, response: HtmlResponse):
        name = response.xpath("//h1[@class='bloko-header-1']/text()").extract_first()
        link = response.url
        salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        source = self.name
        yield JobparserItem(name=name, salary=salary, link=link, source=source)




