import random
from time import sleep
import urllib.request
import base64
import os
import urllib

url = "https://www.vatican.va/archive/ESL0506/_INDEX.HTM"
cached_path = 'cached_websites'

def http_get(url, cached_path):
    factor = 1000
    sleep_time = random.randrange(5 * factor, 10  * factor) / factor

    encoded = base64.b64encode(url)
    encoded_path = os.path.join(cached_path, encoded + '.htm')

    if not os.path.exists(encoded_path):
        sleep(sleep_time)
        content = urllib.urlopen(url)
        with open(encoded_path, 'w') as f:
            f.write(content)

    with open(encoded_path, 'r') as opened:
        text = opened.read()

http_get(url, cached_path)

