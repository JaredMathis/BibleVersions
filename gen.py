
from common import *
import json

import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials

cred = credentials.Certificate(os.path.join(directory_gitignore, 'firebasecreds.json'))
firebase_admin.initialize_app(cred)

# Get a reference to the Cloud Storage bucket
bucket = storage.bucket('wlj-bible-versions.appspot.com')

first_chapter_only = False
delete_firebase_blobs = False
firebase_blobs_write = True


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

def file_read_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as source:
        return source.readlines()

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
        if firebase_blobs_write:
            blob.upload_from_filename(file_path)
            print(file_path)
        if first_chapter_only:
            exit()

def json_to(result):
    j = json.dumps(result, ensure_ascii=False, indent=4)
    return j

def update_index(index, book_number, chapter, book):
    if not book_number in index:
        index[book_number] = {}
        index[book_number]["name"] = book
        index[book_number]["chapters"] = []
    if chapter not in index[book_number]["chapters"]:
        index[book_number]["chapters"].append(chapter)
            # Make sure the chapters are sorted by integer and not string
        index[book_number]["chapters"] = sorted(index[book_number]["chapters"], key=lambda e:int(e))


def find_all_filter(parsed, tag_name, attribute_name, attribute_value):
    metas = parsed.find_all(tag_name)
    parts = [x for x in filter(lambda m:m.get(attribute_name) == attribute_value, metas)]
    return parts

for v in vatican_download():
    parsed = html_parse(v)
    parts = find_all_filter(parsed, 'meta', 'name', 'part')
    if (len(parts) == 0):
        continue
    part = parts[0]['content']
    split = part.split(' > ')
    if len(split) < 3:
        continue
    book = split[1]
    chapter = split[2]

    result = []

    MsoNormals = find_all_filter(parsed, 'p', 'class', ['MsoNormal'])
    for verse_element in MsoNormals:
        tokens = verse_element.text.split(' ')
        verse = tokens[0]
        tokens = tokens[1:]
        result.append({
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "tokens": tokens,
        })

exit()

#BSB
def biblehub_get():
    versions_to_generate = ["BSB"]
    verse_column = 0
    import csv
    bible_csv = file_read_lines('./biblehub/biblehub_bibles.csv')
    verse_reference = None
    result = {}
    index = {}
    book_number = 0
    book_previous = None
    i = 0
    versions = []
    for line in csv.reader(bible_csv):
        i = i+1
        if i == 1:
            versions = line[1:]
            for version in versions:
                result[version] = []
        if (line[0] == '\ufeff'):
            continue
        i = 1
        for version in [x for x in versions if x in versions_to_generate]:
            if line[verse_column] != '':
                if line[i] == '':
                    continue
                verse_reference = line[verse_column]
                result_verse = {"tokens": []}
                result[version].append(result_verse)
                book_number, book, chapter, verse = reference_parse(verse_reference, book_number, book_previous)
                book_previous = book
                result_verse["verse_reference"] = verse_reference
                result_verse["book"] = book
                result_verse["chapter"] = chapter
                result_verse["verse"] = verse
                update_index(index, book_number, chapter, book)
                result_verse["tokens"] = line[i].split(" ")
                i = i + 1
    return result,index

def reference_parse(verse_reference, book_number, book_previous):
    parsed1 = verse_reference.split(' ')
    book = " ".join(parsed1[:-1])
    if book != book_previous:
        book_number = book_number + 1
        book_previous = book
    chapter_verse = parsed1[-1]
    parsed2 = chapter_verse.split(':')
    assert len(parsed2) == 2
    chapter = parsed2[0] 
    verse = parsed2[1]
    return book_number,book,chapter,verse

result,index = biblehub_get()


def bible_write(result, index, bsb_path):
    bsb_index_output_path = os.path.join(bsb_path, 'index.json')
    if not os.path.exists(bsb_index_output_path):
        file_json_write(bsb_index_output_path, index)
    for book_number in index:
        book = index[book_number]["name"]
        book_output_path = os.path.join(bsb_path ,f"{book_number:02d}")
        dir_create_if_not_exists(book_output_path)
        for chapter in  index[book_number]["chapters"]:
            chapter_output_path = os.path.join(book_output_path, chapter + ".json")
            verses_for_book_and_chapter = [x for x in filter(lambda v:v["book"] == book and v["chapter"] == chapter, result)]
            if not os.path.exists(chapter_output_path):
                file_json_write(chapter_output_path, verses_for_book_and_chapter)

bible_write(result["BSB"], index, os.path.join("public", "berean"))


def bsb_get():
    verse_column = 5
    import csv
    bsb = file_read_lines('./bsb/bsb.csv')
    verse_reference = None
    result_bsb = []
    bsb_index = {}
    book_number = 0
    book_previous = None
    i = 0
    for line in csv.reader(bsb):
        i = i+1
        if i == 1:
            continue
        if (line[0] == ""):
            continue
        if line[verse_column] != '':
            result_verse = {"tokens": []}
            result_bsb.append(result_verse)
            verse_reference = line[verse_column]
            book_number, book, chapter, verse = reference_parse(verse_reference, book_number, book_previous)
            update_index(bsb_index, book_number, chapter, book)
        result_verse["verse_reference"] = verse_reference
        result_verse["book"] = book
        result_verse["chapter"] = chapter
        result_verse["verse"] = verse
        token = {}
        token["token"] = line[0]
        token["transliteration"] = line[1] 
        token["strong"] = line[4] 
        token["translation"] = line[6] 
        result_verse["tokens"].append(token)
    return result_bsb,bsb_index

result_bsb, bsb_index = bsb_get()

bible_write(result_bsb, bsb_index, os.path.join("public", "bsb"))

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
            s = parsed.find_all('span', {"class":"chapread"})
            chapter = list_first(s).text.strip()
            update_index(book_number, chapter, book)
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

