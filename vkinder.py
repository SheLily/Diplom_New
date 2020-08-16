import requests
from time import time, sleep


class VKinder:
    def __init__(self, token, result_writer=None, db=None, v='5.107', rps=3):
        self.token = token
        self.v = v
        self.request_time = 1 / rps
        self.result_writer = result_writer
        self.db = db
        self.base_config = {
            'access_token': self.token,
            'v': self.v
        }
        (
            self.main_id,
            self.sex,
            self.year,
            self.city
            ) = self.get_info()
        self.handle_bdate()

    def get_info(self):
        method = 'users.get'
        url = f'https://api.vk.com/method/{method}'
        config = self.base_config.copy()
        config['fields'] = 'bdate,sex,city,relation'
        start = time()
        result = requests.get(url, config).json()
        sleep_time = self.request_time - (time() - start)
        if sleep_time > 0:
            sleep(sleep_time)

        result = result['response'][0]
        try:
            return (
                result['id'],
                result['sex'],
                result['bdate'],
                result['city']['id'],
                )
        except KeyError:
            print('Одно или несколько полей пусто.')
            print('Пожалуйста, заполните в своем профиле следующие поля')
            print('\t1)День рождения')
            print('\t2)Страна и город')
            return [None]*4

    def handle_bdate(self):
        if not self.main_id:
            return None
        self.year = self.year.split('.')
        if len(self.year) == 2:
            self.year = input('Введите год рождения')
        else:
            self.year = self.year[-1]

    def do(self):
        if not self.main_id:
            return None

        if self.db:
            viewed = self.db.read_viewed(self.main_id)

        else:
            viewed = {}

        print('Получение списка кандидатов...', end='')
        method = 'users.search'
        url = f'https://api.vk.com/method/{method}'
        config = self.base_config.copy()
        config['city'] = self.city
        config['sex'] = 1 if self.sex == 2 else 2
        config['status'] = '6'
        config['birth_year'] = self.year
        config['count'] = 1000
        start = time()
        result = requests.get(url, config).json()['response']['items']
        sleep_time = self.request_time - (time() - start)
        if sleep_time > 0:
            sleep(sleep_time)
        result = [i for i in result if not i['is_closed']]
        print('Готово!')
        print('Фильтруем кандидатов...', end='')
        if viewed:
            result = [i for i in result if i['id'] not in viewed]
        result = result[:10]
        print('Готово!')
        print('Получаем фотографии кандидатов...', end='')
        for i in result:
            method = 'photos.get'
            url = f'https://api.vk.com/method/{method}'
            config = self.base_config.copy()
            config['owner_id'] = i['id']
            config['album_id'] = 'profile'
            config['extended'] = 1
            start = time()
            photos = requests.get(url, config).json()
            sleep_time = self.request_time - (time() - start)
            if sleep_time > 0:
                sleep(sleep_time)
            photos = photos['response']['items']
            photos.sort(key=lambda x: x['likes']['count'])
            i['photos'] = [photo['sizes'][-1]['url'] for photo in photos[:3]]
        print('Готово!')
        print('Сохраняем результаты...', end='')
        if self.db:
            self.db.write_viewed(self.main_id, result)
        result = [
            {
                'url': f'https://vk.com/id{i["id"]}',
                'photos': i['photos']
            } for i in result
            ]
        if self.result_writer:
            self.result_writer(self.main_id, result)
        print('Готово!')
        return result
