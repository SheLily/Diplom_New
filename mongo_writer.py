from pymongo import MongoClient
import pymongo
from mongo_config import url

class Mongo_writer:
    def __init__(self):
        self.db_name = 'vkinder'
        self.connect = MongoClient(url)

        self.db = self.connect[f'{self.db_name}-database']
        self.db = self.db[f'{self.db_name}-collecction']
        self.connected = True
        print('Попытка подключения к БД...', end='')
        try:
            self.read_viewed(0)
            print('Успех!')
        except pymongo.errors.ServerSelectionTimeoutError:
            print('Провал!')
            self.connected = False
            print('Проблемы с подключением к базе данных\nПрверьте правильность url ')


    def read_viewed(self, main_id):
        if self.connected:
            return {
                i['view_id'] for i in self.db.posts.find({'main_id': main_id})
            }
        return {}

    def write_viewed(self, main_id, data):
        if self.connected:
            for i in data:
                self.db.posts.insert_one(
                    {
                        'main_id': main_id,
                        'view_id': i['id'],
                        'photos': i['photos']
                    }
                )
