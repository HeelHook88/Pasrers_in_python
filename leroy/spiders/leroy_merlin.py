# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroy.leroy.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroyMerlinSpider(scrapy.Spider):
    name = 'leroy_merlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self):
        self.start_urls = ['https://leroymerlin.ru/search/?q=обои']

    def parse(self, response: HtmlResponse):

        links = response.xpath("//a[@class='black-link product-name-inner']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.pars_link)

        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

    def pars_link(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photo_urls', "//img[@alt='product image']/@src")
        loader.add_xpath('price', "//uc-pdp-price-view[1]/span/text()")
        loader.add_xpath('params', "//dt[@class='def-list__term']/text() | //dd[@class='def-list__definition']/text()")
        loader.add_value('link', response.url)
        yield loader.load_item()
