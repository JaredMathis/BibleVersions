
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

for version in versions:
    version_directory = os.path.join(directory_wordproject, version)
    def for_each(book):
        book_directory = os.path.join(version_directory, book)
        files = os.listdir(book_directory)
        for chapter in files:
            f_path = os.path.join(book_directory, chapter)
            with open(f_path, 'r', encoding='utf-8') as source:
                output_directory = os.path.join(directory_public, version, book_directory)
                dir_create_if_not_exists(output_directory)
                output_path = os.path.join(output_directory, str_ending_rename(chapter, '.htm', '') + ".json")
                with open(output_path, 'w', encoding='utf-8') as output:
                    parsed = html_parse(source)
                    h = parsed.find_all('h1')
                    book = list_first(h).text.strip()
                    s = parsed.find_all('span', {"class":"chapread"})
                    chapter = list_first(s).text.strip()
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
                    exit()
    directory_for_each_if_numeric(version_directory, for_each)