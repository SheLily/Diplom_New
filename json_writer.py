import json
from datetime import datetime


class Json_writer:
    def __init__(self):
        pass

    def __call__(self, main_id, data):
        with open(
                (f'{main_id} '
                 f'{str(datetime.now()).replace(":", " ")}.json'), 'w') as fp:
            json.dump(data, fp)
