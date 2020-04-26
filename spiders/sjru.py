# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['http://superjob.ru/']

    def __init__(self):
        self.start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        vacancy_links = response.xpath("//div[@class='_3mfro CuJz5 PlM3e _2JVkc _3LJqf']/a/@href").extract()

        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

        yield response.follow(next_page, callback=self.parse)

    def vacancy_parce(self, response: HtmlResponse):
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        link = response.url
        source = self.name
        yield JobparserItem(name=name, salary=salary, link=link, source=source)
