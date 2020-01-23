import pathlib
import os
import json


def ensure_dir(path):
    dir_path = pathlib.Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)


def store(basedir, data):
    fname = data['hash']
    path = f'{basedir}/{fname}'
    if os.path.exists(path):
        obj = retrieve(basedir, data['hash'])
        obj.append(data)
    else:
        obj = [data]
    with open(path, 'w+') as f:
        f.write(json.dumps(obj))


def retrieve(basedir, objhash):
    path = f'{basedir}/{objhash}'
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None