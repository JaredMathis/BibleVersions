import random
from time import sleep
import base64
import os
from urllib.request import urlopen

url = "https://www.vatican.va/archive/ESL0506/_INDEX.HTM"

def dir_create_if_not_exists(my_path):
    if os.path.exists(my_path):
        return
    else:
        os.makedirs(my_path)

def http_get_cached(url, cached_path = 'cached_websites'):
    factor = 1000
    sleep_time = random.randrange(5 * factor, 10  * factor) / factor

    encoded = base64.b64encode(url.encode()).decode()
    encoded_path = os.path.join(cached_path, encoded + '.htm')

    dir_create_if_not_exists(cached_path)

    if not os.path.exists(encoded_path):
        print(f'Sleeping for {sleep_time}s')
        sleep(sleep_time)
        http_get_save(url, encoded_path)

    with open(encoded_path, 'r') as opened:
        body = opened.read()
        return body

def http_get_save(url, encoded_path):
    with urlopen(url) as response:
        body = response.read().decode()
        with open(encoded_path, 'w') as f:
            f.write(body)

http_get_cached(url, cached_path)

