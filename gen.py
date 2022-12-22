
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
    parent = os.path.join(directory_wordproject, v)
    def for_each(f):
        print(f)
    directory_for_each_if_numeric(parent, for_each)