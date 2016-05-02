import json
import hashlib
import os
import pprint
import requests
import shutil
import sys
import time

from utils import log, server, directory


def file_hash(file):
    hsh = hashlib.md5()
    hsh.update(open(file, 'r').read())
    return hsh.hexdigest()


def json_hash(json_obj):
    hsh = hashlib.md5()
    hsh.update(json.dumps(json_obj))
    return hsh.hexdigest()


def serialize_addon_result(result):
    addon_id = result['id']
    directories = get_directories(addon_id)
    files = get_files(addon_id)
    target_file = files['root']
    if os.path.exists(target_file):
        if file_hash(target_file) == json_hash(result):
            log.info('{}: No need to update, hashes match.'.format(addon_id))
        else:
            log.info('{}: Hashes differ.'.format(addon_id))
            shutil.move(target_file, files['backup'])
            json.dump(result, open(target_file, 'w'))
    else:
        log.info('{}: Writing addons.json.'.format(addon_id))
        json.dump(result, open(target_file, 'w'))


def fetch(url=None):
    url = url or server + '/api/v3/addons/search/?sort=created'
    log.info('Fetching: {}'.format(url))
    res = requests.get(url)
    res.raise_for_status()

    res_json = res.json()
    for addon in res_json['results']:
        serialize_addon_result(addon)

    if res_json['next']:
        fetch(res_json['next'])


if __name__=='__main__':
    fetch()
