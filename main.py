from vkinder import VKinder
from json_writer import Json_writer
from mongo_writer import Mongo_writer

if __name__ == '__main__':
    token = input('Введите токен пользователя ')
    v = VKinder(
        token,
        result_writer=Json_writer(),
        db=Mongo_writer()
    )
    v.do()
