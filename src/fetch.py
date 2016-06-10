import json
import hashlib
import os
import pprint
import requests
import shutil
import sys
import time

from utils import log, server, get_directories, get_files

import sys
sys.setrecursionlimit(200000)

def file_hash(file):
    hsh = hashlib.md5()
    hsh.update(open(file, 'r').read())
    return hsh.hexdigest()


def json_hash(json_obj):
    hsh = hashlib.md5()
    hsh.update(json.dumps(json_obj))
    return hsh.hexdigest()


def serialize_addon_result(addon_id, result, type='root'):
    directories = get_directories(addon_id)
    files = get_files(addon_id)
    target_file = files[type]
    if os.path.exists(target_file):
        if file_hash(target_file) == json_hash(result):
            log.info('{}: No need to update, hashes match.'.format(addon_id))
        else:
            log.info('{}: Hashes differ.'.format(addon_id))
            shutil.move(target_file, files['backup'])
            json.dump(result, open(target_file, 'w'))
    else:
        log.info('{}: Writing json for {}'.format(addon_id, type))
        json.dump(result, open(target_file, 'w'))


def fetch(url=None):
    url = url or server + '/api/v3/addons/search/?sort=created&type=extension'
    log.info('Fetching: {}'.format(url))
    res = requests.get(url)
    res.raise_for_status()

    res_json = res.json()
    for addon in res_json['results']:
        serialize_addon_result(addon['id'], addon)

        compat = server + '/api/v3/addons/addon/{}/feature_compatibility/'.format(addon['id'])
        log.info('Fetching: {}'.format(compat))
        res = requests.get(compat)
        if res.status_code == 404:
            continue
        serialize_addon_result(addon['id'], res.json(), type='compat')

    if res_json['next']:
        fetch(res_json['next'])


if __name__=='__main__':
    fetch()
