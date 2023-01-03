import random
from time import sleep
import base64
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

directory_wordproject = 'wordproject'

directory_gitignore = 'gitignore'


def vatican_download():
    return links_download(
        'https://www.vatican.va/archive/ESL0506/', 
        "_INDEX.HTM", 
        lambda href: href.startswith('__'),
        '.htm',
        True)

def dir_create_if_not_exists(my_path):
    if os.path.exists(my_path):
        return
    else:
        os.makedirs(my_path)

def http_get_cached(url, file_extension='.htm', decode_response=True, cached_path = 'gitignore/cached_websites'):
    factor = 1000
    sleep_time = random.randrange(5 * factor, 10  * factor) / factor

    encoded = base64.b64encode(url.encode()).decode()
    encoded_path = os.path.join(cached_path, encoded + file_extension)

    dir_create_if_not_exists(cached_path)

    if not os.path.exists(encoded_path):
        print(f'downloading {url} to {encoded_path}')
        print(f'Sleeping for {sleep_time}s')
        sleep(sleep_time)
        http_get_save(url, encoded_path, decode_response)

    with open(encoded_path, 'r') as opened:
        body = opened.read()
        return body

def http_get_save(url, path_save, decode_response=True):
    with urlopen(url) as response:
        body = response.read()
        if decode_response:
            body = body.decode()
        with open(path_save, 'w') as f:
            f.write(body)

def html_parse(s):
    b = BeautifulSoup(s, features="html.parser")
    return b

def list_first(list):
    assert len(list) == 1
    return list[0]

def links_download(url_base, url_index, download_if, file_extension, decode_response):
    url_root = url_base + url_index
    b = html_parse(http_get_cached(url_root))
    hrefs = ([c['href'] for c in b.find_all('a', href=True)])
    subs = [url_base + x for x in filter(download_if, hrefs)]

    for sub in subs:
        try:
            yield http_get_cached(sub, file_extension, decode_response)
        except Exception as inst:
            print("error " + sub)
            print(inst)

def directory_files_for_if_ends_with(directory, ending, for_each):
    files = os.listdir(directory)
    for f in files:
        if f.endswith(ending):
            for_each(f)
        
def str_ending_rename(f, ending, ending_new):
    assert f.endswith(ending)
    f_new = f[:len(f)-len(ending)] + ending_new
    return f_new

def directory_files_rename_if_ends_with(directory, ending, ending_new):
    def for_each(f):
        f_new = str_ending_rename(f, ending, ending_new)
        os.rename(os.path.join(directory, f), os.path.join(directory, f_new))

    directory_files_for_if_ends_with(directory, ending, for_each)
