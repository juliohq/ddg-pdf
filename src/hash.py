import os
import hashlib

def get_hash(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    else:
        raise FileNotFoundError(f'Couldn\'t hash file {filepath}: the file doesn\'t exist')

def get_hash_raw(data):
    return hashlib.sha256(data).hexdigest()