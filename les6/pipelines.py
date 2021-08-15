# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class Les6Pipeline:

    def __init__(self):
        self.MONGO_HOST = "localhost"
        self.MONGO_PORT = 27017

    def process_item(self, item, spider):
        MONGO_COLLECTION = spider.name
        MONGO_DB = item['scrap']
        self.process_direct(item['scrap'], item, MONGO_COLLECTION, MONGO_DB)

    def process_direct(self, scrap, item, MONGO_COLLECTION, MONGO_DB):
        if scrap == 'hh_ru':
            self.process_sal_hh(item, MONGO_COLLECTION, MONGO_DB)
        elif scrap == 'superjob_ru':
            self.process_sal_sj(item, MONGO_COLLECTION, MONGO_DB)
        elif scrap == 'labirint_ru':
            self.process_labirint(item, MONGO_COLLECTION, MONGO_DB)
        elif scrap == 'book24_ru':
            self.process_book24(item, MONGO_COLLECTION, MONGO_DB)

    # разбор salary для HH
    def process_sal_hh(self, item, MONGO_COLLECTION, MONGO_DB):
        salary = item['salary']
        if salary == 'з/п не указана':
            sal_dct = {'min': None, 'max': None, 'cur': None}
        val = re.split(' – | ', salary.replace('\xa0', ''))
        if val == ['None']:
            sal_dct = {'min': None, 'max': None, 'cur': None}
        if len(val) == 3 and val[0] == 'от' and val[2] == 'руб.':
            sal_dct = {'min': int(val[1]), 'max': None, 'cur': 'руб.'}
        if len(val) == 3 and val[0] == 'от' and val[2] == 'USD':
            sal_dct = {'min': int(val[1]), 'max': None, 'cur': 'USD'}
        if len(val) == 3 and val[0] == 'от' and val[2] == 'EUR':
            sal_dct = {'min': int(val[1]), 'max': None, 'cur': 'EUR'}
        if len(val) == 3 and val[0] == 'до' and val[2] == 'USD':
            sal_dct = {'min': None, 'max': int(val[1]), 'cur': 'USD'}
        if len(val) == 3 and val[0] == 'до' and val[2] == 'руб.':
            sal_dct = {'min': None, 'max': int(val[1]), 'cur': 'руб.'}
        if len(val) == 3 and val[0] == 'до' and val[2] == 'EUR':
            sal_dct = {'min': None, 'max': int(val[1]), 'cur': 'EUR'}
        if len(val) == 3 and val[0] != 'до' and val[0] != 'от' \
                and val[1] != 'до' and val[1] != 'от' and val[2] == 'руб.':
            sal_dct = {'min': int(val[0]), 'max': int(val[1]), 'cur': 'руб.'}
        if len(val) == 3 and val[0] != 'до' and val[0] != 'от' \
                and val[1] != 'до' and val[1] != 'от' and val[2] == 'USD':
            sal_dct = {'min': int(val[0]), 'max': int(val[1]), 'cur': 'USD'}
        if len(val) == 3 and val[0] != 'до' and val[0] != 'от' \
                and val[1] != 'до' and val[1] != 'от' and val[2] == 'EUR':
            sal_dct = {'min': int(val[0]), 'max': int(val[1]), 'cur': 'EUR'}
        if len(val) == 5 and val[0] == 'от' and val[2] == 'до' and val[4] == 'руб.':
            sal_dct = {'min': int(val[1]), 'max': int(val[3]), 'cur': 'руб.'}
        if len(val) == 5 and val[0] == 'от' and val[2] == 'до' and val[4] == 'EUR':
            sal_dct = {'min': int(val[1]), 'max': int(val[3]), 'cur': 'EUR'}
        if len(val) == 5 and val[0] == 'от' and val[2] == 'до' and val[4] == 'USD':
            sal_dct = {'min': int(val[1]), 'max': int(val[3]), 'cur': 'USD'}
        item['salary'] = sal_dct
        self.to_mongo_vacancy(item, MONGO_COLLECTION, MONGO_DB)

    # разбор salary для SJ
    def process_sal_sj(self, item, MONGO_COLLECTION, MONGO_DB):
        salary = item['salary']
        if len(salary) == 1 and salary[0] == 'По договорённости':
            sal_dct = {'min': 'По договорённости', 'max': 'По договорённости', 'cur': '-'}
        elif len(salary) == 4:
            for el in range(len(salary)):
                salary[el] = salary[el].replace('\xa0', '')
            sal_dct = {'min': int(salary[0]), 'max': int(salary[1]), 'cur': salary[3]}
        else:
            for el in range(len(salary)):
                salary[el] = salary[el].replace('\xa0', '')
            salary.append(salary[2][-4:])
            salary[2] = salary[2][:-4]
            if salary[1] == '':
                sal_dct = {'min': None, 'max': int(salary[2]), 'cur': salary[3]}
            else:
                sal_dct = {'min': int(salary[1]), 'max': int(salary[2]), 'cur': salary[3]}
        item['salary'] = sal_dct
        self.to_mongo_vacancy(item, MONGO_COLLECTION, MONGO_DB)

    def process_labirint(self, item, MONGO_COLLECTION, MONGO_DB):
        self.to_mongo_book(item, MONGO_COLLECTION, MONGO_DB)

    def process_book24(self, item, MONGO_COLLECTION, MONGO_DB):
        self.to_mongo_book(item, MONGO_COLLECTION, MONGO_DB)

    def to_mongo_vacancy(self, base, MONGO_COLLECTION, MONGO_DB):
        with MongoClient(self.MONGO_HOST, self.MONGO_PORT) as client:
            db = client[MONGO_DB]
            users = db[MONGO_COLLECTION]
            update_data = {
                "$set": {
                    "name": base['name'],
                    "link": base['link'],
                    "salary": base['salary'],
                    "source": base['source']
                }
            }
            filter_data = {"link": base['link']}
            users.update_many(filter_data, update_data, upsert=True)

    def to_mongo_book(self, base, MONGO_COLLECTION, MONGO_DB):
        with MongoClient(self.MONGO_HOST, self.MONGO_PORT) as client:
            db = client[MONGO_DB]
            users = db[MONGO_COLLECTION]
            try:
                price = base['price']
            except:
                price = None
            update_data = {
                "$set": {
                    "author": base['author'],
                    "title": base['title'],
                    "link": base['link'],
                    "price": price,
                    "new price": base['new_price'],
                    "old price": base['old_price'],
                    "rate": base['rate'],
                    "source": base['source']
                }
            }
            filter_data = {"link": base['link']}
            users.update_many(filter_data, update_data, upsert=True)
