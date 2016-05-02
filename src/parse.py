import json
import os

from functools import partial

from utils import log, directory


def parse(callback):
    results = []
    assert callback
    callback = parsers[callback]
    for root, dir_, filenames in os.walk(directory):

        for filename in filenames:
            path = os.path.join(root, filename)
            if filename == 'addon.json':
                data = json.load(open(path, 'r'))
                if callback(data):
                    results.append(data)

    return results


def is_type(type, data):
    return data['type'] == type


parsers = {
    'is_extension': partial(is_type, 'Extension')
}

if __name__=='__main__':
    results = parse('is_extension')
