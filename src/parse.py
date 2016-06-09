import json
import os
import tempfile
import zipfile

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


def parse_xpi(callback):
    results = []
    assert callback
    callback = parsers[callback]
    for root, dir_, filenames in os.walk(directory):

        files_path = os.path.join(root, 'files')
        for files_root, files_dir_, files in os.walk(files_path):
            for filename in files:
                full_filename = os.path.join(files_root, filename)
                with zipfile.ZipFile(full_filename, 'r') as zippy:
                    result = callback(zippy)
                    if result:
                        results.append(result)

    return results


def is_type(type, data):
    return data['type'] == type


def has_package_json(zippy):
    path = tempfile.mkdtemp()
    try:
        package_json = zippy.extract('package.json', path)
    except KeyError:
        return

    return os.path.join(path, 'package.json')


parsers = {
    'is_extension': partial(is_type, 'extension'),
    'has_package_json': partial(has_package_json)
}


if __name__=='__main__':
    print len(parse('is_extension'))
    for filename in parse_xpi('has_package_json'):
        print open(filename, 'r').read()
