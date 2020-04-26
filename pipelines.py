# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client =MongoClient('localhost', 27017)
        self.mongo_base =client.vacansy_00

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if spider.name == 'sjru':

            item['money_type'] = None
            item['salary_min'] = None
            item['salary_max'] = None

            if len(item['salary']) is not 1:

                if len(item['salary']) is 4:
                    item['salary'] = item['salary'].replace('\xa0', '')
                    item['salary_min'] = item['salary'][0]
                    item['salary_max'] = item['salary'][1]
                    item['money_type'] = item['salary'][3]

                elif len(item['salary']) is 3 and 'от' in item['salary']:
                    item['salary_min'] = item['salary'][2].split('\xa0')[0:2]
                    item['money_type'] = item['salary'][2].split('\xa0')[2]

                elif len(item['salary']) is 3 and 'до' in item['salary']:
                    item['salary_max'] = item['salary'][2].split('\xa0')[0:2]
                    item['money_type'] = item['salary'][2].split('\xa0')[2]

            collection = self.mongo_base[spider.name]
            collection.insert_one(item)


        if spider.name == 'hhru':

            item['money_type'] = None
            item['salary_min'] = None
            item['salary_max'] = None

            if len(item['salary']) is not 1:
                item['salary'] = item['salary'].replace('\xa0', '')

                if len(item['salary']) is 7:

                    item['salary_min'] = item['salary'][1]
                    item['salary_max'] = item['salary'][3]
                    item['money_type'] = item['salary'][5]

                elif len(item['salary']) is 5 and 'от ' in item['salary']:
                    item['salary_min'] = item['salary'][1]
                    item['money_type'] = item['salary'][3]

                else:
                    item['salary_max'] = item['salary'][1]
                    item['money_type'] = item['salary'][3]

                collection = self.mongo_base[spider.name]
                collection.insert_one(item)


        return item
