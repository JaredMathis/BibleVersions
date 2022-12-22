
from common import *

dir_create_if_not_exists('public')

versions = [
    'sp'
]

for v in versions:
    parent = directory_wordproject
    files = os.listdir(os.path.join(parent, v))
    for f in files:
        if f.isnumeric():
            print(f)