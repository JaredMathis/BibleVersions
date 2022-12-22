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

def directory_files_rename_if_ends_with(directory, ending, ending_new):
    def for_each(f):
        f_new = f[:len(f)-len(ending)] + ending_new
        os.rename(os.path.join(directory, f), os.path.join(directory, f_new))
    directory_files_for_if_ends_with(directory, ending, for_each)

def directory_files_for_if_ends_with(directory, ending, for_each):
    files = os.listdir(directory)
    for f in files:
        if f.endswith(ending):
            for_each(f)

directory = 'gitignore'
extension = '.zip'
def wordproject_downloads_fix_endings():
    endings = [
        ' (1)' + extension,
        '_new' + extension
    ]
    for ending in endings:
        directory_files_rename_if_ends_with(directory, ending, extension)

import zipfile

def unzip_to_wordproject(f):
    joined = os.path.join(directory, f)
    with zipfile.ZipFile(joined, 'r') as zip_ref:
        zip_ref.extractall(directory_wordproject)


directory_wordproject = 'wordproject'
def wordproject_unzip():
    dir_create_if_not_exists(directory_wordproject)
    directory_files_for_if_ends_with(directory, extension, unzip_to_wordproject)

# vatican_download()
# wordproject_download()
# wordproject_downloads_fix_endings()
wordproject_unzip()