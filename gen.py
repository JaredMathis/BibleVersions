
from common import *

dir_create_if_not_exists('public')

versions = [
    'sp'
]

def directory_for_each_if_numeric(parent, for_each):
    files = os.listdir(parent)
    for f in files:
        if f.isnumeric():
            for_each(f)

for v in versions:
    version_directory = os.path.join(directory_wordproject, v)
    def for_each(f):
        chapter_directory = os.path.join(version_directory, f)
        files = os.listdir(chapter_directory)
        for f in files:
            f_path = os.path.join(chapter_directory, f)
            with open(f_path, 'r', encoding='utf-8') as f:
                parsed = html_parse(f)
                h = parsed.find_all('h1')
                book = list_first(h).text.strip()
                s = parsed.find_all('span', {"class":"chapread"})
                chapter = list_first(s).text.strip()
                verses = str(parsed.find_all('p')[-2])
                verses_list = verses.split('<br/>')
                for v in verses_list:
                    print({"book":book,"chapter":chapter,"v":v})
                exit()
    directory_for_each_if_numeric(version_directory, for_each)