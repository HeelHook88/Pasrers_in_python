from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroy.leroy import settings
from leroy.leroy.spiders.leroy_merlin import LeroyMerlinSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyMerlinSpider)
    process.start()
