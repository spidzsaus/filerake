from core.pools import *
from core.suggestions import *

from app.settings import *

from pathlib import Path

settings = UserSettings('config/settings.json')
st = settings.suggestion_table

home = Path('C:/Users/Ivan/Desktop')

paths = [f for f in home.iterdir() if f.is_file()]

for path in paths:
    print(f'Reviewing path {path}')
    suggs = list(st.suggest(path.name))
    if suggs:
        print('Suggested pools:')
        for i, pool in enumerate(suggs):
            print('\t' + f'[{i}]: {pool.name}')
    else:
        print('No suggestions found :C')
        print('\t***')
        continue
    idx = int(input('Enter pool ID (or type -1 if you want the file to stay):'))
    if idx == -1:
        continue
    suggs[idx].send(path)
input()