from python_oop import mail_ru_parser
from pymongo import MongoClient

if __name__ == '__main__':
    mrp = mail_ru_parser('study.ai_172@mail.ru', 'NewPassword172', MongoClient('localhost', 27017))
    mrp.login()

    while True:
        mrp.mail_parser()
        mrp.mover()

    mrp.add_to_db()

