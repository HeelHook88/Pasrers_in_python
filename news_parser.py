import datetime

from lxml import html
import requests
from pprint import pprint
from datetime import date
import pandas as pd
from pymongo import MongoClient
import json
import itertools

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}



def lenta():
    main_link = 'https://lenta.ru'
    response = requests.get(main_link, headers=header)
    root = html.fromstring(response.text)
    items = root.xpath("//div[@class='span4']/div[@class='item']")
    list_news = []

    for item in items:
        dict_news = {}
        dict_news['link'] = main_link+str(item.xpath("./a/@href")[0])
        dict_news['title'] = item.xpath("./a/text()")[0].replace('\xa0', ' ')
        dict_news['time'] = item.xpath("./a/time/@datetime")[0]
        dict_news['source'] = main_link
        list_news.append(dict_news)
    return list_news

def yandex():
    main_link = 'https://yandex.ru'
    response = requests.get(main_link, headers=header)
    root = html.fromstring(response.text)
    items = root.xpath("//div[@id='news_panel_news']/ol/li")
    list_news = []
    for item in items:
        dict_news = {}
        dict_news['link'] = item.xpath("./a[@rel='noopener']/@href")
        dict_news['title'] = item.xpath("./a/@aria-label")
        date_time_day = item.xpath("//span[contains(@class,'datetime__day')]/text()")
        date_time_month = item.xpath("//span[contains(@class,'datetime__month')]/text()")
        date_time_hour = item.xpath("//span[contains(@class,'datetime__hour')]/text()")
        date_time_min = item.xpath("//span[contains(@class,'datetime__min')]/text()")
        date_time = F'{date_time_day}:{date_time_month} {date_time_hour}:{date_time_min}'.replace('\'', '').replace('.', '').replace(', ', '')
        dict_news['date_time'] = date_time
        dict_news['source'] = main_link

        list_news.append(dict_news)

    return list_news


def mail_ru():
    main_link = 'https://news.mail.ru'
    response = requests.get(main_link, headers=header)
    root = html.fromstring(response.text)
    items = root.xpath("//table[@class='daynews__inner']//a |//ul/li/a |//ul/li//a[@class='link link_flex']|//a[@class='newsitem__title link-holder']")
    result = []
    for item in items:
        dict_news = {}
        #news_date = item.xpath("./span[@class='newsitem__param js-ago']/@datetime")
        #if news_date != []:
            #dict_news['date'] = news_date
        #else:
            #dict_news['date'] = date.today()

        dict_news['title'] = str(item.xpath("./span/span[@class='photo__title photo__title_new photo__title_new_hidden js-topnews__notification']/text() |./text() |./span/text()")).replace('\\xa0', ' ')
        dict_news['link'] = main_link + str(item.xpath("./@href")[0])
        dict_news['source'] = main_link
        result.append(dict_news)
    return result


news = yandex() + mail_ru() + lenta()
df = pd.DataFrame(news)

client = MongoClient('localhost', 27017)
db = client['news_base']
collection = db.news_base
df_dict = df.to_dict(orient='index')
df_list = [*df_dict.values()]
collection.insert_many(df_list)

pprint(df_list)


