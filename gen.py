
from common import *
import json

import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials

first_chapter_only = False
delete_firebase_blobs = False

cred = credentials.Certificate(os.path.join(directory_gitignore, 'firebasecreds.json'))
firebase_admin.initialize_app(cred)

# Get a reference to the Cloud Storage bucket
bucket = storage.bucket('wlj-bible-versions.appspot.com')

directory_public = 'public'
dir_create_if_not_exists(directory_public)

versions = [
    'sp'
]

def directory_for_each_if_numeric(parent, for_each):
    files = os.listdir(parent)
    for f in files:
        if f.isnumeric():
            for_each(f)

def file_html_parse(file_path):
    with open(file_path, 'r', encoding='utf-8') as source:
        parsed = html_parse(source)
        return parsed

def file_json_write(file_path, result):
    # Create a new blob in the bucket
    blob = bucket.blob(file_path.replace('\\','/').replace('public/',''))
    if delete_firebase_blobs:
        if blob.exists():
            blob.delete()
    else:
        j = json_to(result)
        with open(file_path, 'w', encoding='utf-8') as output:
            output.write(j)
        # Upload the file to the bucket
        blob.upload_from_filename(file_path)
        if first_chapter_only:
            exit()

def json_to(result):
    j = json.dumps(result, ensure_ascii=False, indent=4)
    return j

#BSB

#Wordproject

for version in versions:
    index = {}
    version_directory_input = os.path.join(directory_wordproject, version)
    version_directory_output = os.path.join(directory_public, version_directory_input)
    def for_each(book_number):
        book_directory = os.path.join(version_directory_input, book_number)
        files = os.listdir(book_directory)
        for chapter in files:
            f_path = os.path.join(book_directory, chapter)
            parsed = file_html_parse(f_path)
            output_directory = os.path.join(directory_public, book_directory)
            dir_create_if_not_exists(output_directory)
            output_path = os.path.join(output_directory, str_ending_rename(chapter, '.htm', '') + ".json")
            h = parsed.find_all('h1')
            book = list_first(h).text.strip()
            if not book_number in index:
                index[book_number] = {}
                index[book_number]["name"] = book
                index[book_number]["chapters"] = []
            s = parsed.find_all('span', {"class":"chapread"})
            chapter = list_first(s).text.strip()
            index[book_number]["chapters"].append(chapter)
            # Make sure the chapters are sorted by integer and not string
            index[book_number]["chapters"] = sorted(index[book_number]["chapters"], key=lambda e:int(e))
            verses = str(parsed.find_all('p')[-2])
            verses_list = verses.split('<br/>')
            result = []
            for v in verses_list:
                t = html_parse(v).text.strip('\n')
                s = t.split(' ')
                verse = s[0]
                tokens = s[1:] 
                result.append({"book":book,"chapter":chapter,"verse":verse,"tokens":tokens})
            file_json_write(output_path, result)

    directory_for_each_if_numeric(version_directory_input, for_each)
    
    output_path = os.path.join(version_directory_output, 'index.json')
    file_json_write(output_path, index)
