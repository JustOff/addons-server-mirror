import json
import os
import tempfile
import re
import zipfile

from functools import partial

from utils import log, directory

count = {}
regex = re.compile('(chrome|browser)\.(\w+)\.(\w+)')


def noop_callback(data):
    return data


def parse(callback=None, file_type='addon.json'):
    results = []
    callback = parsers.get(callback, parsers['noop_callback'])
    for root, dir_, filenames in os.walk(directory):
        data = {}
        for filename in filenames:
            path = os.path.join(root, filename)
            if filename in ['addon.json', 'compat.json']:
                data[filename.split('.')[0]] = json.load(open(path, 'r'))

        if data and callback(data):
            results.append(data)

    return results


def parse_xpi(callback=None):
    results = []
    callback = parsers.get(callback, parsers['noop_callback'])
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
    return data.get('addon', {}).get('type') == type


def is_compat(type, data):
    return data.get('compat', {}).get('e10s') == type


def has_package_json(zippy):
    path = tempfile.mkdtemp()
    try:
        package_json = zippy.extract('package.json', path)
    except KeyError:
        return

    return os.path.join(path, 'package.json')


def webextension_apis(zippy):
    path = tempfile.mkdtemp()
    zippy.extractall(path)

    count = {}

    def find(filename):
        data = open(filename, 'rb').read()

        while data:
            match = regex.search(data)
            if match:
                count.setdefault(match.group(), 0)
                count[match.group()] += 1
                data = data[match.end():]
            else:
                break

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.js'):
                full = os.path.join(root, file)
                print 'Examining ', full
                find(full)

    for k, v in count.items():
        global_counter.setdefault(k, 0)
        global_counter[k] += 1


global_counter = {}


parsers = {
    'noop_callback': partial(noop_callback),
    'is_extension': partial(is_type, 'extension'),
    'is_webextension': partial(is_compat, 'compatible-webextension'),
    'has_package_json': partial(has_package_json),
    'webextension_apis': partial(webextension_apis)
}
