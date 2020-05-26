import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pymongo import MongoClient


class mvideo_parser():

    def __init__(self):
        self.options = Options()
        self.options.add_argument('start-maximized')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get('https://www.mvideo.ru/')
        assert "М.Видео -" in self.driver.title
        self.data = []
        self.button = ' '
        self.button_text = ' '
        #self.hits

    def mover(self):
        self.driver.execute_script("window.scrollTo(0, 2100)")
        self.hits = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sel-hits-block')))[1]
        self.button = self.hits.find_element_by_xpath(".//a[contains(@class, 'sel-hits-button-next')]")
        self.button_text = self.button.get_attribute('class')
        self.button.click()

    def parser(self):
        products = WebDriverWait(self.hits, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sel-product-tile-title')))

        for prod in products:
            items = {}

            items['link'] = prod.get_attribute('href')
            elem = json.loads(prod.get_attribute('data-product-info'))

            items['name'] = elem['productName']
            elem.pop('productName')

            items['id'] = elem['productId']
            elem.pop('productId')

            items['desr'] = elem

            self.data.append(items)




class ToDb:

    def __init__(self, data_for_save):
        self.client = MongoClient
        self.db = self.client['Tops_DB']
        self.db_tops = self.db.tops
        self.tops = data_for_save

    def to_mongo(self):
        self.db_tops.insert_one(self.tops)


