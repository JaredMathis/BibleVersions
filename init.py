import os

from common import *

def vatican_download():
    links_download(
        'https://www.vatican.va/archive/ESL0506/', 
        "_INDEX.HTM", 
        lambda href: href.startswith('__'),
        '.htm',
        True)

def wordproject_download():
    links_download(
        'https://www.wordproject.org/download/bibles/', 
        "index.htm", 
        lambda href: href.endswith('.zip'),
        '.zip',
        False)

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

def wordproject_unzip():
    dir_create_if_not_exists(directory_wordproject)
    directory_files_for_if_ends_with(directory, extension, unzip_to_wordproject)

def wordproject_unzipped_fix_endings():
    directory_files_rename_if_ends_with(directory_wordproject, '_new', '')

# vatican_download()
# wordproject_download()
# wordproject_downloads_fix_endings()
wordproject_unzipped_fix_endings()
