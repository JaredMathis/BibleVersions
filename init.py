import os

from common import *

def wordproject_download():
    links_download(
        'https://www.wordproject.org/download/bibles/', 
        "index.htm", 
        lambda href: href.endswith('.zip'),
        '.zip',
        False)

extension = '.zip'
def wordproject_downloads_fix_endings():
    endings = [
        ' (1)' + extension,
        '_new' + extension
    ]
    for ending in endings:
        directory_files_rename_if_ends_with(directory_gitignore, ending, extension)

import zipfile

def unzip_to_wordproject(f):
    joined = os.path.join(directory_gitignore, f)
    with zipfile.ZipFile(joined, 'r') as zip_ref:
        zip_ref.extractall(directory_wordproject)

def wordproject_unzip():
    dir_create_if_not_exists(directory_wordproject)
    directory_files_for_if_ends_with(directory_gitignore, extension, unzip_to_wordproject)

def wordproject_unzipped_fix_endings():
    directory_files_rename_if_ends_with(directory_wordproject, '_new', '')

# vatican_download()
# wordproject_download()
# wordproject_downloads_fix_endings()
wordproject_unzipped_fix_endings()
