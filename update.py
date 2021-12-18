"""
    this module uses for updating the project files from github without using git.
"""

from os import walk,mkdir,unlink,system

need_modules = ['flask', 'jdatetime','requests']
for module in need_modules:
    try:
        import requests
    except:
        system('python -m pip install ' + module)
        import requests

import zipfile
import random
import shutil
import string
from os.path import join,exists

PROJECT_NAME = 'cs_khu_project-master'
ZIP_FILE = 'zip.zip'

print('starting update . . . ')
print('downloading . . . ')
DOWNLOAD_URL = 'https://github.com/duniyalr/cs_khu_project/archive/refs/heads/master.zip'

r = requests.get(DOWNLOAD_URL)

open(ZIP_FILE, 'wb').write(r.content)

directory_name = '.'+''.join(random.choice(string.ascii_lowercase) for _ in range(10))

with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
    zip_ref.extractall(directory_name)

print('download completed.')
print('starting building . . . ')

for dirpath, dirnames, filenames in walk(join(directory_name, PROJECT_NAME)):
    abspath = dirpath
    dirpath = '.'+dirpath.replace(directory_name, '').replace('\\'+PROJECT_NAME, '')
    if not exists(dirpath): mkdir(dirpath)
    for filename in filenames:
        f = open(join(abspath, filename), 'r').read()
        fw = open(join(dirpath, filename), 'w').write(f)
        print(f'creating {str(join(dirpath, filename))}')

shutil.rmtree(directory_name)
unlink(ZIP_FILE)

print('update completed!')