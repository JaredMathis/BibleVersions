
from common import *
import json

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
            with open(output_path, 'w', encoding='utf-8') as output:
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
                json.dump(result, output, ensure_ascii=False, indent=4)
    directory_for_each_if_numeric(version_directory_input, for_each)
    
    output_path = os.path.join(version_directory_output, 'index.json')
    with open(output_path, 'w', encoding='utf-8') as output:
        json.dump(index, output, ensure_ascii=False, indent=4)
