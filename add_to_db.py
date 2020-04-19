import pandas as pd
from pymongo import MongoClient, collection
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacansy']
collection = db.vacansy
df = pd.read_json(r'D:\pars\pars_hh.json', orient="columns")


def add_to_db():
    df_to_dict = df.to_dict(orient='index')
    df_list = [*df_to_dict.values()]
    collection.insert_many(df_list)
    return collection


def search():
    salary = 3000
    search_id_db = collection.find({'salary_min': {'$gt': salary}}, {'money_type': {'$eq': 'USD'}})
    pprint(search_id_db)


