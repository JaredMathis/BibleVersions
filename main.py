import random
from time import sleep
import base64
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

def dir_create_if_not_exists(my_path):
    if os.path.exists(my_path):
        return
    else:
        os.makedirs(my_path)

def http_get_cached(url, file_extension='.htm', decode_response=True, cached_path = 'cached_websites'):
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

def vatican_download():
    links_download(
        'https://www.vatican.va/archive/ESL0506/', 
        "_INDEX.HTM", 
        lambda href: href.startswith('__'),
        '.htm',
        True)

def links_download(url_base, url_index, download_if, file_extension, decode_response):
    url_root = url_base + url_index
    b = BeautifulSoup(http_get_cached(url_root), features="html.parser")
    hrefs = ([c['href'] for c in b.find_all('a', href=True)])
    subs = [url_base + x for x in filter(download_if, hrefs)]

    for sub in subs:
        try:
            http_get_cached(sub, file_extension, decode_response)
        except:
            print("error " + sub)

def wordproject_download():
    links_download(
        'https://www.wordproject.org/download/bibles/', 
        "index.htm", 
        lambda href: href.endswith('.zip'),
        '.zip',
        False)

# vatican_download()
# wordproject_download()

directory = 'gitignore'
ending = ' (1).zip'
ending_new = '.zip'
def directory_files_rename_if_ends_with(directory, ending, ending_new):
    files = os.listdir(directory)
    for f in files:
        if f.endswith(ending):
            f_new = f[:len(f)-len(ending)] + ending_new
            os.rename(os.path.join(directory, f), os.path.join(directory, f_new))
    return files

files = directory_files_rename_if_ends_with(directory, ending, ending_new)
print(files)
# os.rename()